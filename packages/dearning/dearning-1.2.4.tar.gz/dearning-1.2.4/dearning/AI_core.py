from __future__ import absolute_import, division, print_function, unicode_literals
import sys,os,time,json,threading,collections,logging,builtins,pathlib

class Converter:
    """A converter is a function that converts text, byte, or binary into something else.

    With the following functions:
    - text2binary, converts text to ASCII binary and vice versa
    - unit, converts a unit (for example a Byte) to another unit (for example KiloByte)"""
    UNITS = ("B", "KB", "MB", "GB", "TB", "PB")

    @staticmethod
    def text2binary(data, *, to="binary", encoding="utf-8", sep=" "):
        """text2binary is a function to convert text to ASCII binary and vice versa.
        
        example:
        >>> print(Converter.text2binary("Hello, World!", to="binary"))
        >>> print(Converter.text2binary("01001000 01100101 01101100 01101100 01101111 00101100 00100000 01010111 01101111 01110010 01101100 01100100 00100001", to="text"))"""
        if to == "binary":
            if isinstance(data, str): data = data.encode(encoding)
            if isinstance(data, (bytes, bytearray)): return sep.join(format(b, "08b") for b in data)
            raise TypeError("Input must be str or bytes")
        elif to == "text":
            if isinstance(data, str):
                parts = data.split(sep) if sep else [data[i:i+8] for i in range(0, len(data), 8)]
                if any(len(p) != 8 for p in parts): raise ValueError("Invalid binary block")
                data = bytes(int(p, 2) for p in parts)
            if isinstance(data, (bytes, bytearray)): return bytes(data).decode(encoding)
            raise TypeError("Input must be binary str or bytes")
        else: raise ValueError("Mode must be 'binary' or 'text'")

    @staticmethod
    def unit(value, to="B", binary=True, precision=4):
        """unit is a function to convert units (for example Bytes) into other units (for example KiloBytes).

        example:
        >>> print(Converter.unit("2B",to="KB"))"""
        base = 1024.0 if binary else 1000.0
        if isinstance(value, str):
            value = value.strip().upper()
            num = unit = ""
            for c in value:
                if c.isdigit() or c == ".": num += c
                else: unit += c
            if not num or unit not in Converter.UNITS: raise ValueError("Invalid byte format")
            value = float(num) * (base ** Converter.UNITS.index(unit))
        if not isinstance(value, (int, float)): raise TypeError("Value must be int, float, or string size")
        if to not in Converter.UNITS: raise ValueError("Unknown destination unit")
        result = value / (base ** Converter.UNITS.index(to))
        return round(result, precision)

_ALLOW_DAFE = getattr(builtins, "__dafe_internal__", False)
class Dafenot(object):
    def __init__(self):
        if not _ALLOW_DAFE: raise RuntimeError("DAFE internal only")
# logger, tidak enulis ke console secara default
logger = logging.getLogger("dearning.dafe")
logger.setLevel(logging.INFO)
HOME = pathlib.Path.home()
DAFE_DIR = HOME / ".dearning"
DAFE_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = DAFE_DIR / "dafe.log"
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s"))
logger.addHandler(file_handler)

class Dafe:
    def __init__(self, window_size=500, anomaly_threshold=8.0, telemetry_opt_in=False, auto_instrument=False):
        self.logs = []
        self.errors = []
        self.window_size = int(window_size)
        self.anomaly_threshold = float(anomaly_threshold)
        self.telemetry_opt_in = bool(telemetry_opt_in)
        self.auto_instrument = bool(auto_instrument)
        self._queue = collections.deque(maxlen=self.window_size)
        self._mean = None
        self._cov = None
        self._cov_inv = None
        self._lock = threading.RLock()
        self._stop_event = threading.Event()
        self._meta = {"created_at": time.time(),
                    "python_version": sys.version,
                    "dearning_version": self._detect_package_version()}
        from dearning.Quantum import Quantum
        try:
            self.quantum = Quantum(qubit_size=4)
            self.use_quantum = True
            logger.info("[DAFE] Quantum engine initialized.")
        except Exception:
            self.quantum = None
            self.use_quantum = False
            logger.warning("[DAFE] Quantum engine unavailable, fallback to classical mode.")

        # scan & start background
        self.scan_environment()
        self._bg_thread = threading.Thread(target=self._background_worker, daemon=True)
        self._bg_thread.start()
        if self.auto_instrument: logger.info("[DAFE] Auto-instrumentation requested (not enabled by default).")
        self.scan_environment() # initial checks (silent)

        # if auto_instrument True, you can implement function wrappers (dangerous) — TODO
        if self.auto_instrument: logger.info("[DAFE] Auto-instrumentation requested (not enabled by default).")

    # Environment checks
    def _detect_package_version(self):
        try: import importlib.metadata as imd # Python 3.8+
        except ImportError: import pkg_resources as imd # Python 3.4
        try: return imd.version("dearning")
        except Exception: return "unknown"

    def scan_environment(self):
        try:
            base_path = os.path.dirname(__file__)
            total_size = self.get_directory_size(base_path)
            self.logs.append("[DAFE] Total size dearning: {:.2f} KB".format(total_size / 1024))
            if sys.version_info < (3, 4): self.errors.append("This version of Python is not supported by dearning.")
            # log silently
            for l in self.logs: logger.info(l)
            for e in self.errors: logger.warning(e)
        except Exception as e:
            self.errors.append("[DAFE] Internal error: {}".format(str(e)))
            logger.exception("DAFE scan_environment error")

    def get_directory_size(self, path):
        total = 0
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.isfile(fp): total += os.path.getsize(fp)
        return total

    # record_event + quantum
    def record_event(self, feature_vector, meta=None):
        x = [float(v) for v in feature_vector]
        if self._mean and len(x) != len(self._mean): return
        # Queue & Mahalanobis
        with self._lock:
            self._queue.append(x)
            if len(self._queue) >= 2: self._update_stats()
            score = self._mahalanobis_distance(x) if self._cov_inv is not None else 0.0
            if score > self.anomaly_threshold:
                logger.warning("[DAFE] Suspicious activity detected (score=%.3f) meta=%s", score, str(meta))
                self._store_flagged(x, score, meta)
            else: logger.debug("[DAFE] event score=%.3f", score)

    def _store_flagged(self, x, score, meta):
        # prepare vector_mean safely (support built-in lists and objects like numpy arrays)
        if self._mean is None: vector_mean = None
        else:
            tolist = getattr(self._mean, "tolist", None)
            if callable(tolist):
                try: vector_mean = tolist()
                except Exception: vector_mean = list(self._mean)
            else: vector_mean = list(self._mean)
        rec = {"ts": time.time(),
                "score": float(score),
                "meta": meta or {},
                "vector_mean": vector_mean}
        # append to a local audit log file
        audit_file = DAFE_DIR / "audit.jsonl"
        try:
            with open(audit_file, "a", encoding="utf-8") as fh: fh.write(json.dumps(rec) + "\n")
        except Exception: logger.exception("DAFE failed to write audit record")

    def _update_stats(self): # Math: mean & covariance (matrix) + Mahalanobis
        # stack queue (n x d)
        arr = list(self._queue) # list of list, shape (n,d)

        # mean per kolom
        n = len(arr)
        d = len(arr[0])
        self._mean = [sum(col)/n for col in zip(*arr)]
        # covariance manual
        if n < 2:
            self._cov = None
            self._cov_inv = None
            return
        cov = [[sum((row[i]-self._mean[i])*(row[j]-self._mean[j]) for row in arr)/(n-1) for j in range(d)] for i in range(d)]
        # regularisasi
        eps = 1e-6
        for i in range(d): cov[i][i] += eps
        self._cov = cov
        try: self._cov_inv = self._matrix_inverse(cov) 
        except ValueError: self._cov_inv = None

    def _matrix_inverse(self, mat):
        n = len(mat)
        if n == 0: raise ValueError("Empty matrix")
        if any(len(row) != n for row in mat): raise ValueError("Matrix must be square")
        aug = [[float(v) for v in mat[i]] + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)] # construct augmented matrix [A | I]
        # Gauss-Jordan elimination
        for i in range(n):
            # find pivot with largest absolute value to improve stability
            pivot_row = max(range(i, n), key=lambda r: abs(aug[r][i]))
            if abs(aug[pivot_row][i]) < 1e-12: raise ValueError("Matrix is singular and cannot be inverted")
            # swap rows if needed
            if pivot_row != i: aug[i], aug[pivot_row] = aug[pivot_row], aug[i]
            # normalize pivot row
            pivot = aug[i][i]
            aug[i] = [val / pivot for val in aug[i]]
            # eliminate other rows
            for r in range(n):
                if r == i: continue
                factor = aug[r][i]
                if factor != 0.0: aug[r] = [aug[r][c] - factor * aug[i][c] for c in range(2 * n)]
        return [row[n:] for row in aug] # extract inverse part

    def _mahalanobis_distance(self, x):
        if self._mean is None or self._cov_inv is None: return 0.0
        # compute delta vector (list)
        delta = [xi - mi for xi, mi in zip(x, self._mean)]
        # compute quadratic form delta^T * cov_inv * delta manually
        d = len(delta)
        total = 0.0
        for i in range(d):
            row_sum = 0.0
            for j in range(d): row_sum += self._cov_inv[i][j] * delta[j]
            total += delta[i] * row_sum
        return float(total) 

    def _background_worker(self): # Background worker: periodic maintenance & optional updates
        logger.info("[DAFE] Background worker started.")
        while not self._stop_event.is_set():
            try:
                time.sleep(5)

                # do lightweight self-checks
                if len(self._queue) and (time.time() % 60) < 5:
                    # try re-evaluate cov inverse in case it becomes stable
                    with self._lock:
                        if self._queue: self._update_stats()

                # optional telemetry uploader only if user opted in
                if self.telemetry_opt_in:
                    # prepare small anonymous summary (counts, mean norms, flagged count)
                    try: self._upload_telemetry_summary()
                    except Exception: logger.debug("DAFE telemetry upload failed (ignored)")
            except Exception: logger.exception("DAFE background_worker error (ignored)")
        logger.info("[DAFE] Background worker stopped.")

    def _upload_telemetry_summary(self):
        # compute safe mean norm (self._mean may be None or empty)
        if self._mean:
            try: mean_norm = (sum(m**2 for m in self._mean))**0.5
            except Exception: mean_norm = 0.0
        else: mean_norm = 0.0
        summary = {"ts": time.time(),
                "queue_len": len(self._queue),
                "mean_norm": mean_norm,
                "dearning_version": self._meta.get("dearning_version")}
        tfile = DAFE_DIR / "telemetry_summary.jsonl"
        try:
            with open(tfile, "a", encoding="utf-8") as fh: fh.write(json.dumps(summary) + "\n")
        except Exception: logger.exception("DAFE failed to write telemetry summary")

    def stop(self):
        self._stop_event.set()
        if self._bg_thread.is_alive(): self._bg_thread.join(timeout=1.0)

    def report(self):
        logger.info("DAFE report requested.")
        # minimal console-safe output if environment variable set
        if os.environ.get("DAFE_VERBOSE") == "1":
            for e in self.errors: print("[DAFE] ERROR:", e)
            for l in self.logs: print("[DAFE]", l)

# create a global instance so it runs automatically on import within package
_global_dafe = None
def get_dafe():
    global _global_dafe
    if _global_dafe is None: _global_dafe = Dafe()
    return _global_dafe
record_event = lambda *a, **k: get_dafe().record_event(*a, **k)

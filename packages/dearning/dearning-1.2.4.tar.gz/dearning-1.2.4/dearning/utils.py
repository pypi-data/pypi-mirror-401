import platform,ctypes,logging,json,os,sys

logging.basicConfig(level=logging.INFO)

class cached:
    '''cached is a decorator that can cache the results of a function's calculations to speed up subsequent function calls.

       cached has:
       - "precision" improves the accuracy of the calculation results
       - "jit" a pseudo-Just-In-Time Optimizer (dynamically reorders Python code)

       cached can also debug via cached.debug, cached can also wrap other decorators, simply to compact the code.'''
    def __init__(self, *decorators, maxsize=128, mode=None, debug_modes=None, force_debug=False):
        self.decorators = decorators
        self.maxsize = maxsize
        self.mode = mode
        self.debug_modes = debug_modes or set()
        self.force_debug = force_debug

    def __call__(self, func):
        for deco in reversed(self.decorators): func = deco(func) # decorators 
        func = self._cache_wrapper(func) # caching
        if self.debug_modes: func = self._debug_wrapper(func) # debugging
        return func

    class jdi:
        '''jdi, make "time" and "memory" output logs without any specific conditions.

        Example:
        >>> @cached.debug(cached.jdi("memory"))
        >>> def add(a, b): return a + b
        >>> print(add(5, 10))'''
        __slots__ = ("modes", "force")
        def __init__(self, *modes):
            self.modes = set(modes)
            self.force = True

    @staticmethod
    def debug(*modes):
        '''cached.debug makes the cache decorator a debug decorator which has several features:
        - "time" logs if the function takes more than 0.7 seconds.
        - "memory" logs if the function uses 512 bytes or more.
        - "error" logs hidden errors.
        - jdi, forces debug logs to be issued without any specific conditions. '''
        force = False
        real_modes = set()
        for m in modes:
            if isinstance(m, cached.jdi):
                force = True
                real_modes |= m.modes
            else: real_modes.add(m)
        def decorator(func): return cached( maxsize=128, debug_modes=real_modes, force_debug=force)(func)
        return decorator

    def _cache_wrapper(self, func):
        import threading
        cache = {}
        cache_order = []
        lock = threading.RLock()
        jit_cache = {}
        mode = self.mode

        def make_hashable(obj):
            if isinstance(obj, (int, float, str, bytes, tuple, frozenset, type(None))): return obj
            if isinstance(obj, list): return tuple(map(make_hashable, obj))
            if isinstance(obj, set): return frozenset(map(make_hashable, obj))
            if isinstance(obj, dict): return tuple(sorted((k, make_hashable(v)) for k, v in obj.items()))
            try: return repr(obj)
            except Exception: return str(id(obj))

        def sumprecision(values):
            s = c = 0.0
            for v in values:
                y = v - c
                t = s + y
                c = (t - s) - y
                s = t
            return s

        def wrapper(*args, **kwargs):
            import copy
            key = (tuple(map(make_hashable, args)), tuple(sorted((k, make_hashable(v)) for k, v in kwargs.items())))
            with lock:
                if key in cache: return copy.deepcopy(cache[key])
            if mode == "precision":
                result = func(*args, **kwargs)
                if isinstance(result, (list, tuple)): result = sumprecision(result)
            elif mode == "jit":
                code = func.__code__
                h = (code.co_argcount, code.co_consts)
                fast = jit_cache.get(h)
                if fast is None:
                    f = func
                    locals_ = f.__globals__
                    def fast_call(*a, **kw): return f(*a, **kw)
                    jit_cache[h] = fast_call
                    fast = fast_call
                result = fast(*args, **kwargs)
            else: result = func(*args, **kwargs)
            with lock:
                cache[key] = copy.deepcopy(result)
                cache_order.append(key)
                if len(cache_order) > self.maxsize: del cache[cache_order.pop(0)]
            return result
        wrapper._cache_ref = cache
        return wrapper
    
    def _debug_wrapper(self, func):
        modes = set(self.debug_modes)
        def wrapper(*args, **kwargs):
            import time, traceback
            start = time.time()
            cache = getattr(func, "_cache_ref", None)
            mem_before = sys.getsizeof(cache) if cache is not None else 0
            try: return func(*args, **kwargs)
            except Exception as e:
                if "error" in modes:
                    print("\n[ERROR]", func.__name__)
                    print(traceback.format_exc())
                raise
            finally:
                elapsed = time.time() - start
                mem_after = sys.getsizeof(cache) if cache is not None else 0
                mem_used = mem_after - mem_before
                if "time" in modes:
                    if self.force_debug or elapsed > 0.7: print("[TIME] {} {:.4f}s".format(func.__name__, elapsed))
                if "memory" in modes and cache is not None:
                    if self.force_debug or mem_used >= 512: print("[MEMORY] {} {} bytes".format(func.__name__, mem_used))
        return wrapper

def scale_data(data):
    n = len(data)
    if not data: return data
    m = len(data[0])
    means = [sum(col)/n for col in zip(*data)]
    stdevs = [(sum((x-m)**2 for x in col)/n)**0.5 or 1 for col, m in zip(zip(*data), means)]
    return [[(row[j] - means[j]) / (stdevs[j] if stdevs[j] != 0 else 1) for j in range(m)] for row in data]

def preprocess_data(data, n_jobs=-1, optimizer_args=None):
    """preprocess_data is a function to perform data pre-processing."""
    if isinstance(data[0], (int, float)): data = [[x] for x in data]
    n_samples = len(data)
    n_features = len(data[0]) if data else 0
    def scale_batch(batch):
        cols = list(zip(*batch))
        means = [sum(col) / len(col) for col in cols]
        vars_ = [ sum((x - m) ** 2 for x in col) / len(col) for col, m in zip(cols, means)]
        stdevs = [(v ** 0.5 if v > 0 else 1.0) for v in vars_]
        return [[(x - m) / s for x, m, s in zip(row, means, stdevs)] for row in batch]
    if n_samples > 1000:
        import concurrent.futures
        batches = [data[i:i + 200] for i in range(0, n_samples, 200)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=None if n_jobs in (-1, 0, None) else n_jobs) as executor: scaled_batches = list(executor.map(scale_batch, batches))
        data_scaled = [x for sub in scaled_batches for x in sub]
    else: data_scaled = scale_batch(data)
    if optimizer_args is not None:
        w, b, grad_w, grad_b, layer_idx = optimizer_args[:5]
        method = optimizer_args[5] if len(optimizer_args) > 5 else "sgd"
        learning_rate = optimizer_args[6] if len(optimizer_args) > 6 else 0.01
        beta1 = optimizer_args[7] if len(optimizer_args) > 7 else 0.9
        beta2 = optimizer_args[8] if len(optimizer_args) > 8 else 0.999
        epsilon = optimizer_args[9] if len(optimizer_args) > 9 else 1e-8
        state = optimizer_args[10] if len(optimizer_args) > 10 else dict()
        method = method.lower()
        if method == "sgd":
            w_new = [[wij - learning_rate * gwij for wij, gwij in zip(wrow, grow)] for wrow, grow in zip(w, grad_w)]
            b_new = [bj - learning_rate * gbj for bj, gbj in zip(b, grad_b)]
        elif method == "momentum":
            m_w, m_b = state["m_w"], state["m_b"]
            if layer_idx not in m_w:
                m_w[layer_idx] = [[0.0] * len(row) for row in grad_w]
                m_b[layer_idx] = [0.0] * len(grad_b)
            m_w[layer_idx] = [[beta1 * mwij + (1 - beta1) * gwij for mwij, gwij in zip(mrow, grow)] for mrow, grow in zip(m_w[layer_idx], grad_w)]
            m_b[layer_idx] = [beta1 * mbj + (1 - beta1) * gbj for mbj, gbj in zip(m_b[layer_idx], grad_b)]
            w_new = [[wij - learning_rate * mwij for wij, mwij in zip(wrow, mrow)] for wrow, mrow in zip(w, m_w[layer_idx])]
            b_new = [bj - learning_rate * mbj for bj, mbj in zip(b, m_b[layer_idx])]
            state["m_w"], state["m_b"] = m_w, m_b
        elif method == "rmsprop":
            v_w, v_b = state["v_w"], state["v_b"]
            if layer_idx not in v_w:
                v_w[layer_idx] = [[0.0] * len(row) for row in grad_w]
                v_b[layer_idx] = [0.0] * len(grad_b)
            v_w[layer_idx] = [[beta2 * vwij + (1 - beta2) * (gwij ** 2) for vwij, gwij in zip(vrow, grow)] for vrow, grow in zip(v_w[layer_idx], grad_w)]
            v_b[layer_idx] = [beta2 * vbj + (1 - beta2) * (gbj ** 2) for vbj, gbj in zip(v_b[layer_idx], grad_b)]
            w_new = [[wij - learning_rate * gwij / ((vwij)**0.5 + epsilon) for wij, gwij, vwij in zip(wrow, grow, vrow)] for wrow, grow, vrow in zip(w, grad_w, v_w[layer_idx])]
            b_new = [bj - learning_rate * gbj / ((vbj)**0.5 + epsilon) for bj, gbj, vbj in zip(b, grad_b, v_b[layer_idx])]
            state["v_w"], state["v_b"] = v_w, v_b
        elif method == "adam":
            m_w, v_w, m_b, v_b = state["m_w"], state["v_w"], state["m_b"], state["v_b"]
            t = state.get("t", 1)
            if layer_idx not in m_w:
                m_w[layer_idx] = v_w[layer_idx] = [[0.0] * len(row) for row in grad_w]
                m_b[layer_idx] = v_b[layer_idx] = [0.0] * len(grad_b)
            m_w[layer_idx] = [[beta1 * mwij + (1 - beta1) * gwij for mwij, gwij in zip(mrow, grow)] for mrow, grow in zip(m_w[layer_idx], grad_w)]
            v_w[layer_idx] = [[beta2 * vwij + (1 - beta2) * (gwij ** 2) for vwij, gwij in zip(vrow, grow)] for vrow, grow in zip(v_w[layer_idx], grad_w)]
            m_b[layer_idx] = [beta1 * mbj + (1 - beta1) * gbj for mbj, gbj in zip(m_b[layer_idx], grad_b)]
            v_b[layer_idx] = [beta2 * vbj + (1 - beta2) * (gbj ** 2) for vbj, gbj in zip(v_b[layer_idx], grad_b)]
            m_w_hat = [[mwij / (1 - beta1 ** t) for mwij in mrow] for mrow in m_w[layer_idx]]
            v_w_hat = [[vwij / (1 - beta2 ** t) for vwij in vrow] for vrow in v_w[layer_idx]]
            m_b_hat = [mbj / (1 - beta1 ** t) for mbj in m_b[layer_idx]]
            v_b_hat = [vbj / (1 - beta2 ** t) for vbj in v_b[layer_idx]]
            t += 1
            state.update({"m_w": m_w, "v_w": v_w, "m_b": m_b, "v_b": v_b, "t": t})
            w_new = [[wij - learning_rate * mwij / ((vwij)**0.5 + epsilon) for wij, mwij, vwij in zip(wrow, mrow, vrow)] for wrow, mrow, vrow in zip(w, m_w_hat, v_w_hat)]
            b_new = [bj - learning_rate * mbj / ((vbj)**0.5 + epsilon) for bj, mbj, vbj in zip(b, m_b_hat, v_b_hat)]
        else: raise ValueError("Optimizer '{}' is not recognized.".format(method))
        return data_scaled, (w_new, b_new, state)
    return data_scaled

def evaluate_model(model, data, labels=None, task=None, threshold=0.5, optimizer_args=None):
    """evaluate_model is a function to evaluate a machine learning model for regression or classification.

    Features:
    - Auto-detection of tasks (regression/classification)
    - Evaluation metric calculation
    - Model parameter updates (optional)"""
    y_pred = model.forward(data)
    optimizer_result = None
    if optimizer_args is not None:
        w, b, grad_w, grad_b, layer_idx = optimizer_args[:5]
        method = optimizer_args[5] if len(optimizer_args) > 5 else "sgd"
        learning_rate = optimizer_args[6] if len(optimizer_args) > 6 else 0.01
        beta1 = optimizer_args[7] if len(optimizer_args) > 7 else 0.9
        beta2 = optimizer_args[8] if len(optimizer_args) > 8 else 0.999
        epsilon = optimizer_args[9] if len(optimizer_args) > 9 else 1e-8
        state = optimizer_args[10] if len(optimizer_args) > 10 else dict()
        method = method.lower()
        if not isinstance(grad_w[0], list):
            grad_w = [grad_w]
            w = [w]
        if method == "sgd":
            w_new = [[wij - learning_rate * gwij for wij, gwij in zip(wrow, grow)] for wrow, grow in zip(w, grad_w)]
            b_new = [bj - learning_rate * gbj for bj, gbj in zip(b, grad_b)]
        elif method == "momentum":
            m_w = state.get("m_w", {})
            m_b = state.get("m_b", {})
            if layer_idx not in m_w:
                m_w[layer_idx] = [[0.0 for _ in grow] for grow in grad_w]
                m_b[layer_idx] = [0.0 for _ in grad_b]
            m_w[layer_idx] = [[beta1 * mw + (1 - beta1) * gw for mw, gw in zip(mrow, grow)] for mrow, grow in zip(m_w[layer_idx], grad_w)]
            m_b[layer_idx] = [beta1 * mb + (1 - beta1) * gb for mb, gb in zip(m_b[layer_idx], grad_b)]
            w_new = [[wij - learning_rate * mw for wij, mw in zip(wrow, mrow)] for wrow, mrow in zip(w, m_w[layer_idx])]
            b_new = [bj - learning_rate * mb for bj, mb in zip(b, m_b[layer_idx])]
            state["m_w"], state["m_b"] = m_w, m_b
        elif method == "rmsprop":
            v_w = state.get("v_w", {})
            v_b = state.get("v_b", {})
            if layer_idx not in v_w:
                v_w[layer_idx] = [[0.0 for _ in grow] for grow in grad_w]
                v_b[layer_idx] = [0.0 for _ in grad_b]
            v_w[layer_idx] = [[beta2 * vw + (1 - beta2) * (gw ** 2) for vw, gw in zip(vrow, grow)] for vrow, grow in zip(v_w[layer_idx], grad_w)]
            v_b[layer_idx] = [beta2 * vb + (1 - beta2) * (gb ** 2) for vb, gb in zip(v_b[layer_idx], grad_b)]
            w_new = [[wij - learning_rate * gw / ((vw)**0.5 + epsilon) for wij, gw, vw in zip(wrow, grow, vrow)] for wrow, grow, vrow in zip(w, grad_w, v_w[layer_idx])]
            b_new = [bj - learning_rate * gb / ((vb)**0.5 + epsilon) for bj, gb, vb in zip(b, grad_b, v_b[layer_idx])]
            state["v_w"], state["v_b"] = v_w, v_b
        elif method == "adam":
            m_w = state.get("m_w", {})
            v_w = state.get("v_w", {})
            m_b = state.get("m_b", {})
            v_b = state.get("v_b", {})
            t = state.get("t", 1)
            if layer_idx not in m_w:
                m_w[layer_idx] = v_w[layer_idx] = [[0.0 for _ in grow] for grow in grad_w]
                m_b[layer_idx] = v_b[layer_idx] = [0.0 for _ in grad_b]
            m_w[layer_idx] = [[beta1 * mw + (1 - beta1) * gw for mw, gw in zip(mrow, grow)] for mrow, grow in zip(m_w[layer_idx], grad_w)]
            v_w[layer_idx] = [[beta2 * vw + (1 - beta2) * (gw ** 2) for vw, gw in zip(vrow, grow)] for vrow, grow in zip(v_w[layer_idx], grad_w)]
            m_b[layer_idx] = [beta1 * mb + (1 - beta1) * gb for mb, gb in zip(m_b[layer_idx], grad_b)]
            v_b[layer_idx] = [beta2 * vb + (1 - beta2) * (gb ** 2) for vb, gb in zip(v_b[layer_idx], grad_b)]
            m_w_hat = [[mw / (1 - beta1 ** t) for mw in mrow] for mrow in m_w[layer_idx]]
            v_w_hat = [[vw / (1 - beta2 ** t) for vw in vrow] for vrow in v_w[layer_idx]]
            m_b_hat = [mb / (1 - beta1 ** t) for mb in m_b[layer_idx]]
            v_b_hat = [vb / (1 - beta2 ** t) for vb in v_b[layer_idx]]
            w_new = [[wij - learning_rate * mw / ((vw)**0.5 + epsilon) for wij, mw, vw in zip(wrow, mrow, vrow)] for wrow, mrow, vrow in zip(w, m_w_hat, v_w_hat)]
            b_new = [bj - learning_rate * mb / ((vb)**0.5 + epsilon) for bj, mb, vb in zip(b, m_b_hat, v_b_hat)]
            state.update({"m_w": m_w, "v_w": v_w, "m_b": m_b, "v_b": v_b, "t": t + 1})
        else: raise ValueError("Optimizer '{}' tidak dikenali.".format(method))
        optimizer_result = (w_new, b_new, state)
    if labels is not None and task is None: # Task detection
        flat_labels = [y[0] if isinstance(y, list) else y for y in labels]
        task = "classification" if set(flat_labels) <= {0, 1} else "regression"
        logging.info("[Auto Task Detection] Task detection: {}".format(task))
    result = {}
    if not y_pred: raise ValueError("The model produces empty output.")
    if labels is None: result = {"output_mean": float(sum(y_pred) / len(y_pred))}
    elif task == "regression":
        mse = sum((yp - yt) ** 2 for yp, yt in zip(y_pred, labels)) / len(labels)
        mean_y = sum(labels) / len(labels)
        ss_tot = sum((yt - mean_y) ** 2 for yt in labels)
        ss_res = sum((yp - yt) ** 2 for yp, yt in zip(y_pred, labels))
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
        mean_err = sum(abs(yp - yt) for yp, yt in zip(y_pred, labels)) / len(labels)
        result.update({"mse": mse, "r2": r2, "mean_error": mean_err})
    elif task == "classification":
        y_class = [1 if (yp[0] if isinstance(yp, list) else yp) > threshold else 0 for yp in y_pred]
        tp = sum(1 for yc, yt in zip(y_class, labels) if yc == yt == 1)
        tn = sum(1 for yc, yt in zip(y_class, labels) if yc == yt == 0)
        fp = sum(1 for yc, yt in zip(y_class, labels) if yc == 1 and yt == 0)
        fn = sum(1 for yc, yt in zip(y_class, labels) if yc == 0 and yt == 1)
        accuracy = (tp + tn) / len(labels)
        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
        cm = [[tn, fp], [fn, tp]]
        report = {"0": {"precision": tn / (tn + fn) if (tn + fn) else 0.0, "recall": tn / (tn + fp) if (tn + fp) else 0.0},"1": {"precision": precision, "recall": recall}}
        result.update({"accuracy": accuracy, "precision": precision, "recall": recall, "f1_score": f1, "confusion_matrix": cm, "report": report})
    else: raise ValueError("task must be 'regression' or 'classification'")
    return (result, optimizer_result) if optimizer_result is not None else result

import gc
class DOMM:
    def __init__(self, mem_name="MODEL"):
        import collections
        self._cache = {}
        self._load_from_file = None
        self.base_name = mem_name
        self.dir_path = os.path.join(os.getcwd(), "models")
        os.makedirs(self.dir_path, exist_ok=True)

        # Path utama
        self.shelve_file = os.path.join(self.dir_path, self.base_name + ".db")
        self.json_file = os.path.join(self.dir_path, self.base_name + ".json")
        self.dm_file = os.path.join(self.dir_path, self.base_name + ".dm")

        # Inisialisasi database
        self.shelf = open(self.shelve_file, "a+", encoding="utf-8")
        self.shelf.seek(0)
        self._order = collections.deque(maxlen=1000)
        self.experiences = []
        if os.path.exists(self.json_file):
            with open(self.json_file, "r") as f:
                try: self.experiences = json.load(f)
                except: self.experiences = []

        # Buat file `.dm` kosong jika belum ada
        if not os.path.exists(self.dm_file):
            with open(self.dm_file, "w") as f: f.write(json.dumps({"MODEL": {}, "EXPERIENCE": []}, indent=4))

    def check_size(self):
        files = [self.shelve_file, self.json_file, self.dm_file]
        total = sum(os.path.getsize(f) for f in files if os.path.exists(f))
        return total <= 20 * 1024 * 1024

    def save_model(self, key, model_data):
        if not self.check_size(): raise Exception("Memory file size exceeds 20MB.")
        with open(self.shelve_file, "a", encoding="utf-8") as f: f.write("{}:{}\n".format(key,model_data))
        self._update_dm_file()

    # Load model dari DM 
    def load_model(self, key):
        def _load_from_file(key):
            try:
                with open(self.shelve_file, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("{}:".format(key)): return line.split(":", 1)[1].strip()
            except FileNotFoundError: return None
            return None
        if key in self._cache: return self._cache[key]
        value = _load_from_file(key) 
        if value is not None: self._cache[key] = value
        return value

    def delete_model(self, key):
        lines = []
        try:
            with open(self.shelve_file, "r", encoding="utf-8") as f: lines = f.readlines()
            with open(self.shelve_file, "w", encoding="utf-8") as f:
                for line in lines:
                    if not line.startswith("{}:".format(key)): f.write(line)
        except FileNotFoundError: pass
        self._cache.pop(key, None)
        self._update_dm_file()

    # Hapus semua model
    def clear(self):
        open(self.shelve_file, "w").close()
        self._cache.clear()
        gc.collect()
        self._update_dm_file()

    def add_experience(self, state, action, reward):
        if not self.check_size(): raise Exception("Memory file size exceeds 20MB.")
        exp = {"state": state, "action": action, "reward": reward}
        self.experiences.append(exp)
        if not os.path.exists(self.json_file): data = []
        else:
            with open(self.json_file, "r", encoding="utf-8") as f:
                try: data = json.load(f)
                except json.JSONDecodeError: data = []
        data.append(exp)

        # Tulis ulang file
        with open(self.json_file, "w", encoding="utf-8") as f: json.dump(data, f)
        self._update_dm_file()

    def search_experience(self, min_reward=0.0): return [exp for exp in self.experiences if exp["reward"] >= min_reward]

    # Hapus semua pengalaman
    def clear_experience(self):
        self.experiences = []
        with open(self.json_file, "w") as f: json.dump(self.experiences, f)
        gc.collect()
        self._update_dm_file()

    def _update_dm_file(self):
        os.makedirs(os.path.dirname(self.dm_file), exist_ok=True)
        def handler(obj):
            if isinstance(obj, (int, float, str, bool)) or obj is None: return obj
            if isinstance(obj, dict): return {k: handler(v) for k, v in obj.items()}
            if isinstance(obj, list): return [handler(x) for x in obj]
            return str(obj)
        dm_data = {"MODEL": {}, "EXPERIENCE": handler(self.experiences)}
        with open(self.dm_file, "w", encoding="utf-8") as f: json.dump(dm_data, f, indent=4, ensure_ascii=False)

    # Buat file .dm baru
    def create_dm(self, name):
        new_dm = os.path.join(self.dir_path, name + ".dm")
        if os.path.exists(new_dm): return "The .dm file already exists!"
        with open(new_dm, "w") as f: json.dump({"MODEL": {}, "EXPERIENCE": []}, f, indent=4)
        return "New .dm file successfully created: {}.dm".format(name)

    def close(self): open(self.shelve_file, "w").close() # Tutup database

class Adapter:
    @staticmethod
    def json(data):
        if isinstance(data, str): return json.loads(data)
        return json.dumps(data)

    @staticmethod
    def csv(data):
        import io, csv
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        if isinstance(data, list):
            for row in data: writer.writerow(row)
        return buffer.getvalue()

    @staticmethod
    def numpy(data):
        try:
            import numpy as np
            return np.array(data)
        except ImportError: return data

    @staticmethod
    def scipyspar(data):
        try:
            from scipy import sparse
            return sparse.csr_matrix(data)
        except ImportError: return data

    @staticmethod
    def pandas(data):
        try:
            import pandas as pd
            return pd.DataFrame(data)
        except ImportError: return data

    @staticmethod
    def polars(data):
        try:
            import polars as pl
            return pl.DataFrame(data)
        except ImportError: return data

    @staticmethod
    def pyarrow(data):
        try:
            import pyarrow as pa
            return pa.array(data)
        except ImportError: return data
        
    @staticmethod
    def pygame(data):
        try:
            import pygame
            return pygame
        except ImportError: return data

    @staticmethod
    def librosa(path):
        try:
            import librosa
            return librosa.load(path)
        except ImportError: return None

    @staticmethod
    def pillow(data):
        try:
            from PIL import Image
            return Image.open(data) if isinstance(data, str) else Image.fromarray(data)
        except ImportError: return data    

    class GPUD:
        '''GPUD is a subclass of Adapter that allows users to access the GPU.

        With the following functions:
        - gpu_info, to indicate the type of GPU available on your device.'''
        _opencl = None
        _cuda = None

        @staticmethod
        def _load_opencl():
            if Adapter.GPUD._opencl is not None: return Adapter.GPUD._opencl
            system = platform.system().lower()
            candidates = {"windows": ["OpenCL.dll"],
                        "darwin": ["/System/Library/Frameworks/OpenCL.framework/OpenCL"],
            }.get(system, ["libOpenCL.so", "libOpenCL.so.1",
                           "/usr/lib/x86_64-linux-gnu/libOpenCL.so.1"])
            for lib in candidates:
                try:
                    Adapter.GPUD._opencl = ctypes.CDLL(lib)
                    return Adapter.GPUD._opencl
                except Exception: pass
            return None

        @staticmethod
        def _load_cuda():
            if Adapter.GPUD._cuda is not None: return Adapter.GPUD._cuda
            system = platform.system().lower()
            name = "nvcuda.dll" if system == "windows" else "libcuda.so"
            try:
                Adapter.GPUD._cuda = ctypes.CDLL(name)
                return Adapter.GPUD._cuda
            except Exception: return None

        @staticmethod
        def gpu_available(): return bool(Adapter.GPUD._load_opencl() or Adapter.GPUD._load_cuda())

        @staticmethod
        def gpu_info():
            info = {"vendors": [], "devices": [], "api": {}}

            def haslib_osaware(name):
                try:
                    plat = sys.platform
                    if plat.startswith("win"):
                        if name == "cuda": return ctypes.util.find_library("nvcuda") is not None
                        if name == "vulkan": return ctypes.util.find_library("vulkan-1") is not None
                        return False
                    if plat.startswith("linux"):
                        if name == "rocm":
                            for lib in ("hsa-runtime64", "amdhip64", "hiprtc"):
                                if ctypes.util.find_library(lib):  return True
                            return False
                        return ctypes.util.find_library(name) is not None
                    return ctypes.util.find_library(name) is not None
                except Exception: return False

            vendors = devices = set()
            if haslib_osaware("cuda"):
                info["api"]["cuda"] = True
                vendors.add("NVIDIA")
            cl = Adapter.GPUD._load_opencl()
            if cl:
                try:
                    cl_uint = ctypes.c_uint
                    cl_ulong = ctypes.c_ulong
                    cl_size = ctypes.c_size_t
                    cl_platform_id = ctypes.c_void_p
                    cl_device_id = ctypes.c_void_p
                    CL_DEVICE_NAME = 0x102B
                    CL_DEVICE_VENDOR = 0x102C
                    CL_DEVICE_TYPE_GPU = 0x2
                    num_p = cl_uint()
                    cl.clGetPlatformIDs(0, None, ctypes.byref(num_p))
                    if num_p.value:
                        info["api"]["opencl"] = True
                        plats = (cl_platform_id * num_p.value)()
                        cl.clGetPlatformIDs(num_p.value, plats, None)
                        for p in plats:
                            num_d = cl_uint()
                            cl.clGetDeviceIDs(p, CL_DEVICE_TYPE_GPU, 0, None, ctypes.byref(num_d))
                            if not num_d.value: continue
                            devs = (cl_device_id * num_d.value)()
                            cl.clGetDeviceIDs(p, CL_DEVICE_TYPE_GPU, num_d.value, devs, None)
                            for d in devs:
                                size = cl_size()
                                cl.clGetDeviceInfo(d, CL_DEVICE_NAME, 0, None, ctypes.byref(size))
                                buf = ctypes.create_string_buffer(size.value)
                                cl.clGetDeviceInfo(d, CL_DEVICE_NAME, size, buf, None)
                                name = buf.value.decode(errors="ignore").strip()
                                if name: devices.add(name)
                                size = cl_size()
                                cl.clGetDeviceInfo(d, CL_DEVICE_VENDOR, 0, None, ctypes.byref(size))
                                buf = ctypes.create_string_buffer(size.value)
                                cl.clGetDeviceInfo(d, CL_DEVICE_VENDOR, size, buf, None)
                                vendor = buf.value.decode(errors="ignore").strip()
                                if vendor: vendors.add(vendor)
                except Exception: pass

            if haslib_osaware("vulkan"): info["api"]["vulkan"] = True 
            if haslib_osaware("hsa-runtime64"): 
                info["api"]["rocm"] = True
                vendors.add("AMD")
            if sys.platform == "darwin":
                info["api"]["metal"] = True
                vendors.add("Apple")
                if not devices: devices.add("Apple GPU")

            info["vendors"] = sorted(vendors)
            info["devices"] = sorted(devices)
            info["api"] = {k: True for k in info["api"]}
            return info

        @staticmethod
        def opencl_vector_add(a, b):
            import array
            cl = Adapter.GPUD._load_opencl()
            if cl is None: raise RuntimeError("OpenCL not available")
            clGetPlatformIDs = cl.clGetPlatformIDs
            clGetDeviceIDs = cl.clGetDeviceIDs
            clCreateContext = cl.clCreateContext
            clCreateCommandQueue = getattr(cl, "clCreateCommandQueue", None)  # old OpenCL 1.2
            clCreateBuffer = cl.clCreateBuffer
            clEnqueueWriteBuffer = cl.clEnqueueWriteBuffer
            clEnqueueReadBuffer = cl.clEnqueueReadBuffer
            clCreateProgramWithSource = cl.clCreateProgramWithSource
            clBuildProgram = cl.clBuildProgram
            clCreateKernel = cl.clCreateKernel
            clSetKernelArg = cl.clSetKernelArg
            clEnqueueNDRangeKernel = cl.clEnqueueNDRangeKernel
            cl_uint = ctypes.c_uint
            cl_platform_id = ctypes.c_void_p
            cl_device_id = ctypes.c_void_p
            cl_context = ctypes.c_void_p
            cl_command_queue = ctypes.c_void_p
            cl_mem = ctypes.c_void_p

            # Platform → Device
            num = cl_uint()
            clGetPlatformIDs(0, None, ctypes.byref(num))
            platforms = (cl_platform_id * num.value)()
            clGetPlatformIDs(num.value, platforms, None)
            device = cl_device_id()
            clGetDeviceIDs(platforms[0], 1, ctypes.byref(device), None)
            ctx = clCreateContext(None, 1, ctypes.byref(device), None, None, None) # Context
            queue = clCreateCommandQueue(ctx, device, 0, None) # Queue

            # Convert a,b → C float arrays
            a_arr = array.array("f", a)
            b_arr = array.array("f", b)
            n = len(a)

            # Buffer
            buf_a = clCreateBuffer(ctx, 1, a_arr.buffer_info()[1] * 4, None)
            buf_b = clCreateBuffer(ctx, 1, b_arr.buffer_info()[1] * 4, None)
            buf_out = clCreateBuffer(ctx, 1, a_arr.buffer_info()[1] * 4, None)

            # Write input → GPU
            clEnqueueWriteBuffer(queue, buf_a, True, 0, a_arr.buffer_info()[1] * 4, a_arr.buffer_info()[0], 0, None, None)
            clEnqueueWriteBuffer(queue, buf_b, True, 0, b_arr.buffer_info()[1] * 4, b_arr.buffer_info()[0], 0, None, None)

            # Kernel code
            kernel_src = b"""
            __kernel void vadd(__global const float* a, __global const float* b, __global float* out)
            {
                int i = get_global_id(0);
                out[i] = a[i] + b[i];
            }"""
            program = clCreateProgramWithSource(ctx, 1, ctypes.byref(ctypes.c_char_p(kernel_src)), None, None)
            clBuildProgram(program, 0, None, None, None, None)
            kernel = clCreateKernel(program, b"vadd", None)
            clSetKernelArg(kernel, 0, ctypes.sizeof(cl_mem), ctypes.byref(buf_a))
            clSetKernelArg(kernel, 1, ctypes.sizeof(cl_mem), ctypes.byref(buf_b))
            clSetKernelArg(kernel, 2, ctypes.sizeof(cl_mem), ctypes.byref(buf_out))
            # Run kernel
            global_size = (ctypes.c_size_t * 1)(n)
            clEnqueueNDRangeKernel(queue, kernel, 1, None, global_size, None, 0, None, None)
            # Read output
            out = array.array("f", [0] * n)
            clEnqueueReadBuffer(queue, buf_out, True, 0, out.buffer_info()[1] * 4, out.buffer_info()[0], 0, None, None)
            return list(out)

import math,random,logging,fractions
from dearning import cached
from multiprocessing import Pool,cpu_count

class Quan:
    """Quan is a tool function for"""
    @cached(staticmethod)
    def plus(a, b): return a + b
    @cached(staticmethod)
    def minus(a, b): return a - b
    @cached(staticmethod)
    def multiplication(a, b): return a * b
    @cached(staticmethod)
    def division(a, b): return a / b if b != 0 else None
    @cached(staticmethod)
    def squared(x): return x**2
    @cached(staticmethod)
    def root(x): return math.sqrt(x)
    @cached(staticmethod)
    def trigonometri(x): return {"sin": math.sin(x),"cos": math.cos(x),"tan": math.tan(x), "asin": math.asin(x),"acos": math.acos(x),"atan": math.atan(x)}
    @cached(staticmethod)
    def logeks(x, base=math.e): return {"log": math.log(x, base), "exp": math.exp(x)}
    @cached(staticmethod)
    def Tphytagoras(a, b, c=0): return math.sqrt(a**2 + b**2 + c**2)
    @cached(staticmethod)
    def matrix_mul(A, B):
        if not A or not B: raise ValueError("Matrix A and B cannot be empty")
        m = len(A[0])
        if not all(len(row) == m for row in A): raise ValueError("Matrix A is not rectangular")
        if not all(len(row) == len(B[0]) for row in B): raise ValueError("Matrix B is not rectangular")
        if m != len(B): raise ValueError("Dimensions are not suitable for matrix multiplication.")
        Bt = list(zip(*B))
        return [[sum(A[i][k] * Bt[j][k] for k in range(m)) for j in range(len(Bt))] for i in range(len(A))]
    @cached(staticmethod)
    def matrix_inv(A):
        from decimal import Decimal
        n = len(A)
        M, I = [[Decimal(x) for x in r] for r in A], [[Decimal(i == j) for i in range(n)] for j in range(n)] 
        for i in range(n):
            p = max(range(i, n), key=lambda r: abs(M[r][i]))
            if not M[p][i]: raise ValueError("Matriks singular")
            if p != i:
                M[i], M[p] = M[p], M[i]
                I[i], I[p] = I[p], I[i]
            piv = M[i][i]
            M[i] = [x / piv for x in M[i]]
            I[i] = [x / piv for x in I[i]]
            for k in range(n):
                if k != i:
                    f = M[k][i]
                    M[k], I[k] = [a - f*b for a, b in zip(M[k], M[i])], [a - f*b for a, b in zip(I[k], I[i])]
        return [[float(x) for x in r] for r in I]
    @cached(staticmethod)
    def statistics(data):
        d = sorted(data)
        n = len(d)
        m = sum(d) / n if n else 0.0
        return {"mean": m,
                "median": d[n//2] if n%2 else (d[n//2-1]+d[n//2])/2 if n else 0.0,
                "stdev": (sum((x-m)**2 for x in d)/n)**0.5 if n else 0.0}
    @cached(staticmethod)
    def probability(event, sample): return fractions(event, sample)
    @cached(staticmethod)
    def derivative(f, x, h=1e-5): return (f(x + h) - f(x - h)) / (2 * h)
    @cached(staticmethod)
    def integral(f, a, b, n=1000):
        dx = (b - a) / n
        return sum(f(a + i*dx) * dx for i in range(n))
    @cached(staticmethod)
    def ratio(a, b): return fractions(a, b)
    # Absolute Quan additions
    @cached(staticmethod)
    def Erelatif(m_vector, c: float = 299792458.0): return m_vector * c**2 if isinstance(m_vector, (int, float)) else [float(m) * c**2 for m in m_vector]
    @cached(staticmethod)
    def Efoton(f_vector, h: float = 6.62607015e-34): return float(h) * f_vector if isinstance(f_vector, (int, float)) else [float(h) * float(f) for f in f_vector]
    @cached(staticmethod)
    def compress_array(x, M=None):
        eps = 1e-12
        arr = [float(x)] if isinstance(x, (int, float)) else [float(v) for v in x]
        if M is None:
            if not arr: M = 1.0
            else:
                cr = sorted(abs(v) for v in arr)
                n = len(cr)
                mid = n // 2
                M = (cr[mid] if n & 1 else (cr[mid-1] + cr[mid]) * 0.5) + eps
                M = max(M, eps)
        res = [math.copysign(math.log1p(abs(v) / M), v) for v in arr]
        return res[0] if len(res) == 1 else res
    @cached(staticmethod)
    def build_C_vector(N, T_vals=None, P3_vals=None, L_vals=None, M_vals=None, GeomAlg_vals=None, S_vals=None, Calc_vals=None, B_vals=None, fallback_random=False):
        def _safe_vec(v, N):
            if v is None: return [0.0] * N
            if isinstance(v, (int, float)): return [float(v)] * N
            v = list(map(float, v))
            lv = len(v)
            if lv == 0: return []
            if lv < N:
                full_repeats, remainder = divmod(N, lv)
                return v * full_repeats + v[:remainder]
            return v[:N]
        rand = [random.gauss(0, 1) for _ in range(N)] if fallback_random else [0.0] * N
        T = _safe_vec(T_vals, N)
        P3 = _safe_vec(P3_vals, N)
        L = _safe_vec(L_vals, N)
        M_ = _safe_vec(M_vals, N)
        GeomAlg = _safe_vec(GeomAlg_vals, N)
        S = _safe_vec(S_vals, N)
        Calc = _safe_vec(Calc_vals, N)
        B = _safe_vec(B_vals, N)
        return [complex(val, 0.0) for val in Quan.compress_array([T[i] + P3[i] + L[i] + M_[i] + GeomAlg[i] + S[i] + Calc[i] + B[i] + rand[i] for i in range(N)])]
    @cached(staticmethod)
    def build_H_eff(E_rel_vec, E_ph_vec, interaction_matrix=None, coupling_scale=1e-6, cutoff=None):
        E_rel, E_ph = list(map(float, E_rel_vec)), list(map(float, E_ph_vec)) 
        N = len(E_rel)
        H = [[complex((E_rel[i] + E_ph[i]) if i == j else 0.0, 0.0) for j in range(N)] for i in range(N)]
        if interaction_matrix is None: return H
        rows = len(interaction_matrix)
        cols = len(interaction_matrix[0]) if rows else 0
        cs = float(coupling_scale)
        cut = float(cutoff) if cutoff is not None else None
        for i in range(min(N, rows)):
            Ai = interaction_matrix[i]
            Hi = H[i]
            for j in range(min(N, cols)):
                v = float(Ai[j])
                if cut is None or abs(v) >= cut: Hi[j] += complex(v * cs, 0.0)
        return H
    @cached(staticmethod)
    def expm_apply(H, state, steps=20):
        N = len(state)
        Hc = [[(H[i][j] + H[j][i].conjugate()) / 2 for j in range(N)] for i in range(N)]
        A0 = [[1j * Hc[i][j] for j in range(N)] for i in range(N)]
        def matmul(A, B): return [[sum(A[i][k] * B[k][j] for k in range(N)) for j in range(N)] for i in range(N)]
        def matvec(A, v): return [sum(A[i][k] * v[k] for k in range(N)) for i in range(N)]
        normA = max(abs(v) for row in A0 for v in row)
        s = int(math.log2(normA)) if normA > 0 else 0
        A = [[v / (2 ** s) for v in row] for row in A0]
        I = [[1+0j if i == j else 0j for j in range(N)] for i in range(N)]
        U = term = [row[:] for row in I]
        fact = 1
        for k in range(1, steps + 1):
            term = matmul(term, A)
            fact *= k
            for i in range(N):
                for j in range(N): U[i][j] += term[i][j] / fact
        for _ in range(s): U = matmul(U, U)
        return matvec(U, state)
    @cached(staticmethod)
    def expm_diag(matrix): return [[complex(math.e) ** (-1j * matrix[i][i]) if i == j else 0j for j in range(len(matrix))] for i in range(len(matrix))]
    @cached(staticmethod)
    def qft(state):
        N, norm, tau = len(state), 1 / math.sqrt(N), 2 * math.pi / N 
        return [sum(state[n] * complex(math.cos(tau * k * n), math.sin(tau * k * n))for n in range(N)) * norm for k in range(N)]
    @staticmethod
    def variational_layer(state, phase_params=None):
        N = len(state)
        if phase_params is None: phase = [random.gauss(0.0, 0.01) for _ in range(N)]
        elif isinstance(phase_params, (int, float)): phase = [float(phase_params)] * N
        else: phase = [float(phase_params[i % len(phase_params)]) for i in range(N)]
        return [amp * complex(math.cos(theta), math.sin(theta)) for amp, theta in zip(state, phase)]
    @cached(staticmethod)
    def normalize(state, eps=1e-12):
        s = 0.0
        for x in state: s += (x.real * x.real + x.imag * x.imag)
        norm = math.sqrt(s)
        if norm <= eps: return state
        inv = 1.0 / norm
        return [x * inv for x in state]
    @staticmethod
    def measure_topk(state, top_k=5):
        probs = [abs(x)**2 for x in state]
        n, total = len(probs), sum(probs) 
        probs = ([1.0/n]*n if total <= 0 else [p/total for p in probs])
        return [(i, float(p)) for i, p in sorted(enumerate(probs), key=lambda t: t[1], reverse=True)[:top_k]]
    @cached(staticmethod)
    def fft(x):
        N = len(x)
        if N == 0: return x
        if N & (N - 1) != 0: raise ValueError("A radix-2 FFT requires a power-of-two data length")
        j = 0
        for i in range(1, N):
            bit = N >> 1
            while j & bit:
                j ^= bit
                bit >>= 1
            j |= bit
            if i < j: x[i], x[j] = x[j], x[i]
        m = 2
        while m <= N:
            ang = -2 * math.pi / m
            wm = complex(math.cos(ang), math.sin(ang))
            for k in range(0, N, m):
                w = 1+0j
                half = m >> 1
                for j in range(half):
                    a, b = x[k + j], w * x[k + j + half]
                    x[k + j], x[k + j + half] = a + b, a - b
                    w *= wm
            m <<= 1
        return x
    @cached(staticmethod)
    def linspace(start, stop, num): return [start + i * (stop - start)/(num - 1) for i in range(num)] if num > 1 else [start]
    @cached(staticmethod)
    def mean(vec): return sum(vec) / len(vec) if vec else 0.0

_log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class Quantum:
    """Quantum is a function for performing quantum calculations.

    with the following functions:
    - initialize,
    - kron,
    - apply_gate,
    - hadamard,
    - (pauli_x, pauli_y, pauli_z),
    - cnot,
    - measure,
    - evolve_absolute,
    - grover
    - shor,
    - qfts,
    - vqe,
    - qaoa,"""
    def __init__(self, qubit_size=4, n_cores=2, seed=None, use_absolute=True):
        self.qubit_size = int(qubit_size)
        self.state = self.initialize()  
        self.gates = []
        self.entangled_pairs = []
        self.n_cores = max(1, min(int(n_cores), cpu_count()))
        self._rng = random.Random(seed)
        self._pool = None
        self.debug_compact = True
        self._damping = 0.995
        self.use_absolute = bool(use_absolute)
        import atexit
        atexit.register(self.close_pool)
    def __getitem__(self, index):
        if isinstance(self.state, (list, tuple)): return self.state[index]
        raise TypeError("Quantum state is not indexable")
    def __setitem__(self, index, value):
        if isinstance(self.state, list): self.state[index] = value
        else: raise TypeError("Quantum state is not mutable or not a list")
    def initialize(self):
        n = 1 << self.qubit_size
        state = [0+0j] * n
        state[0] = 1+0j
        return state
    @cached(staticmethod)
    def kron(A, B): return ([a * b for a in rowA for b in rowB] for rowA in A for rowB in B)
    @cached(staticmethod)
    def matvec(A_flat, v_real, v_imag, n, m):
        out_r = out_i = [0.0] * n
        for i in range(n):
            sumr = sumi = 0.0
            base = i * m
            for k in range(m):
                ar = A_flat[base + k]
                vr, vi = v_real[k], v_imag[k]
                sumr += ar * vr
                sumi += ar * vi
            out_r[i], out_i[i] = sumr, sumi
        return out_r, out_i
    def apply_gate(self, gate, qubit_index, damping=1.0): # gate: [[g00,g01],[g10,g11]] each complex (tuple of (r,i) or complex)
        n = 1 << self.qubit_size
        stride = 1 << qubit_index
        # derive real and imag arrays from self.state to avoid relying on missing attributes
        real, imag = [val.real for val in self.state], [val.imag for val in self.state]
        g00 = complex(gate[0][0]); g01 = complex(gate[0][1])
        g10 = complex(gate[1][0]); g11 = complex(gate[1][1])
        for base in range(0, n, 2*stride):
            for i in range(base, base + stride):
                ar = real[i]; ai = imag[i]
                br = real[i + stride]; bi = imag[i + stride]
                # compute a' = g00*a + g01*b
                a_pr = (g00.real*ar - g00.imag*ai) + (g01.real*br - g01.imag*bi)
                a_pi = (g00.real*ai + g00.imag*ar) + (g01.real*bi + g01.imag*br)
                # compute b' = g10*a + g11*b
                b_pr = (g10.real*ar - g10.imag*ai) + (g11.real*br - g11.imag*bi)
                b_pi = (g10.real*ai + g10.imag*ar) + (g11.real*bi + g11.imag*br)
                # damping and assign
                real[i], imag[i] = a_pr * damping, a_pi * damping
                real[i + stride], imag[i + stride] = b_pr * damping, b_pi * damping
        self.state = [complex(r, im) for r, im in zip(real, imag)] # update self.state with new complex amplitudes
    @cached()
    def hadamard(self, index):
        H = [[1, 1], [1, -1]]
        H = [[x / math.sqrt(2) for x in row] for row in H]
        self.apply_gate(H, index)
    @cached()
    def pauli_x(self, index):
        X = [[0, 1], [1, 0]]
        self.apply_gate(X, index)
    @cached()
    def pauli_y(self, index):
        Y = [[0, -1j], [1j, 0]]
        self.apply_gate(Y, index)
    @cached()
    def pauli_z(self, index):
        Z = [[1, 0], [0, -1]]
        self.apply_gate(Z, index)
    @cached(staticmethod)
    def cnot(state, control, target):
        for i in range(len(state)):
            if (i >> control) & 1:
                j = i ^ (1 << target)  # flip target bit
                if i < j: state[i], state[j] = state[j], state[i] # swap amplitudes 
    @cached()
    def entangle(self, q1, q2):
        pair = (int(q1), int(q2))
        if pair not in self.entangled_pairs: self.entangled_pairs.append(pair)
    def measure(self, top_k=5):
        probs = [abs(x)**2 for x in self.state]
        total = sum(probs)
        n = len(probs)
        probs = ([1.0 / n] * n) if total <= 0 else [p / total for p in probs]
        idx = random.choices(range(n), weights=probs, k=1)[0]
        result = list(format(idx, "0{}b".format(self.qubit_size)))
        if self.entangled_pairs:
            for a, b in self.entangled_pairs: result[b] = result[a]
        result = "".join(result)
        k = min(int(top_k), n)
        top_k_list = sorted(enumerate(probs), key=lambda x: x[1], reverse=True)[:k]
        mean = sum(probs) / n
        sorted_p = sorted(probs)
        mid = n // 2
        median = sorted_p[mid] if n & 1 else (sorted_p[mid - 1] + sorted_p[mid]) / 2.0
        stdev = (sum((x - mean) ** 2 for x in probs) / n) ** 0.5 if n > 1 else 0.0
        return {"result": result,
                "probabilities": list(map(float, probs)),
                "top_k": [(i, float(p)) for i, p in top_k_list],
                "total_prob_sum": float(total),
                "stats": {"mean": float(mean), "median": float(median), "stdev": float(stdev)}}
    @staticmethod
    def _worker_update_seeded(seed, state_chunk, factor, damping):
        rng = random.Random(seed)
        std = 0.001 * max(1.0, abs(factor))
        return [(val * factor + (math.sqrt(-2.0 * math.log(u1)) * math.cos(2 * math.pi * u2)) * std) * damping for val, u1, u2 in ((v, rng.random(), rng.random()) for v in state_chunk)]
    def unstable_multiprocessing_update(self, factor: float = 1.0):
        if not self.state: return
        n_cores = max(1, min(2, int(self.n_cores)))
        # manual array split
        chunk_size = max(1, len(self.state) // n_cores)
        chunks = [self.state[i:i + chunk_size] for i in range(0, len(self.state), chunk_size)]
        seeds = [self._rng.randint(0, 2**31 - 1) for _ in chunks]
        args = [(s, c, float(factor), float(self._damping)) for s, c in zip(seeds, chunks)]
        if self._pool is None:
            import os
            os.environ.setdefault("OMP_NUM_THREADS", "1")
            self._pool = Pool(processes=n_cores, maxtasksperchild=200)
        results = self._pool.starmap(Quantum._worker_update_seeded, args)
        self.state = [x for sub in results for x in sub]
        # normalize vector (l2 norm)
        norm_val = math.sqrt(sum(abs(x) ** 2 for x in self.state))
        if norm_val > 0: self.state = [x / norm_val for x in self.state]
    @cached()
    def helper_memory(self, enable_trace = True, compress = True):
        import gc, weakref, tracemalloc
        gc.collect()
        state_ref = weakref.ref(self.state)
        if compress and self.state is not None: self.state = [complex(float(val.real), float(val.imag)) for val in self.state]
        snapshot_info = None
        if enable_trace:
            try:
                tracemalloc.start()
                snapshot = tracemalloc.take_snapshot()
                top_stats = snapshot.statistics("lineno")
                snapshot_info = [(str(stat.traceback[0]), stat.size / 1024) for stat in top_stats[:5]]
                tracemalloc.stop()
            except Exception: snapshot_info = None
        return {"state_ref_alive": state_ref() is not None, "dtype": "complex (python built-in)",
                "length": len(self.state), "snapshot": snapshot_info}
    @cached()
    def evolve_absolute(self, m_vec=None, f_vec=None, coupling_scale=1e-3, dt=0.1, apply_qft=True, apply_variational=True, phase_params=None, compress_M=None, eps_regularizer=None):
        N = len(self.state)
        m_vec = [0.0] * N if m_vec is None else m_vec
        f_vec = [0.0] * N if f_vec is None else f_vec
        H_mass = [m_vec[i] for i in range(N)] # Mass term: diagonal matrix
        H_force = [float(f) for f in f_vec]   # diagonal external field term
        H = [[0.0]*N for _ in range(N)]
        for i in range(N):
            H[i][i] = H_mass[i] + H_force[i]
            if i+1 < N:
                c = coupling_scale * (m_vec[i] - m_vec[i+1])
                H[i][i+1] = H[i+1][i] = c
        new_state = [0]*N
        for i in range(N):
            acc = 0j
            for j in range(N): acc += self.state[j] * complex(math.cos(-H[i][j]*dt), math.sin(-H[i][j]*dt))
            new_state[i] = acc
        self.state = new_state
        if apply_qft: # optional
            psi = Quan.fft(self.state)
            self.state = [val / math.sqrt(N) for val in psi]
        if apply_variational:
            theta = float(phase_params or 0.2)
            self.state = [val * complex(math.cos(theta), math.sin(theta)) for val in self.state]
        real_part = [val.real for val in self.state]
        compressed = Quan.compress_array(real_part, M=compress_M)
        expanded = (compressed * (N // len(compressed) + 1))[:N]
        # Combine magnitude + original phase
        phases = [math.atan2(val.imag, val.real) for val in self.state]
        self.state = [expanded[i] * complex(math.cos(phases[i]), math.sin(phases[i])) for i in range(N)]
        if eps_regularizer is None: eps_regularizer = max(1e-12, 1e-12 * math.sqrt(N))
        self.state = Quan.normalize(self.state, eps_regularizer)
        return self.state
    def grover(self, oracle_mask_or_fn):
        N = len(self.state)
        if N == 0: return None
        # interpret oracle
        if callable(oracle_mask_or_fn):
            res = oracle_mask_or_fn(self.state)
            if hasattr(res, "__iter__"): mask = [bool(x) for x in res]
            elif isinstance(res, bool): mask = [res] * N
            elif isinstance(res, int):
                mask = [False] * N
                mask[res % N] = True
            else: raise TypeError("Callable oracle must return iterable/bool/int")
        else:
            if hasattr(oracle_mask_or_fn, "__iter__"): mask = [bool(x) for x in oracle_mask_or_fn]
            else: raise TypeError("oracle_mask_or_fn harus fungsi atau iterable")
        # H⊗n applied to state vector = multiply each amplitude by 1/sqrt(N)
        inv = 1.0 / math.sqrt(N)
        self.state = [val * inv for val in self.state]
        # Grover iterations 
        iters = int(math.floor((math.pi / 4.0) * math.sqrt(N)))
        for _ in range(iters):
            # Oracle: phase flip
            for i in range(N):
                if mask[i]: self.state[i] = -self.state[i]
            # Diffuser (inversion around mean) 
            self.state = [(2.0 * (sum(self.state) / float(N)) - amp) for amp in self.state]
        return self.measure()
    @cached()
    def shor(self, n): return "Factoring {} (simulated)".format(n)
    @cached()
    def qfts(self):
        s = 0.0
        self.state = [x / math.sqrt(len(self.state)) for x in Quan.fft(self.state)]
        for x in self.state: s += (x.real * x.real + x.imag * x.imag)
        norm = math.sqrt(s)
        if norm > 1e-12:
            inv = 1.0 / norm
            self.state = [x * inv for x in self.state]
        return self.measure()
    def vqe(self, cost_function, iterations=20, lr=0.1):
        theta = random.random()
        loss = None
        state = self.state
        def apply_ry(st, t):
            c, s = math.cos(t * 0.5), math.sin(t * 0.5)
            return [complex(a.real*c - a.imag*s, a.real*s + a.imag*c) for a in st]
        def numerical_grad(t, eps=1e-4): return (cost_function(apply_ry(state, t + eps)) - cost_function(apply_ry(state, t - eps))) / (2.0 * eps)
        for i in range(int(iterations)):
            state = apply_ry(state, theta)
            self.state = state
            loss = float(cost_function(state))
            grad = numerical_grad(theta)
            theta -= lr * grad
            if self.debug_compact: _log.info("[VQE] iter={}/{} loss={:.6f} theta={:.4f} grad={:.4f}".format(i + 1, iterations, loss, theta, grad))
        return {"state": state, "loss": loss, "theta": theta}
    def qaoa(self, hamiltonian, iterations: int = 10):
        N = len(self.state)
        for i in range(int(iterations)):
            try: # simple exponentiation of diagonal Hamiltonian
                U = Quan.expm_diag(hamiltonian)
                self.state = [sum(U_row[j] * self.state[j] for j in range(N)) for U_row in U]
            except Exception:
                mean_diag = sum(hamiltonian[i][i] for i in range(N)) / N
                self.state = [val * complex(-1j * mean_diag) for val in self.state]
            # simulasi unstable update
            self.state = [val * 0.99 for val in self.state]
        return self.measure()

    def debug_state(self, top_n: int = 5):
        meas = self.measure(top_k=top_n)
        _log.info(" Quantum State Summary:")
        _log.info(" bitstring (sampled) : {}".format(meas['result']))
        _log.info(" top_{} : {}".format(top_n, meas['top_k']))
        stats = meas.get("stats", {})
        _log.info(" probs mean/median/stdev : {:.6e} / {:.6e} / {:.6e}".format(stats.get('mean'),stats.get('median'),stats.get('stdev')))
        _log.info(" gates applied count : {}".format(len(self.gates)))
        _log.info(" entangled pairs : {}".format(self.entangled_pairs))

    def compact_summary(self, top_n: int = 5):
        meas = self.measure(top_k=top_n)
        return {"sampled_bitstring": meas["result"], "top_k": meas["top_k"], "stats": meas["stats"],
                "gates_applied": len(self.gates), "entangled_pairs": list(self.entangled_pairs)}
    def close_pool(self):
        pool = getattr(self, "_pool", None)
        if pool is not None:
            try:
                close_fn = getattr(pool, "close", None)
                if callable(close_fn): close_fn()
                join_fn = getattr(pool, "join", None)
                if callable(join_fn): join_fn()
            except Exception: pass
            finally: self._pool = None
    @cached()
    def reset(self):
        self.state = self.initialize()
        self.gates.clear()
        self.entangled_pairs.clear()
    @cached()
    def summary(self):
        state_norm = math.sqrt(sum(abs(x)**2 for x in self.state))
        return {"qubit_size": self.qubit_size, "gates_applied": len(self.gates),
                "entangled_pairs": list(self.entangled_pairs), "state_norm": float(state_norm)}

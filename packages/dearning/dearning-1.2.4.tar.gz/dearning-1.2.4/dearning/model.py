from __future__ import division, print_function, absolute_import
import math,random

class DOtensor(object):
    """DOtensor is a function for 1D grad (after all, it's called Dearning Of tensor, abbreviated as DOtensor).

    with the following functions:
    - backward, automatic gradient propagation
    - zero_grad, to reset the gradient
    - trace, to trace code"""
    __slots__ = ("data","grad","requires_grad","_backward","_prev")
    _global_trace_enabled = False
    _global_trace_log = []
    def __init__(self, data, requires_grad=False):
        if isinstance(data, DOtensor): data = data.data
        if isinstance(data, (int, float)): self.data = [float(data)]
        else: self.data = [float(x) for x in data]
        self.requires_grad = requires_grad
        self.grad = [0.0]*len(self.data) if requires_grad else None
        self._prev = ()
        self._backward = None

    @classmethod
    def trace(cls, enabled=True):
        """trace is a function for tracing tensor code (you probably already know this, as the name suggests). This function can be turned on or off as desired.

        example:
        >>> with DOtensor.trace(enabled=True) as log:
        >>>     a = DOtensor([1.0, 2.0], requires_grad=True)
        >>>     b = DOtensor([3.0, 4.0], requires_grad=True)
        >>>     c = a * b
        >>>     d = c.DTS()
        >>>     d.backward()
        >>> for entry in log: print(entry)"""
        class _TraceContext:
            def __enter__(self_inner):
                cls._prev_trace_state = cls._global_trace_enabled
                cls._global_trace_enabled = enabled
                if enabled: cls._global_trace_log = []
                return cls._global_trace_log

            def __exit__(self_inner, exc_type, exc, tb): cls._global_trace_enabled = cls._prev_trace_state
        return _TraceContext()

    def __add__(self, other):
        other = other if isinstance(other, DOtensor) else DOtensor([other])
        if len(self.data) != len(other.data):
            raise ValueError("DOtensor: shape mismatch {} vs {}".format(len(self.data), len(other.data)))
        def backward(self):
            if not self.requires_grad: return
        out = DOtensor([a+b for a,b in zip(self.data, other.data)], requires_grad=self.requires_grad or other.requires_grad)
        if out.requires_grad:
            def _backward():
                if out.grad is None: return
                if self.requires_grad:
                    for i in range(len(self.grad)): self.grad[i] += out.grad[i]
                if other.requires_grad:
                    for i in range(len(other.grad)): other.grad[i] += out.grad[i]
            out._backward = _backward
            out._prev = (self, other)
        if DOtensor._global_trace_enabled:DOtensor._global_trace_log.append(("add", repr(self), repr(other), repr(out)))
        return out
    
    def __mul__(self, other):
        other = other if isinstance(other, DOtensor) else DOtensor([other])
        if len(self.data) != len(other.data):
            raise ValueError("DOtensor: shape mismatch {} vs {}".format(len(self.data), len(other.data)))
        def backward(self):
            if not self.requires_grad: return
        out = DOtensor([a*b for a,b in zip(self.data, other.data)], requires_grad=self.requires_grad or other.requires_grad)
        if out.requires_grad:
            def _backward():
                if out.grad is None: return
                if self.requires_grad:
                    for i in range(len(self.grad)): self.grad[i] += other.data[i] * out.grad[i]
                if other.requires_grad:
                    for i in range(len(other.grad)): other.grad[i] += self.data[i] * out.grad[i]
            out._backward = _backward
            out._prev = (self, other)
        if DOtensor._global_trace_enabled:DOtensor._global_trace_log.append(("mul", repr(self), repr(other), repr(out)))
        return out
    
    def __sub__(self, other):
        other = other if isinstance(other, DOtensor) else DOtensor([other])
        return self + (-other)

    def __neg__(self):
        out = DOtensor([-x for x in self.data], self.requires_grad)
        if self.requires_grad:
            def _backward():
                for i in range(len(self.data)): self.grad[i] += -out.grad[0]
            out._backward = _backward
            out._prev = (self,)
        return out
    
    def DTS(self):
        """DTS (Dearning Tensor Sum) is a function that sums all tensor elements into a single scalar.

        Example:
        >>> from dearning import DOtensor
        >>> x = DOtensor([2.0, 3.0], requires_grad=True)
        >>> y = DOtensor([4.0, 5.0], requires_grad=True)
        >>> z = x * y + x
        >>> s = z.DTS()"""
        out = DOtensor([sum(self.data)], self.requires_grad)
        if self.requires_grad:
            def _backward():
                for i in range(len(self.data)): self.grad[i] += out.grad[0]
            out._backward = _backward
            out._prev = (self,)
        return out

    def backward(self):
        """Backward is a function that performs backward propagation on a computational graph.

        Example:
        >>> from dearning import DOtensor
        >>> x = DOtensor([2.0, 3.0], requires_grad=True)
        >>> y = DOtensor([4.0, 5.0], requires_grad=True)
        >>> z = x * y + x
        >>> s = z.DTS()
        >>> s.backward()
        Must be called on a scalar tensor (the final result)."""
        topo = []
        visited = set()
        def build(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev: build(child)
                topo.append(v)
        build(self)
        self.grad = [1.0]
        for node in reversed(topo):
            if node._backward: node._backward()
        if DOtensor._global_trace_enabled: DOtensor._global_trace_log.append(("backward", repr(self)))

    def zero_grad(self):
        """zero_grad is a function to reset grad.

        example:
        >>> from dearning import DOtensor
        >>> x = DOtensor([2.0, 3.0], requires_grad=True)
        >>> y = DOtensor([4.0, 5.0], requires_grad=True)
        >>> x.zero_grad()
        >>> y.zero_grad()
        >>> print("x.grad:", x.grad)
        >>> print("y.grad:", y.grad)"""
        visited = set()
        def reset(v):
            if v not in visited:
                visited.add(v)
                if v.requires_grad: v.grad = [0.0] * len(v.data)
                for p in v._prev: reset(p)
        reset(self)

    def __hash__(self): return id(self)
    def __repr__(self): return "DOtensor(data={}, grad={})".format(self.data,self.grad)

class Dense:
    """Dense is a function for a fully connected (linear) neural network layer."""
    def __init__(self, input_dim, output_dim):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.weights = [[random.gauss(0, 1) * math.sqrt(2.0 / input_dim) for _ in range(output_dim)] for _ in range(input_dim)]
        self.bias = [0.0] * output_dim

    def forward(self, X, training=True):
        if not X or len(X[0]) != self.input_dim: raise ValueError("Expected input_dim={}, got {}".format(self.input_dim, len(X[0]) if X else None))
        self.input = X
        return [[sum(x[i] * self.weights[i][j] for i in range(self.input_dim)) + self.bias[j] for j in range(self.output_dim)] for x in X]

    def backward(self, grad_output):
        B = len(grad_output)
        self.grad_w = [[0.0]*self.output_dim for _ in range(self.input_dim)]
        self.grad_b = [0.0]*self.output_dim
        grad_in = [[0.0]*self.input_dim for _ in range(B)]
        for b in range(B):
            for j in range(self.output_dim):
                self.grad_b[j] += grad_output[b][j]
                for i in range(self.input_dim):
                    self.grad_w[i][j] += self.input[b][i] * grad_output[b][j]
                    grad_in[b][i] += self.weights[i][j] * grad_output[b][j]
        return grad_in

    def update(self, lr):
        for i in range(self.input_dim):
            for j in range(self.output_dim): self.weights[i][j] -= lr * self.grad_w[i][j]
        for j in range(self.output_dim): self.bias[j] -= lr * self.grad_b[j]

class Activation:
    """Activation is a function for the activation layer for relu, sigmoid, and tanh."""
    def __init__(self, kind="relu"): self.kind = kind

    def forward(self, x, training=True):
        self.input = x
        if self.kind == "relu": self.output = [[max(0.0, v) for v in row] for row in x]
        elif self.kind == "sigmoid": self.output = [[1.0/(1.0+math.exp(-v)) for v in row] for row in x]
        elif self.kind == "tanh": self.output = [[math.tanh(v) for v in row] for row in x]
        else: raise ValueError("Unknown activation")
        return self.output

    def backward(self, grad_output):
        if self.kind == "relu": return [[g if o > 0 else 0.0 for g, o in zip(gr, orow)] for gr, orow in zip(grad_output, self.output)]
        if self.kind == "sigmoid": return [[g * o * (1-o) for g, o in zip(gr, orow)] for gr, orow in zip(grad_output, self.output)]
        if self.kind == "tanh": return [[g * (1-o*o) for g, o in zip(gr, orow)] for gr, orow in zip(grad_output, self.output)]

    def update(self, lr): pass

class Dropout:
    """"""
    def __init__(self, rate=0.5): self.rate = rate

    def forward(self, x, training=True):
        if not training: return x
        self.mask = [[1.0 if random.random() > self.rate else 0.0 for _ in row] for row in x]
        return [[v*m for v,m in zip(row, mrow)] for row, mrow in zip(x, self.mask)]

    def backward(self, grad_output):
        return [[g*m for g,m in zip(row, mrow)] for row, mrow in zip(grad_output, self.mask)]

    def update(self, lr): pass

class CustomAIModel:
    """"""
    def __init__(self, loss="mse"):
        self.layers = []
        self.loss = loss
        self.memory_neuron = None
        self.expert_neurons = []

    def add(self, layer):
        """add is a function to add layers to the model.
        
        example:
        >>> from dearning import CustomAIModel, Dense
        >>> model = CustomAIModel(loss="mse")
        >>> model.add(Dense(1, 1))"""
        self.layers.append(layer)

    def forward(self, x):
        for layer in self.layers: x = layer.forward(x)
        return x

    def seed(self, n): random.seed(n)

    def _loss(self, y_pred, y_true):
        total = 0.0
        if self.loss == "mse":
            for yp_row, yt_row in zip(y_pred, y_true):
                for yp, yt in zip(yp_row, yt_row):
                    diff = yp - yt
                    total += diff * diff
            return total
        elif self.loss == "cross_entropy":
            epsilon = 1e-8
            for yp_row, yt_row in zip(y_pred, y_true):
                for yp, yt in zip(yp_row, yt_row):
                    yp = min(max(yp, epsilon), 1.0 - epsilon)
                    total += -(yt * math.log(yp) + (1 - yt) * math.log(1 - yp))
            return total
        return 0.0

    def _loss_grad(self, y_pred, y_true):
        n = sum(len(row) for row in y_true)
        if self.loss == "mse": return [[2 * (yp - yt) / n for yp, yt in zip(yp_row, yt_row)] for yp_row, yt_row in zip(y_pred, y_true)]
        elif self.loss == "cross_entropy": return [[(yp - yt) / n for yp, yt in zip(yp_row, yt_row)] for yp_row, yt_row in zip(y_pred, y_true)]
        return 0.0
    
    def zero_grad(self):
        for layer in self.layers:
            if hasattr(layer, "grad_w"):
                for i in range(len(layer.grad_w)):
                    for j in range(len(layer.grad_w[i])): layer.grad_w[i][j] = 0.0
            if hasattr(layer, "grad_b"): layer.grad_b = [0.0]*len(layer.grad_b)

    def backward(self, grad):
        """backward is a function to run backward propagation on all layers.
        
        example:
        >>> from dearning import CustomAIModel, Dense
        >>> model = CustomAIModel(loss="mse")
        >>> model.add(Dense(1, 1))
        >>> # after forward pass and loss computation
        >>> grad = model._loss_grad(y_pred, y_true)
        >>> model.zero_grad()
        >>> model.backward(grad)"""
        for layer in reversed(self.layers):
            if hasattr(layer, "backward"): grad = layer.backward(grad)
        return grad

    def step(self, lr):
        """step is a function to update all model parameters using a certain learning rate.
        
        example:
        >>> from dearning import CustomAIModel, Dense
        >>> model = CustomAIModel(loss="mse")
        >>> model.add(Dense(1, 1))
        >>> # after backward pass
        >>> lr = 0.1
        >>> model.step(lr)"""
        for layer in self.layers:
            if hasattr(layer, "update"): layer.update(lr)

    def train(self, X, y, epochs=100, learning_rate=0.1, batch_size=None, task=None):
        for _ in range(epochs):
            y_pred = self.forward(X)
            loss = self._loss(y_pred, y)
            grad = self._loss_grad(y_pred, y)
            self.zero_grad()
            self.backward(grad)
            self.step(learning_rate)
        return loss

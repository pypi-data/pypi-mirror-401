import math,random

class datal:
    """datal is a function for creating data that is immediately ready for use.

    with functions
    - load, creating random data
    - loader, dividing data
    - transform, making data more informative, rich in patterns, and other things"""
    from typing import List
    def load(task="classification", n_samples=500, n_features=4):
        """load is a function for creating random data for regression or classification.
        
        example:
        """
        if task == "classification":
            X = [[random.gauss(0, 1) for _ in range(n_features)] for _ in range(n_samples)]
            y = [[1 if sum(v > 0 for v in row) > (n_features >> 1) else 0] for row in X]
        elif task == "regression":
            X = [[random.gauss(0, 2) for _ in range(n_features)] for _ in range(n_samples)]
            y = [[sum(row) + random.gauss(0, 0.5)] for row in X]
        else: raise ValueError("Task must be classification or regression")
        X_t = list(zip(*X))
        means = [sum(col) / len(col) for col in X_t]
        stdevs = [math.sqrt(sum((x - m) ** 2 for x in col) / len(col)) or 1.0 for m, col in zip(means, X_t)]
        return [[(v - means[i]) / stdevs[i] for i, v in enumerate(row)] for row in X], y
    @staticmethod
    def loader(X, y, batch=32, shuffle=True):
        """loader is a function that yields data in batches."""
        indices = list(range(len(X)))
        if shuffle: random.shuffle(indices)
        for i in range(0, len(indices), batch):
            batch_idx = indices[i:i+batch]
            yield ([X[j] for j in batch_idx],[y[j] for j in batch_idx])
    @staticmethod
    def transform(X: List[List[float]]) -> List[List[float]]:
        """
        
        example:
        >>> from dearning import datal
        >>> X = [[1.0, 2.0, 3.0], [0.5, 1.5, 2.5]]
        >>> print(datal.transform(X))"""
        if not X: return X
        X_log = [[math.log(max(x, 1e-8)) for x in row] for row in X]
        X_exp = [[math.exp(x) for x in row] for row in X]
        n_features = len(X[0]) if X else 0
        mat = [[sum(row[i] * row[j] for row in X) for j in range(n_features)] for i in range(n_features)]
        max_val = max(abs(v) for row in mat for v in row) or 1.0
        mat_avg = [[v / max_val for v in row] for row in mat]
        X_matrixed = [[sum(x * mat_avg[k][j] for k, x in enumerate(row)) for j in range(n_features)] for row in X]
        return [[(a + b + c) / 3.0 for a, b, c in zip(r_log, r_exp, r_lin)] for r_log, r_exp, r_lin in zip(X_log, X_exp, X_matrixed)]

def train(models, X, y, *, task=None, epochs=100, lr=0.01, batch_size=None, detail=False, log_interval=1):
    """train is a function used to train an AI model using regression or classification.

    example
    -
    regression:
    >>> from dearning import CustomAIModel, Dense, train
    >>> X = [[1.0], [2.0], [3.0], [4.0]]
    >>> y = [[5.0], [6.0], [7.0], [8.0]]
    >>> model = CustomAIModel(loss="mse")
    >>> model.add(Dense(1, 1))
    >>> print(train(model, X, y, task="regression", epochs=100, lr=0.1, detail=True))
    >>> test_X = [[5.0]]
    >>> print("prediction:", model.forward(test_X))

    classification:
    >>> # Data: AND gate
    >>> X = [[0.0, 0.0],[0.0, 1.0],[1.0, 0.0],[1.0, 1.0]]
    >>> y = [[0.0],[0.0],[0.0],[1.0]]
    >>> model = CustomAIModel(loss="cross_entropy")
    >>> model.add(Dense(2, 1))
    >>> model.add(Activation("sigmoid"))
    >>> print(train(model, X, y, task="classification", epochs=100, lr=0.1, detail=True))
    >>> for x in X: # inference
    >>> p = model.forward([x])[0][0]
    >>> print(x, "→", 1 if p >= 0.5 else 0, "(prob:", p, ")")"""
    import threading, time
    if not isinstance(models, (list, tuple)): models = [models]
    results = [None] * len(models)
    lock = threading.Lock()
    def _accuracy(y_pred, y_true):
        correct = total = 0
        for yp, yt in zip(y_pred, y_true):
            p = max(range(len(yp)), key=lambda i: yp[i]) if len(yp) > 1 else int(yp[0] >= 0.5)
            t = max(range(len(yt)), key=lambda i: yt[i]) if len(yt) > 1 else int(yt[0] >= 0.5)
            correct += (p == t)
            total += 1
        return correct / total if total else 0.0

    def run(model, idx):
        name = getattr(model, "name", "model_%d" % idx)
        start = time.time()
        for ep in range(epochs):
            model.train(X, y, epochs=1, learning_rate=lr, batch_size=batch_size, task=task)
            if detail and ((ep + 1) % log_interval == 0 or (ep + 1) == epochs):
                y_pred = model.forward(X)
                loss = model._loss(y_pred, y) if hasattr(model, "_loss") else None
                if task == "classification":
                    acc = _accuracy(y_pred, y)
                    print("epoch {}, {} | loss {:.6f} | acc {:.4f}".format(ep + 1, name, loss, acc))
                elif task == "regression": print("epoch {}, {} | loss {:.6f}".format(ep + 1, name, loss))
        dur = time.time() - start
        y_pred = model.forward(X)
        loss = model._loss(y_pred, y) if hasattr(model, "_loss") else None
        acc = None
        if task == "classification": acc = _accuracy(y_pred, y)
        with lock: 
            if task == "regression": results[idx] = {"model": name, "loss": loss, "duration": dur}
            elif task == "classification": results[idx] = {"model": name, "loss": loss, "accuracy": acc, "duration": dur}
    threads = []
    for i, m in enumerate(models):
        t = threading.Thread(target=run, args=(m, i))
        t.start()
        threads.append(t)
    for t in threads: t.join()
    if not detail:
        for r in results:
            if r["accuracy"] is None: print(r["model"], "loss:", r["loss"], "duration:", r["duration"])
            else: print(r["model"], "loss:", r["loss"], "accuracy:", r["accuracy"], "duration:", r["duration"])
    return results
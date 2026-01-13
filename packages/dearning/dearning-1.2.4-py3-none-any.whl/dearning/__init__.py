import builtins
from typing import TYPE_CHECKING

setattr(builtins, "__dafe_protect__", True) # Protection

def _lazy_func(module_name, class_name):
    import importlib
    class _LazyMeta(type):
        def __getattr__(cls, attr):
            mod = importlib.import_module(module_name)
            real = getattr(mod, class_name)
            return getattr(real, attr)
    class _LazyClass(metaclass=_LazyMeta):
        __name__ = class_name
        __module__ = module_name
        def __new__(cls, *args, **kwargs):
            mod = importlib.import_module(module_name)
            real = getattr(mod, class_name)
            return real(*args, **kwargs)
    try:
        mod = importlib.import_module(module_name)
        real = getattr(mod, class_name)
        _LazyClass.__doc__ = real.__doc__
    except Exception: pass
    return _LazyClass

if TYPE_CHECKING: from dearning.model import CustomAIModel, DOtensor, Dense, Activation, Dropout
else:
    CustomAIModel = _lazy_func("dearning.model", "CustomAIModel")
    DOtensor = _lazy_func("dearning.model", "DOtensor")
    Dense = _lazy_func("dearning.model", "Dense")
    Activation = _lazy_func("dearning.model", "Activation")
    Dropout = _lazy_func("dearning.model", "Dropout")
if TYPE_CHECKING: from dearning.utils import cached, preprocess_data, evaluate_model, Adapter, DOMM
else:
    cached = _lazy_func("dearning.utils", "cached")
    preprocess_data = _lazy_func("dearning.utils", "preprocess_data")
    evaluate_model = _lazy_func("dearning.utils", "evaluate_model")
    Adapter = _lazy_func("dearning.utils", "Adapter")
    DOMM = _lazy_func("dearning.utils", "DOMM")
if TYPE_CHECKING: from dearning.training import train, datal
else:
    train = _lazy_func("dearning.training", "train")
    datal = _lazy_func("dearning.training", "datal")
if TYPE_CHECKING: from dearning.AI_tools import DLP, RLTools, image, video, Qkanalyze
else:
    DLP = _lazy_func("dearning.AI_tools", "DLP")
    AImemory = _lazy_func("dearning.AI_tools", "AImemory")
    TTS = _lazy_func("dearning.AI_tools", "TTS")
    RLTools = _lazy_func("dearning.AI_tools", "RLTools")
    audio = _lazy_func("dearning.AI_tools", "audio")
    image = _lazy_func("dearning.AI_tools", "image")
    video = _lazy_func("dearning.AI_tools", "video")
    Qkanalyze = _lazy_func("dearning.AI_tools", "Qkanalyze")
if TYPE_CHECKING: from dearning.AI_core import Converter
else: Converter = _lazy_func("dearning.AI_core", "Converter")
if TYPE_CHECKING: from dearning.Quantum import Quantum, Quan
else:
    Quantum = _lazy_func("dearning.Quantum", "Quantum")
    Quan = _lazy_func("dearning.Quantum", "Quan")
if TYPE_CHECKING: from dearning.service import load, post, run_server, DGS
else:
    load = _lazy_func("dearning.service", "load")
    post = _lazy_func("dearning.service", "post")
    run_server = _lazy_func("dearning.service", "run_server")
    DGS = _lazy_func("dearning.service", "DGS")

__all__ = ["CustomAIModel", "DOtensor", "cached", "post", "load", "DGS", "Adapter", "DOMM", "datal", "DLP", "AImemory", "Dense", "Activation", "Dropout", "Converter",
            "RLTools", "image", "video", "Qkanalyze", "Quantum", "run_server", "Quan", "preprocess_data", "evaluate_model", "train"] 
globals().update({name: globals()[name] for name in __all__})

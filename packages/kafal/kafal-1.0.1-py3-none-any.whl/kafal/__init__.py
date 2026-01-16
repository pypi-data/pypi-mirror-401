from .core.interpreter import KafalInterpreter

# Backwards-compat alias for older imports
FlowScriptInterpreter = KafalInterpreter

__all__ = ["KafalInterpreter", "FlowScriptInterpreter"]
__version__ = "0.1.0"

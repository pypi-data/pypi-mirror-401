"""denobox - Execute JavaScript and WebAssembly in a Deno sandbox from Python."""

from .async_box import AsyncDenobox, AsyncWasmModule
from .sync_box import Denobox, DenoboxError, WasmModule

__all__ = [
    "Denobox",
    "AsyncDenobox",
    "DenoboxError",
    "WasmModule",
    "AsyncWasmModule",
]
__version__ = "0.1.0"

# Backward compatibility aliases (undocumented)
DenoBox = Denobox
AsyncDenoBox = AsyncDenobox
DenoBoxError = DenoboxError

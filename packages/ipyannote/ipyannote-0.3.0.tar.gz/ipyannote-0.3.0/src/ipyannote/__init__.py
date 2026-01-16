import importlib.metadata

from .blocks.controls import Controls
from .blocks.labels import Labels
from .blocks.waveform import Waveform
from .blocks.htranscript import HTranscript
from .blocks.vtranscript import VTranscript

from .apps.annotation import IAnnotation

try:
    __version__ = importlib.metadata.version("ipyannote")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


__all__ = [
    "Waveform",
    "Labels",
    "Controls",
    "HTranscript",
    "VTranscript",
    "IAnnotation",
]

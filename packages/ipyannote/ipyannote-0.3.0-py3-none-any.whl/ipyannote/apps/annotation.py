from ipywidgets import HBox, VBox
from pyannote.core import Annotation

from ..blocks.controls import Controls
from ..blocks.labels import Labels
from ..blocks.waveform import Waveform

from ..utils.sync import js_sync

class IAnnotation(VBox):
    """Interactive annotation viewer

    Parameters
    ----------
    audio : str
        Path to audio file.
    annotation : Annotation or list of dict, optional
        Annotation to display on top of the waveform. If list of dict is provided,
        each dict must have keys: 'start', 'end', 'label' and optionally 'id'.
    labels : Labels, optional
        Labels widget to use for managing segment labels.
    """
    def __init__(
        self,
        audio: str,
        annotation: Annotation | list[dict] | None = None,
        labels: Labels | None = None,
    ):
        self._labels = labels or Labels()
        self._waveform = Waveform(
            audio=audio, annotation=annotation, labels=self._labels
        )
        self._controls = Controls()
        js_sync(self._controls, self._waveform, ["current_time", "playing"])
        super().__init__([self._waveform, HBox([self._controls, self._labels])])

    @property
    def annotation(self) -> Annotation:
        return self._waveform.annotation

    @annotation.setter
    def annotation(self, annotation: Annotation | list[dict]):
        self._waveform.annotation = annotation

    @annotation.deleter
    def annotation(self):
        del self._waveform.annotation

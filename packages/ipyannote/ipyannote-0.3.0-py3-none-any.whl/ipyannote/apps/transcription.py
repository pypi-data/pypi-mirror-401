from ipywidgets import HBox, VBox
from pyannote.core import Annotation

from ..blocks.controls import Controls
from ..blocks.htranscript import HTranscript
from ..blocks.labels import Labels
from ..blocks.waveform import Waveform

from ..utils.sync import js_sync


class ITranscription(VBox):
    """Interactive transcription viewer"""

    def __init__(
        self,
        audio: str,
        transcription: list[dict],
        diarization: Annotation | list[dict] | None = None,
        labels: Labels | None = None,
    ):
        self._labels = labels or Labels({"N/A": "#808080"})

        if diarization is None:
            diarization = transcription

        self._diarization = Waveform(
            audio=audio, annotation=diarization, labels=self._labels
        )
        self._transcript = HTranscript(transcript=transcription, labels=self._labels)

        self._controls = Controls()

        js_sync(self._controls, self._diarization, ["current_time"])
        js_sync(self._controls, self._transcript, ["current_time"])

        super().__init__(
            [
                self._diarization,
                self._transcript,
                HBox([self._controls, self._labels]),
            ]
        )

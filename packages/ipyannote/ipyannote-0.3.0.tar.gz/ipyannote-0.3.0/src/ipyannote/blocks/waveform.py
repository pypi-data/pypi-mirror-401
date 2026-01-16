import base64
import io
from pathlib import Path

import anywidget
import numpy as np
import scipy.io.wavfile
from pyannote.core import Annotation, Segment
from traitlets import Bool, Dict, Float, List, Unicode

from ..utils.sync import js_sync
from .labels import Labels

try:
    import torchcodec
except ImportError:
    torchcodec = None


class Waveform(anywidget.AnyWidget):
    """Display audio waveform with annotation

    Parameters
    ----------
    audio : str, optional
        Path to audio file.
    annotation : Annotation or list of dict, optional
        Annotation to display on top of the waveform. If list of dict is provided,
        each dict must have keys: 'start', 'end', 'label' and optionally 'id'.
    labels : Labels, optional
        Labels widget to use for managing segment labels.
    """

    _esm = Path(__file__).parent.parent / "static" / "waveform.js"
    _css = Path(__file__).parent.parent / "static" / "waveform.css"

    # used to pass audio to the frontend
    audio_as_base64 = Unicode().tag(sync=True)

    # used to synchronize pool of labels
    labels = Dict(key_trait=Unicode(), value_trait=Unicode()).tag(sync=True)
    active_label = Unicode(None, allow_none=True).tag(sync=True)

    # used to synchronize players
    current_time = Float(0.0).tag(sync=True)
    scroll_time = Float(0.0).tag(sync=True)
    zoom = Float().tag(sync=True)

    playing = Bool(False).tag(sync=True)

    # list of segments
    segments = List(
        Dict(
            per_key_traits={
                "start": Float(),
                "end": Float(),
                "label": Unicode(),
                "id": Unicode(),
                "active": Bool(),
            }
        )
    ).tag(sync=True)

    active_segment = Unicode(None, allow_none=True).tag(sync=True)

    def __init__(
        self,
        audio: str | None = None,
        annotation: Annotation | list[dict] | None = None,
        labels: Labels | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self._labels = labels or Labels()
        js_sync(self._labels, self, ["labels", "active_label"])

        if audio is not None:
            self.audio = audio

        if annotation is not None:
            self.annotation = annotation

    @staticmethod
    def to_base64(waveform: np.ndarray, sample_rate: int) -> str:
        with io.BytesIO() as content:
            scipy.io.wavfile.write(content, sample_rate, waveform)
            content.seek(0)
            b64 = base64.b64encode(content.read()).decode()
            b64 = f"data:audio/x-wav;base64,{b64}"
        return b64

    @property
    def audio(self) -> str:
        raise NotImplementedError("This is a write-only property")

    @audio.setter
    def audio(self, audio: str):
        # reset annotation when audio changes
        del self.annotation

        try:
            sample_rate, waveform = scipy.io.wavfile.read(audio)
        except ValueError:
            if torchcodec is None:
                raise ValueError(
                    "Please install torchcodec to load audio files other than WAV."
                )
            else:
                waveform, sample_rate = torchcodec.load(audio)
                waveform = waveform.numpy().T

        waveform = waveform.astype(np.float32)
        waveform /= np.max(np.abs(waveform)) + 1e-8
        self.audio_as_base64 = self.to_base64(waveform, sample_rate)

    @audio.deleter
    def audio(self):
        # reset annotation when audio changes
        del self.annotation

        sample_rate = 16000
        waveform = np.zeros((sample_rate,), dtype=np.float32)
        self.audio_as_base64 = self.to_base64(waveform, sample_rate)

    @property
    def annotation(self) -> Annotation:
        annotation = Annotation()
        for region in self.segments:
            segment = Segment(region["start"], region["end"])
            annotation[segment, region["id"]] = region["label"]
        return annotation

    @annotation.setter
    def annotation(self, annotation: Annotation | list[dict]):
        regions = []

        if annotation is None:
            regions = []

        elif isinstance(annotation, list):
            for r, region in enumerate(annotation):
                regions.append(
                    {
                        "start": region["start"],
                        "end": region["end"],
                        "id": region.get("id", f"segment-{r}"),
                        "label": region.get("label", region.get("speaker", "N/A")),
                        "active": False,
                    }
                )

        elif isinstance(annotation, Annotation):
            for segment, track_id, label in annotation.rename_tracks(
                "string"
            ).itertracks(yield_label=True):
                regions.append(
                    {
                        "start": segment.start,
                        "end": segment.end,
                        "id": track_id,
                        "label": label,
                        "active": False,
                    }
                )

        else:
            raise ValueError(
                "`annotation` must be either a pyannote.core.Annotation instance or a list of dicts"
            )

        # ensure that all labels are registered in self._labels before updating self.segments
        # (syncing happens only once **after** exiting hold_sync context manager)
        with self._labels.hold_sync():
            for region in regions:
                _ = self._labels[region["label"]]

        self.segments = regions

    @annotation.deleter
    def annotation(self):
        self.segments = []

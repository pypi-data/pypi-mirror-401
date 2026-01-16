from pathlib import Path

import anywidget
from traitlets import Dict, Float, List, Unicode

from ..utils.sync import js_sync
from .labels import Labels


class VTranscript(anywidget.AnyWidget):
    """Display transcript segments in a vertical layout.

    Parameters
    ----------
    transcript : list of dict
        List of segments with keys: 'start', 'end', 'speaker', 'text'
    labels : Labels, optional
        Labels widget to use for managing speaker labels.
    height : str, optional
        Height of the widget. Defaults to '200px'.
    """

    _esm = Path(__file__).parent.parent / "static" / "vtranscript.js"
    _css = Path(__file__).parent.parent / "static" / "vtranscript.css"

    transcript = List(
        Dict(
            per_key_traits={
                "start": Float(),
                "end": Float(),
                "speaker": Unicode(),
                "text": Unicode(),
            }
        )
    ).tag(sync=True)

    labels = Dict(key_trait=Unicode(), value_trait=Unicode()).tag(sync=True)

    current_time = Float(0.0).tag(sync=True)

    height = Unicode("200px").tag(sync=True)

    def __init__(
        self,
        transcript: list[dict],
        labels: Labels | None = None,
        height="200px",
    ):
        super().__init__()

        self._labels = labels or Labels()
        js_sync(self._labels, self, ["labels"])

        # ensure that all labels are registered in self._labels before updating self.transcript
        # (syncing happens only once **after** exiting hold_sync context manager)
        with self._labels.hold_sync():
            for line in transcript:
                speaker = line.get("label", line.get("speaker", "N/A"))
                _ = self._labels[speaker]

        self.transcript = transcript
        self.height = height

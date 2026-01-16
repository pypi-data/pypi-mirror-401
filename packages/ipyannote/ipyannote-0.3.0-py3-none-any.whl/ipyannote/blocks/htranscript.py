from pathlib import Path

import anywidget
from traitlets import Dict, Enum, Float, List, Unicode

from ..utils.sync import js_sync
from .labels import Labels


class HTranscript(anywidget.AnyWidget):
    """Display transcript segments in a horizontal layout.

    Parameters
    ----------
    transcript : list of dict
        List of segments with keys: 'start', 'end', 'speaker', 'text'
    labels : Labels, optional
        Labels widget to use for managing speaker labels.
    width : str, optional
        Width of the widget.
        Defaults to take 100% of the available space.
    """

    _esm = Path(__file__).parent.parent / "static" / "htranscript.js"
    _css = Path(__file__).parent.parent / "static" / "htranscript.css"

    transcript = List(
        Dict(
            per_key_traits={
                "start": Float(),
                "end": Float(),
                "speaker": Unicode(),
                "text": Unicode(),
                "status": Enum(
                    ["insertion", "deletion", "substitution", "correct"],
                    default_value="correct",
                ),
                "source": Enum(["N/A", "reference", "hypothesis"], default_value="N/A"),
            }
        )
    ).tag(sync=True)

    labels = Dict(key_trait=Unicode(), value_trait=Unicode()).tag(sync=True)

    current_time = Float(0.0).tag(sync=True)
    scroll_left = Float(0.0).tag(sync=True)

    width = Unicode("100%").tag(sync=True)

    def __init__(
        self,
        transcript: list[dict],
        labels: Labels | None = None,
        width: str = "100%",
    ):
        super().__init__()

        self._labels = labels or Labels({'N/A': '#808080'})
        js_sync(self._labels, self, ["labels"])

        # ensure that all labels are registered in self._labels before updating self.transcript
        # (syncing happens only once **after** exiting hold_sync context manager)
        with self._labels.hold_sync():
            for line in transcript:
                speaker = line.get("speaker", "N/A")
                _ = self._labels[speaker]

        self.transcript = transcript
        self.width = width

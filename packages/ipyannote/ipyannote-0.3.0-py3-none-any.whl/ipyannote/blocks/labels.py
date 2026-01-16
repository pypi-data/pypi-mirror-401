import itertools
from pathlib import Path

import anywidget
from traitlets import Dict, Unicode


class Labels(anywidget.AnyWidget):
    _esm = Path(__file__).parent.parent / "static" / "labels.js"
    _css = Path(__file__).parent.parent / "static" / "labels.css"

    labels = Dict(key_trait=Unicode(), value_trait=Unicode()).tag(sync=True)
    active_label = Unicode(None, allow_none=True).tag(sync=True)

    def __init__(self, labels: dict[str, str] | None = None):
        super().__init__()
        self._colors = itertools.cycle(
            [
                "#ffd700",
                "#00ffff",
                "#ff00ff",
                "#00ff00",
                "#9932cc",
                "#00bfff",
                "#ff7f50",
                "#66cdaa",
            ]
        )

        if labels:
            self.labels = labels

    # return label color
    def __getitem__(self, label: str) -> str:
        if label in self.labels:
            return self.labels[label]

        labels = dict(self.labels)  # copy existing labels
        color = next(self._colors)
        labels[label] = color
        self.labels = labels  # trigger traitlets sync
        return color

    def __setitem__(self, label: str, color: str):
        labels = dict(self.labels)  # copy existing labels
        labels[label] = color
        self.labels = labels  # trigger traitlets sync

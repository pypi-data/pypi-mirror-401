from pathlib import Path

import anywidget
from traitlets import Bool, Float


class Controls(anywidget.AnyWidget):
    _esm = Path(__file__).parent.parent / "static" / "controls.js"
    _css = Path(__file__).parent.parent / "static" / "controls.css"

    current_time = Float(0.0).tag(sync=True)
    playing = Bool(False).tag(sync=True)

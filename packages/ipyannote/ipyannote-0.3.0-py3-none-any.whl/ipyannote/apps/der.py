from ipywidgets import HBox, VBox
from pyannote.core import Annotation
from pyannote.metrics.diarization import DiarizationErrorRate
from pyannote.metrics.errors.identification import IdentificationErrorAnalysis

from ..blocks.controls import Controls
from ..blocks.labels import Labels
from ..blocks.waveform import Waveform
from ..utils.sync import js_sync


class IDiarizationErrorRate(VBox):
    def __init__(
        self,
        audio: str,
        reference: Annotation,
        hypothesis: Annotation,
        permutation_invariant: bool = False,
    ):
        self.permutation_invariant = permutation_invariant

        # common set of speaker labels
        self._labels_speaker = Labels()

        # reference and hypothesis waveforms...
        self._waveform_reference = Waveform(audio=audio, labels=self._labels_speaker)
        self._waveform_hypothesis = Waveform(audio=audio, labels=self._labels_speaker)

        # set of error labels
        self._labels_diff = Labels(
            {
                "false alarm": "#00ff00",
                "missed detection": "#ffa500",
                "confusion": "#ff0000",
            }
        )

        # create (empty) error waveform...
        self._waveform_diff = Waveform(audio=audio, labels=self._labels_diff)

        # .controls
        self._controls = Controls()

        js_sync(self._controls, self._waveform_reference, ["current_time", "playing"])
        js_sync(self._controls, self._waveform_hypothesis, ["current_time", "playing"])
        js_sync(self._controls, self._waveform_diff, ["current_time", "playing"])
        js_sync(
            self._waveform_reference, self._waveform_hypothesis, ["zoom", "scroll_time"]
        )
        js_sync(
            self._waveform_reference, self._waveform_diff, ["zoom", "scroll_time"]
        )

        super().__init__(
            [
                self._labels_speaker,
                self._waveform_reference,
                self._waveform_hypothesis,
                self._waveform_diff,
                HBox([self._controls, self._labels_diff]),
            ]
        )

        if self.permutation_invariant:
            # map hypothesis labels to reference labels...
            _hypothesis = self._match_speakers(reference, hypothesis)
        else:
            _hypothesis = hypothesis
        # ... and compute errors
        errors = self._compute_errors(reference, _hypothesis)

        # populate reference, hypothesis and errors waveforms
        self._waveform_reference.annotation = reference
        self._waveform_hypothesis.annotation = _hypothesis
        self._waveform_diff.annotation = errors

    def _match_speakers(
        self, reference: Annotation, hypothesis: Annotation
    ) -> Annotation:
        mapping = {label: f"@{label}" for label in hypothesis.labels()}
        hypothesis = hypothesis.rename_labels(mapping)

        optimal_mapping = DiarizationErrorRate().optimal_mapping
        mapping = optimal_mapping(reference, hypothesis)
        mapped_hypothesis = hypothesis.rename_labels(mapping)
        return mapped_hypothesis

    def _compute_errors(
        self, reference: Annotation, mapped_hypothesis: Annotation
    ) -> Annotation:
        errors: Annotation = (
            IdentificationErrorAnalysis()
            .difference(reference, mapped_hypothesis)
            .support()
        )

        # only keep error types
        mapping = {error: error[0] for error in errors.labels()}
        errors = errors.rename_labels(mapping).subset(["correct"], invert=True)
        return errors.rename_tracks()

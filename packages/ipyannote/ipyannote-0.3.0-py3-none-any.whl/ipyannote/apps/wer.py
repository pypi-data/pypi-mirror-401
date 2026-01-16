from ipywidgets import HBox, VBox, HTML

try:
    from meeteval.io.seglst import SegLST, SegLstSegment
    from meeteval.viz.visualize import get_visualization_data

    MEETEVAL_AVAILABLE = True
except ImportError:
    MEETEVAL_AVAILABLE = False
    raise ImportError(
        "Please install ipyannote with 'wer' extra to use IWordErrorRate. "
        "For example: uv add --extra wer ipyannote. "
    )

from ..blocks.controls import Controls
from ..blocks.htranscript import HTranscript
from ..blocks.labels import Labels
from ..blocks.waveform import Waveform
from ..utils.sync import js_sync


# Alignment variants supported by meeteval
# ALIGNMENT = [
#     "cp",
#     "tcp",
#     "tcorc",
#     "greedy_tcorc",
#     "greedy_ditcp",
#     "orc",
#     "greedy_orc",
#     "greedy_dicp",
# ]


class IWordErrorRate(VBox):
    """Interactive Word Error Rate (WER) viewer

    Parameters
    ----------
    audio : str
        Path to audio file.
    reference : list of dict
        Reference transcription as list of segments with keys: 
        'start', 'end', 'speaker', 'text'
    hypothesis : list of dict
        Hypothesis transcription as list of segments with keys: 
        'start', 'end', 'speaker', 'text'
    variant : str, optional
        Alignment variant to use. Must be one of orc, tcorc, cp, or tcp. 
        Defaults to orc.
    """
    def __init__(
        self,
        audio: str,
        reference: list[dict],
        hypothesis: list[dict],
        variant: str = "orc",
    ):
        self.variant = variant
        self._waveform = Waveform(audio=audio)
        self._controls = Controls()

        reference, hypothesis, wer = self._align(reference, hypothesis)

        self._labels_speaker = Labels({"N/A": "#808080"})
        self._htranscript_reference = HTranscript(
            transcript=reference, labels=self._labels_speaker
        )
        self._htranscript_hypothesis = HTranscript(
            transcript=hypothesis, labels=self._labels_speaker
        )

        insertions: str = f"{wer['insertions']} insertion" + (
            "s" if wer["insertions"] > 1 else ""
        )
        deletions: str = f"{wer['deletions']} deletion" + (
            "s" if wer["deletions"] > 1 else ""
        )
        substitutions: str = f"{wer['substitutions']} substitution" + (
            "s" if wer["substitutions"] > 1 else ""
        )

        super().__init__(
            [
                HTML(f"<b>{self.variant}-WER: {wer['error_rate']*100:.1f}% ({insertions}, {deletions}, {substitutions})</b>"),
                self._waveform,
                self._htranscript_reference,
                self._htranscript_hypothesis,
                HBox([self._controls, self._labels_speaker]),
            ]
        )

        js_sync(self._controls, self._waveform, ["current_time", "playing"])
        js_sync(self._controls, self._htranscript_reference, ["current_time"])
        js_sync(self._controls, self._htranscript_hypothesis, ["current_time"])
        js_sync(
            self._htranscript_reference, self._htranscript_hypothesis, ["scroll_left"]
        )

    def _to_meeteval(self, transcription: list[dict]) -> SegLST:
        """Convert specified transcription to meeteval format

        Parameters
        ----------
        transcription: list[dict]
            List of transcription's segments

        Returns
        -------
        meeteval_transcript: SegLST
            Transcription at meeteval format.
        """
        return SegLST(
            segments=[
                SegLstSegment(
                    session_id="",
                    start_time=entry["start"],
                    end_time=entry["end"],
                    words=entry["text"],
                    speaker=entry["speaker"],
                    segment_index=e,
                )
                for e, entry in enumerate(transcription)
            ]
        )

    def _align(
        self, reference: list[dict], hypothesis: list[dict]
    ) -> tuple[list[dict], list[dict], dict]:
        self._data = get_visualization_data(
            self._to_meeteval(reference),
            self._to_meeteval(hypothesis),
            assignment=self.variant,
        )

        wer = {
            key: self._data["info"]["wer"][key]
            for key in [
                "error_rate",
                "length",
                "insertions",
                "deletions",
                "substitutions",
            ]
        }

        alignment = [
            dict(zip(self._data["words"], t))
            for t in zip(*self._data["words"].values())
        ]

        STATUS = {
            "c": "correct",
            "d": "deletion",
            "i": "insertion",
            "s": "substitution",
        }

        SOURCE = {"r": "reference", "h": "hypothesis"}

        r = [[] for _ in alignment]
        h = [[] for _ in alignment]
        for word in alignment:
            (matched_idx, status), *_ = word["matches"]
            idx = word["utterance_index"]
            text = word["words"]
            start_time = word["start_time"]
            end_time = start_time + word["duration"]
            speaker = word["speaker"]
            source = word["source"]

            entry = {
                "text": text,
                "speaker": speaker,
                "start": start_time,
                "end": end_time,
                "status": STATUS[status],
                "source": SOURCE[source],
            }

            if source == "r":
                if status == "d":
                    r[idx].append(entry)
                    h[idx].append(dict(entry, source="hypothesis", text="\u00A0" * len(entry["text"])))
                elif status == "s":
                    matched_text = alignment[matched_idx]["words"]
                    r[idx].append(
                        dict(
                            entry,
                            text=text + "\u00A0" * max(0, len(matched_text) - len(text)),
                        )
                    )
                else:
                    r[idx].append(entry)
                continue

            if status == "c":
                h[matched_idx].append(entry)

            elif status == "s":
                matched_text = alignment[matched_idx]["words"]
                h[matched_idx].append(
                    dict(entry, source="reference", text=text + "\u00A0" * max(0, len(matched_text) - len(text)))
                )

            elif status == "i":
                h[idx].append(entry)
                r[idx].append(dict(entry, source="reference", text="\u00A0" * len(entry["text"])))

        return (
            sorted(
                [word for utterance in r for word in utterance],
                key=lambda w: w["start"],
            ),
            sorted(
                [word for utterance in h for word in utterance],
                key=lambda w: w["start"],
            ),
            wer
        )

"""Generate per-segment narration audio with espeak-ng (offline TTS).

For every segment in ``narration.SEGMENTS`` this writes a WAV file and records
its exact duration (in seconds) into ``output/durations.json``. The Manim scene
reads that file so each animation is timed to match its narration.

espeak-ng is used because it works fully offline. Higher-quality engines
(gTTS / Piper neural voices) need network hosts that are not reachable from
this environment, so we fall back to a clear, tuned espeak-ng voice.
"""

import json
import os
import subprocess
import wave

from narration import SEGMENTS

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
AUDIO_DIR = os.path.join(OUT, "audio")

# espeak-ng voice tuning for clarity: US English, a relaxed pace, slightly
# lowered pitch, and a small inter-word gap so sentences are easy to follow.
VOICE = "en-us"
SPEED = "150"   # words per minute
PITCH = "42"
AMP = "160"
GAP = "4"       # 10ms units of pause between words


def wav_duration(path: str) -> float:
    with wave.open(path, "rb") as w:
        return w.getnframes() / float(w.getframerate())


def main() -> None:
    os.makedirs(AUDIO_DIR, exist_ok=True)
    durations = {}

    for seg in SEGMENTS:
        sid = seg["id"]
        wav_path = os.path.join(AUDIO_DIR, f"{sid}.wav")
        subprocess.run(
            [
                "espeak-ng",
                "-v", VOICE,
                "-s", SPEED,
                "-p", PITCH,
                "-a", AMP,
                "-g", GAP,
                "-w", wav_path,
                seg["text"],
            ],
            check=True,
        )
        dur = wav_duration(wav_path)
        # A little breathing room after each line keeps the pacing natural.
        durations[sid] = round(dur + 0.6, 3)
        print(f"  {sid}: {durations[sid]}s  ({wav_path})")

    with open(os.path.join(OUT, "durations.json"), "w") as f:
        json.dump(durations, f, indent=2)

    total = sum(durations.values())
    print(f"\nTotal narration time: {total:.1f}s")
    print(f"Wrote {os.path.join(OUT, 'durations.json')}")


if __name__ == "__main__":
    main()

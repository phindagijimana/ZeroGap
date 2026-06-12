"""Build the final narrated video end-to-end.

Steps:
  1. Generate narration audio + durations  (make_audio.py)
  2. Render the silent Manim animation, timed to the narration
  3. Concatenate the per-segment narration clips in order
  4. Mux the narration onto the rendered video with ffmpeg

Output: output/what-is-physics.mp4

Usage:
    python3 build.py            # medium quality (1280x720 @ 30fps)
    python3 build.py --high     # high quality (1920x1080 @ 60fps, slower)
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
AUDIO_DIR = os.path.join(OUT, "audio")
FINAL = os.path.join(OUT, "what-is-physics.mp4")


def run(cmd, **kw):
    print("›", " ".join(cmd))
    subprocess.run(cmd, check=True, **kw)


def main():
    high = "--high" in sys.argv
    quality = "-qh" if high else "-qm"

    # 1. Narration audio + durations
    run([sys.executable, os.path.join(HERE, "make_audio.py")], cwd=HERE)

    # 2. Render the silent animation
    run(["manim", quality, "--media_dir", os.path.join(OUT, "media"),
         os.path.join(HERE, "physics_scene.py"), "WhatIsPhysics"], cwd=HERE)

    # Locate the rendered file (manim names the folder by resolution).
    rendered = None
    for root, _dirs, files in os.walk(os.path.join(OUT, "media", "videos")):
        for fn in files:
            if fn == "WhatIsPhysics.mp4":
                rendered = os.path.join(root, fn)
    if not rendered:
        raise SystemExit("Could not find rendered WhatIsPhysics.mp4")
    print("Rendered:", rendered)

    # 3. Pad each narration clip with trailing silence to its section's exact
    #    target length, then concatenate. This keeps every section's audio
    #    aligned with its (equally long) video section — no cumulative drift.
    with open(os.path.join(OUT, "durations.json")) as f:
        durations = json.load(f)
    listfile = os.path.join(OUT, "audio_list.txt")
    with open(listfile, "w") as f:
        for sid, target in durations.items():
            padded = os.path.join(AUDIO_DIR, f"{sid}_padded.wav")
            run(["ffmpeg", "-y", "-i", os.path.join(AUDIO_DIR, f"{sid}.wav"),
                 "-af", "apad", "-t", f"{target:.3f}", padded])
            f.write(f"file '{padded}'\n")
    narration = os.path.join(OUT, "narration.wav")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listfile,
         "-c", "copy", narration])

    # 4. Mux narration onto the video
    run(["ffmpeg", "-y", "-i", rendered, "-i", narration,
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-shortest", FINAL])

    size = os.path.getsize(FINAL) / 1e6
    print(f"\n✅ Done: {FINAL}  ({size:.1f} MB)")


if __name__ == "__main__":
    main()

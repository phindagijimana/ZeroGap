# "What is Physics?" — narrated animated explainer

A ~2 minute educational video that introduces physics with animation and
voice-over narration. Built with [Manim](https://www.manim.community/) for the
animation, **espeak-ng** for offline narration, and **ffmpeg** to mux them.

**Final video:** [`output/what-is-physics.mp4`](output/what-is-physics.mp4)
(1280×720, 30 fps)

## What it covers

1. Title — *What is Physics?*
2. Definition — matter, energy, motion
3. Mechanics — a ball falling under gravity
4. Forces — Newton's laws (`F = m × a`, action/reaction)
5. Energy — a swinging pendulum (conservation of energy)
6. Waves & light — travelling sine waves
7. Atoms — nucleus with orbiting electrons (electromagnetism & quantum)
8. The cosmos — a planet orbiting the Sun
9. Closing — *Physics is everywhere*

## How it works

Each narration line and its animation share a stable segment id, so the
animation for every section is stretched to exactly fill the length of its
spoken clip — audio and video stay in sync with no cumulative drift.

| File | Purpose |
|------|---------|
| `narration.py` | The spoken script (one entry per section). |
| `make_audio.py` | Renders each line to a WAV with espeak-ng and records its duration in `output/durations.json`. |
| `physics_scene.py` | The Manim scene; reads `durations.json` and times each section to its narration. |
| `build.py` | Orchestrates everything: audio → render → pad/concat narration → mux. |

## Rebuild it

Requires `manim`, `ffmpeg`, and `espeak-ng` on the system.

```bash
cd video
python3 build.py            # 1280x720 @ 30 fps  (default)
python3 build.py --high     # 1920x1080 @ 60 fps (slower)
```

The result is written to `output/what-is-physics.mp4`.

## Notes

- Narration uses the offline **espeak-ng** voice because higher-quality engines
  (Google TTS / Piper neural voices) need network hosts that aren't reachable
  from the build environment. To use a nicer voice, swap the synthesis command
  in `make_audio.py`.
- Build intermediates (`output/media/`, `output/audio/`, `output/*.wav`) are
  git-ignored and regenerated on each build.

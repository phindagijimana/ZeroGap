"""Narration script for the "What is Physics?" educational video.

Each segment has a stable ``id`` (used to name its audio clip and to look up the
matching animation in ``physics_scene.py``) and the spoken ``text``.

Keeping the script in one place lets the audio generator and the Manim scene
stay perfectly in sync: every segment's on-screen animation is stretched to
exactly fill the length of its narration clip.
"""

SEGMENTS = [
    {
        "id": "s1_title",
        "text": "What is physics? Let's take three minutes to find out.",
    },
    {
        "id": "s2_define",
        "text": (
            "Physics is the natural science that studies matter, energy, and "
            "how they interact. It tries to understand how the universe behaves, "
            "from the tiniest particles to the largest galaxies."
        ),
    },
    {
        "id": "s3_motion",
        "text": (
            "One of the oldest questions in physics is simple: how and why do "
            "things move? This part of physics is called mechanics. Drop a ball, "
            "and gravity pulls it down, faster and faster."
        ),
    },
    {
        "id": "s4_forces",
        "text": (
            "Forces are the pushes and pulls that change motion. Isaac Newton "
            "described them with a famous rule: force equals mass times "
            "acceleration. And every action has an equal and opposite reaction."
        ),
    },
    {
        "id": "s5_energy",
        "text": (
            "Energy is the ability to do work, and it is never destroyed, only "
            "changed from one form to another. Watch a pendulum trade height for "
            "speed, and speed back into height, again and again."
        ),
    },
    {
        "id": "s6_waves",
        "text": (
            "Physics also explains waves and light. Energy can travel as a wave "
            "through space, and that is how we are able to see colors and hear "
            "sound."
        ),
    },
    {
        "id": "s7_atom",
        "text": (
            "Zoom deep into matter and you find atoms, ruled by electricity, "
            "magnetism, and the strange but powerful laws of quantum physics."
        ),
    },
    {
        "id": "s8_cosmos",
        "text": (
            "Now zoom all the way out. The very same laws guide the planets "
            "around the Sun and shape the structure of the entire cosmos."
        ),
    },
    {
        "id": "s9_closing",
        "text": (
            "Physics is everywhere: in every motion, every spark of light, and "
            "every star in the sky. It is how we read the rule book of the "
            "universe."
        ),
    },
]

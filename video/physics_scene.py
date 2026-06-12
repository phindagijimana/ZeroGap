"""Manim scene for "What is Physics?".

The scene is split into nine sections, one per narration segment. Each section
is timed to fill exactly the duration of its narration clip (read from
``output/durations.json``) so that audio and animation line up when muxed.

Only ``Text`` is used (no LaTeX / MathTex) so the scene renders without a
TeX install. Run via ``build.py``, or directly:

    manim -qm physics_scene.py WhatIsPhysics
"""

import json
import os

import numpy as np
from manim import (
    DOWN, LEFT, ORIGIN, PI, RIGHT, UP, TAU,
    BLUE, BLUE_B, BLUE_D, GREEN, GREY_B, MAROON_B, ORANGE, PURPLE, RED,
    TEAL, WHITE, YELLOW, YELLOW_B,
    Arrow, Circle, Create, Dot, Ellipse, FadeIn, FadeOut, FunctionGraph,
    GrowArrow, Line, ParametricFunction, Rotate, Scene, Star, Text,
    Transform, ValueTracker, VGroup, Write, always_redraw,
    config, linear, rate_functions, smooth, there_and_back,
)

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "output", "durations.json")) as _f:
    DUR = json.load(_f)


class WhatIsPhysics(Scene):
    def construct(self):
        self.camera.background_color = "#0b1021"
        self.s1_title(DUR["s1_title"])
        self.s2_define(DUR["s2_define"])
        self.s3_motion(DUR["s3_motion"])
        self.s4_forces(DUR["s4_forces"])
        self.s5_energy(DUR["s5_energy"])
        self.s6_waves(DUR["s6_waves"])
        self.s7_atom(DUR["s7_atom"])
        self.s8_cosmos(DUR["s8_cosmos"])
        self.s9_closing(DUR["s9_closing"])

    # ----- helpers ---------------------------------------------------------
    def starfield(self, n=60, seed=7):
        rng = np.random.default_rng(seed)
        stars = VGroup()
        for _ in range(n):
            x = rng.uniform(-7, 7)
            y = rng.uniform(-4, 4)
            d = Dot(point=[x, y, 0], radius=rng.uniform(0.01, 0.03),
                    color=WHITE).set_opacity(rng.uniform(0.3, 0.9))
            stars.add(d)
        return stars

    def pad(self, target, used, fade=0.8):
        """Wait so that animations + this wait + the trailing fade-out sum to
        exactly ``target`` (the narration length). ``fade`` is the run_time of
        the FadeOut that immediately follows this call, reserved here so audio
        and video stay aligned across all nine sections."""
        self.wait(max(0.3, target - used - fade))

    # ----- sections --------------------------------------------------------
    def s1_title(self, target):
        stars = self.starfield(n=70)
        self.play(FadeIn(stars, run_time=1.2))
        title = Text("What is Physics?", font_size=72, weight="BOLD",
                     gradient=(BLUE_B, TEAL))
        sub = Text("a short introduction", font_size=30, color=GREY_B)
        sub.next_to(title, DOWN, buff=0.4)
        self.play(Write(title, run_time=2.0))
        self.play(FadeIn(sub, shift=UP * 0.3, run_time=1.0))
        used = 1.2 + 2.0 + 1.0
        self.pad(target, used)
        self.play(FadeOut(title), FadeOut(sub), FadeOut(stars), run_time=0.8)

    def s2_define(self, target):
        heading = Text("The science of the universe", font_size=40,
                       color=WHITE).to_edge(UP, buff=0.8)
        self.play(Write(heading, run_time=1.5))

        def pillar(label, color, icon):
            box = VGroup(icon, Text(label, font_size=30, color=color))
            box.arrange(DOWN, buff=0.3)
            return box

        matter = pillar("MATTER", BLUE_B,
                        VGroup(*[Dot(color=BLUE_B).shift(v) for v in
                                 [UP * 0.2, DOWN * 0.2 + LEFT * 0.2,
                                  DOWN * 0.2 + RIGHT * 0.2]]))
        energy = pillar("ENERGY", YELLOW,
                        Star(n=5, outer_radius=0.45, color=YELLOW,
                             fill_opacity=0.9))
        motion = pillar("MOTION", TEAL,
                        Arrow(LEFT * 0.4, RIGHT * 0.4, color=TEAL,
                              buff=0))
        row = VGroup(matter, energy, motion).arrange(RIGHT, buff=1.6)
        row.shift(DOWN * 0.4)

        self.play(FadeIn(matter, shift=UP * 0.3, run_time=1.0))
        self.play(FadeIn(energy, shift=UP * 0.3, run_time=1.0))
        self.play(FadeIn(motion, shift=UP * 0.3, run_time=1.0))
        tagline = Text("...and how they interact", font_size=28,
                       color=GREY_B).to_edge(DOWN, buff=0.9)
        self.play(FadeIn(tagline, run_time=1.0))
        used = 1.5 + 3.0 + 1.0
        self.pad(target, used)
        self.play(FadeOut(VGroup(heading, row, tagline)), run_time=0.8)

    def s3_motion(self, target):
        heading = Text("Mechanics: the study of motion", font_size=36,
                       color=BLUE_B).to_edge(UP, buff=0.7)
        ground = Line(LEFT * 6, RIGHT * 6, color=GREY_B).shift(DOWN * 3.2)
        self.play(Write(heading, run_time=1.2), Create(ground, run_time=0.8))

        ball = Dot(radius=0.22, color=RED, fill_opacity=1).move_to(
            UP * 2.6 + LEFT * 3)
        self.play(FadeIn(ball, run_time=0.5))

        # Accelerating fall + decaying bounces to show gravity.
        self.play(ball.animate.move_to(DOWN * 2.95 + LEFT * 3),
                  rate_func=rate_functions.rush_into, run_time=1.1)
        self.play(ball.animate.move_to(UP * 0.6 + LEFT * 1.2),
                  rate_func=rate_functions.rush_from, run_time=0.7)
        self.play(ball.animate.move_to(DOWN * 2.95 + LEFT * 1.2),
                  rate_func=rate_functions.rush_into, run_time=0.6)
        self.play(ball.animate.move_to(DOWN * 1.4 + RIGHT * 0.8),
                  rate_func=rate_functions.rush_from, run_time=0.5)
        self.play(ball.animate.move_to(DOWN * 2.95 + RIGHT * 0.8),
                  rate_func=rate_functions.rush_into, run_time=0.4)

        g_arrow = Arrow(ball.get_center(), ball.get_center() + DOWN * 1.2,
                        color=YELLOW, buff=0.25)
        g_label = Text("gravity", font_size=24, color=YELLOW).next_to(
            g_arrow, RIGHT, buff=0.15)
        self.play(GrowArrow(g_arrow), FadeIn(g_label), run_time=0.9)
        used = 1.2 + 0.5 + 3.3 + 0.9
        self.pad(target, used)
        self.play(FadeOut(VGroup(heading, ground, ball, g_arrow, g_label)),
                  run_time=0.8)

    def s4_forces(self, target):
        heading = Text("Forces change motion", font_size=38,
                       color=ORANGE).to_edge(UP, buff=0.7)
        self.play(Write(heading, run_time=1.2))

        box = VGroup(
            Circle(radius=0.0),  # placeholder to keep group centered
        )
        crate = Dot(radius=0.0)
        crate = VGroup(
            Line(LEFT * 0.6 + UP * 0.6, RIGHT * 0.6 + UP * 0.6),
            Line(RIGHT * 0.6 + UP * 0.6, RIGHT * 0.6 + DOWN * 0.6),
            Line(RIGHT * 0.6 + DOWN * 0.6, LEFT * 0.6 + DOWN * 0.6),
            Line(LEFT * 0.6 + DOWN * 0.6, LEFT * 0.6 + UP * 0.6),
        ).set_color(BLUE_B).set_stroke(width=6)
        crate.move_to(ORIGIN)
        self.play(Create(crate, run_time=0.8))

        push = Arrow(LEFT * 2.4, LEFT * 0.7, color=GREEN, buff=0)
        push_l = Text("action", font_size=22, color=GREEN).next_to(push, UP, buff=0.15)
        react = Arrow(RIGHT * 2.4, RIGHT * 0.7, color=RED, buff=0)
        react_l = Text("reaction", font_size=22, color=RED).next_to(react, UP, buff=0.15)
        self.play(GrowArrow(push), FadeIn(push_l), run_time=0.8)
        self.play(GrowArrow(react), FadeIn(react_l), run_time=0.8)

        formula = Text("F = m × a", font_size=44, color=YELLOW)
        formula.to_edge(DOWN, buff=1.0)
        self.play(Write(formula, run_time=1.2))
        used = 1.2 + 0.8 + 1.6 + 1.2
        self.pad(target, used)
        self.play(FadeOut(VGroup(heading, crate, push, push_l, react,
                                 react_l, formula)), run_time=0.8)

    def s5_energy(self, target):
        heading = Text("Energy is conserved", font_size=38,
                       color=YELLOW_B).to_edge(UP, buff=0.7)
        self.play(Write(heading, run_time=1.2))

        pivot = UP * 2.6
        rod = Line(pivot, pivot + DOWN * 3.2, color=GREY_B)
        bob = Dot(rod.get_end(), radius=0.28, color=MAROON_B, fill_opacity=1)
        pend = VGroup(rod, bob)
        pin = Dot(pivot, radius=0.06, color=WHITE)
        self.add(pin)
        # Start lifted to one side.
        self.play(Rotate(pend, angle=PI / 5, about_point=pivot, run_time=0.8))
        self.play(FadeIn(pin, run_time=0.1))

        used = 1.2 + 0.8
        # Swing back and forth to fill remaining time.
        while used < target - 1.3:
            self.play(Rotate(pend, angle=-2 * PI / 5, about_point=pivot,
                             rate_func=there_and_back, run_time=1.8))
            used += 1.8
        self.pad(target, used)
        self.play(FadeOut(VGroup(heading, pend, pin)), run_time=0.8)

    def s6_waves(self, target):
        heading = Text("Waves carry energy and light", font_size=36,
                       color=TEAL).to_edge(UP, buff=0.7)
        self.play(Write(heading, run_time=1.2))

        t = ValueTracker(0.0)
        amp = 1.3

        wave = always_redraw(lambda: FunctionGraph(
            lambda x: amp * np.sin(1.2 * x - t.get_value()),
            x_range=[-6, 6, 0.05], color=TEAL).set_stroke(width=5))
        wave2 = always_redraw(lambda: FunctionGraph(
            lambda x: 0.6 * amp * np.sin(2.2 * x - 1.6 * t.get_value()),
            x_range=[-6, 6, 0.05], color=PURPLE).set_stroke(width=3)
            .set_opacity(0.8))
        self.add(wave, wave2)
        self.play(FadeIn(wave), FadeIn(wave2), run_time=0.6)
        remaining = target - (1.2 + 0.6) - 0.8
        self.play(t.animate.set_value(remaining * 3.0),
                  rate_func=linear, run_time=max(0.5, remaining))
        self.play(FadeOut(VGroup(heading, wave, wave2)), run_time=0.8)

    def s7_atom(self, target):
        heading = Text("Atoms, electricity & quantum physics",
                       font_size=32, color=PURPLE).to_edge(UP, buff=0.7)
        self.play(Write(heading, run_time=1.2))

        nucleus = VGroup(
            Dot(radius=0.18, color=RED).shift(UP * 0.12),
            Dot(radius=0.18, color=BLUE).shift(DOWN * 0.12 + LEFT * 0.1),
            Dot(radius=0.18, color=RED).shift(DOWN * 0.05 + RIGHT * 0.13),
        ).move_to(DOWN * 0.3)

        orbits = VGroup(
            Ellipse(width=4.0, height=2.2, color=GREY_B).set_stroke(width=2),
            Ellipse(width=2.4, height=4.2, color=GREY_B).set_stroke(width=2)
            .rotate(PI / 6),
            Ellipse(width=4.6, height=4.6, color=GREY_B).set_stroke(width=2),
        ).move_to(nucleus.get_center())

        e1 = Dot(radius=0.1, color=YELLOW).move_to(
            nucleus.get_center() + RIGHT * 2.0)
        e2 = Dot(radius=0.1, color=TEAL).move_to(
            nucleus.get_center() + UP * 2.1)
        e3 = Dot(radius=0.1, color=BLUE_B).move_to(
            nucleus.get_center() + RIGHT * 2.3)

        self.play(FadeIn(nucleus, scale=0.5, run_time=0.8),
                  Create(orbits, run_time=1.0))
        self.add(e1, e2, e3)

        center = nucleus.get_center()
        used = 1.2 + 1.0
        # Animate electrons orbiting until the section is filled.
        while used < target - 1.0:
            self.play(
                Rotate(e1, angle=TAU, about_point=center, rate_func=linear),
                Rotate(e2, angle=-TAU, about_point=center, rate_func=linear),
                Rotate(e3, angle=TAU, about_point=center, rate_func=linear),
                run_time=2.2,
            )
            used += 2.2
        self.pad(target, used)
        self.play(FadeOut(VGroup(heading, nucleus, orbits, e1, e2, e3)),
                  run_time=0.8)

    def s8_cosmos(self, target):
        stars = self.starfield(n=80, seed=21)
        self.play(FadeIn(stars, run_time=0.8))
        heading = Text("The same laws shape the cosmos", font_size=34,
                       color=BLUE_B).to_edge(UP, buff=0.7)
        self.play(Write(heading, run_time=1.2))

        sun = Dot(radius=0.45, color=YELLOW, fill_opacity=1).move_to(ORIGIN)
        sun_glow = Circle(radius=0.7, color=ORANGE).set_fill(
            ORANGE, opacity=0.25).set_stroke(width=0).move_to(ORIGIN)
        orbit = Circle(radius=2.6, color=GREY_B).set_stroke(width=1.5)
        planet = Dot(radius=0.16, color=BLUE).move_to(RIGHT * 2.6)
        self.play(FadeIn(sun_glow), FadeIn(sun), Create(orbit), run_time=1.0)

        used = 0.8 + 1.2 + 1.0
        while used < target - 1.0:
            self.play(Rotate(planet, angle=TAU, about_point=ORIGIN,
                             rate_func=linear, run_time=2.4))
            used += 2.4
        self.pad(target, used)
        self.play(FadeOut(VGroup(heading, sun, sun_glow, orbit, planet,
                                 stars)), run_time=0.8)

    def s9_closing(self, target):
        stars = self.starfield(n=110, seed=99)
        self.play(FadeIn(stars, run_time=1.0))
        big = Text("Physics is everywhere", font_size=64, weight="BOLD",
                   gradient=(TEAL, BLUE_B, PURPLE))
        self.play(Write(big, run_time=2.0))
        sub = Text("the rule book of the universe", font_size=30,
                   color=GREY_B).next_to(big, DOWN, buff=0.45)
        self.play(FadeIn(sub, shift=UP * 0.3, run_time=1.2))
        # Gentle twinkle.
        used = 1.0 + 2.0 + 1.2
        self.play(stars.animate.set_opacity(0.4), run_time=1.0)
        self.play(stars.animate.set_opacity(0.9), run_time=1.0)
        used += 2.0
        self.pad(target, used, fade=1.2)
        self.play(FadeOut(VGroup(big, sub, stars)), run_time=1.2)

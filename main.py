from __future__ import annotations

import sys

from potion import *

from scenes.start_screen import StartScreen
from scenes.main_scene import MainScene


def main() -> int:
    # Init engine
    Game.init(name="LD56", version="v1")
    Engine.init_default()
    Window.init_default()
    Renderer.init_default()

    # Start the first scene
    # scene = StartScreen()
    scene = MainScene(is_tutorial=False)
    Engine.start(scene)
    return 0


# def register_text_effects() -> None:
#     from math import sin
#     from potion.data_types.color import Color
#     from potion.text_effect import TextEffect
#     from potion.engine import Engine
#
#     if TYPE_CHECKING:
#         from potion.glyph import Glyph
#
#     class TextEffectRainbow(TextEffect):
#         """ Draws rainbow text. """
#         @classmethod
#         def tag(cls) -> str:
#             return "RAINBOW"
#
#         @classmethod
#         def glyph_color(cls, glyph: Glyph) -> Color:
#             frame = Engine.frame()
#             cycle = (frame % 120.0) / 120.0
#             offset = float(glyph.index) / 25.0
#             hue = cycle - offset
#             color = Color.from_hsv(hue, 1, 1)
#
#             return color
#
#     class TextEffectExciting(TextEffect):
#         """ Draws floating text. """
#
#         @classmethod
#         def tag(cls) -> str:
#             return "EXCITING"
#
#         @classmethod
#         def glyph_color(cls, glyph: Glyph) -> Color:
#             return Color.yellow()
#
#         @classmethod
#         def glyph_offset(cls, glyph: Glyph) -> Point:
#             frame = Engine.frame()
#             t = frame / 8.0
#             cycle_offset = float(glyph.index) / 2.0
#             y_offset = sin(t - cycle_offset) * 2
#             position_offset = Point(0, y_offset)
#             return position_offset
#
#     TextEffectRainbow.register()
#     TextEffectExciting.register()


if __name__ == "__main__":
    with papp.crash_handler():
        sys.exit(main())

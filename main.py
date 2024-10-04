import sys

from potion import *

from scenes.main_scene import MainScene


def main() -> int:
    # Init engine
    Game.init(name="LD56", version="v1")
    Engine.init_default()
    Window.init_default()
    Renderer.init_default()

    # Start the first scene
    scene = MainScene()
    Engine.start(scene)
    return 0


if __name__ == "__main__":
    with papp.crash_handler():
        sys.exit(main())

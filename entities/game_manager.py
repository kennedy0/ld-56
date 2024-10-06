from __future__ import annotations

from potion import *


if TYPE_CHECKING:
    from entities.bug import Bug
    from entities.bug_spawner import BugSpawner
    from entities.cutscene import Cutscene


class GameManager(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "GameManager"

        # Entity References
        self.cutscene: Cutscene | None = None
        self.bug_spawner_top_left: BugSpawner | None = None
        self.bug_spawner_top_right: BugSpawner | None = None
        self.bug_spawner_bottom_left: BugSpawner | None = None
        self.bug_spawner_bottom_right: BugSpawner | None = None

        # Current bugs in on the map
        self.bugs: list[Bug] = []

    def start(self) -> None:
        self.cutscene = self.find("Cutscene")
        self.bug_spawner_top_left = self.find("BugSpawnerTopLeft")
        self.bug_spawner_top_right = self.find("BugSpawnerTopRight")
        self.bug_spawner_bottom_left = self.find("BugSpawnerBottomLeft")
        self.bug_spawner_bottom_right = self.find("BugSpawnerBottomRight")

    def update(self) -> None:
        if __debug__:
            if Keyboard.get_key_down(Keyboard.RETURN):
                self.start_tutorial()
            if Keyboard.get_key_down(Keyboard.NUM_1):
                self.start_wave_1()
            if Keyboard.get_key_down(Keyboard.NUM_2):
                self.start_wave_2()

    def start_tutorial(self) -> None:
        self.cutscene.show_text_box()
        self.cutscene.text("Testing...\nOne, Two Three...")
        self.cutscene.hide_text_box()
        self.cutscene.start_cutscene()

    def start_wave_1(self) -> None:
        bugs = ["ant"] * 10
        self.bug_spawner_top_left.spawn(bugs)

    def start_wave_2(self) -> None:
        bugs = ["ant"] * 10
        self.bug_spawner_top_right.spawn(bugs)

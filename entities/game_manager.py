from __future__ import annotations

from potion import *


if TYPE_CHECKING:
    from entities.bug import Bug
    from entities.bug_spawner import BugSpawner


class GameManager(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "GameManager"

        # Entity References
        self.bug_spawner_top_left: BugSpawner | None = None
        self.bug_spawner_top_right: BugSpawner | None = None
        self.bug_spawner_bottom_left: BugSpawner | None = None
        self.bug_spawner_bottom_right: BugSpawner | None = None

        # Current bugs in on the map
        self.bugs: list[Bug] = []

    def start(self) -> None:
        self.bug_spawner_top_left = self.find("BugSpawnerTopLeft")
        self.bug_spawner_top_right = self.find("BugSpawnerTopRight")
        self.bug_spawner_bottom_left = self.find("BugSpawnerBottomLeft")
        self.bug_spawner_bottom_right = self.find("BugSpawnerBottomRight")

    def update(self) -> None:
        if Keyboard.get_key_down(Keyboard.NUM_1):
            self.start_wave_1()
        if Keyboard.get_key_down(Keyboard.NUM_2):
            self.start_wave_2()

    def start_wave_1(self) -> None:
        bugs = ["ant"] * 10
        self.bug_spawner_top_left.spawn(bugs)

    def start_wave_2(self) -> None:
        bugs = ["ant"] * 10
        self.bug_spawner_top_right.spawn(bugs)

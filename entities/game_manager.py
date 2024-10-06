from __future__ import annotations

from imaplib import Debug

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
        Log.debug("START TUTORIAL")

        # self.cutscene.pause(3)

        self.cutscene.show_text_box()
        self.cutscene.text("Hello...\nIs this thing on?")
        self.cutscene.pause(.5)
        self.cutscene.text("Okay soldier, listen up.\nSee that apple over there?")
        self.cutscene.disable_player()
        self.cutscene.move_camera_to_position(Point(400, 200))
        self.cutscene.text("The bugs are about to be all over it.\nWe can't let that happen.")
        self.cutscene.text("It'll ruin my picnic...!")
        self.cutscene.pause(.5)
        self.cutscene.text("*Cough*")
        self.cutscene.pause(.5)
        self.cutscene.text("I mean, it'll ruin my training\nexercise!")
        self.cutscene.move_camera_to_player()
        self.cutscene.text("That's where you come in.")
        self.cutscene.enable_player()
        self.cutscene.text("You're piloting the Bug-Bash Buggy,\nthe latest in cutting-edge")
        self.cutscene.text("military technology.")
        self.cutscene.text("Let's take it for a spin.\nClick the left mouse to drive.")
        self.cutscene.hide_text_box()
        self.cutscene.start_cutscene()

    def start_wave_1(self) -> None:
        Log.debug("START Wave 1")
        bugs = ["ant"] * 10
        self.bug_spawner_top_left.spawn(bugs)

    def start_wave_2(self) -> None:
        Log.debug("START Wave 2")
        bugs = ["ant"] * 10
        self.bug_spawner_top_right.spawn(bugs)

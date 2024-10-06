from __future__ import annotations

from potion import *


if TYPE_CHECKING:
    from entities.apple import Apple
    from entities.bug import Bug
    from entities.bug_spawner import BugSpawner
    from entities.camera_controller import CameraController
    from entities.cutscene import Cutscene
    from entities.player import Player


class GameManager(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "GameManager"

        # Entity References
        self.apple: Apple | None = None
        self.camera_controller: CameraController | None = None
        self.cutscene: Cutscene | None = None
        self.player: Player | None = None
        self.bug_spawner_top_left: BugSpawner | None = None
        self.bug_spawner_top_right: BugSpawner | None = None
        self.bug_spawner_bottom_left: BugSpawner | None = None
        self.bug_spawner_bottom_right: BugSpawner | None = None

        # Current bugs in on the map
        self.bugs: list[Bug] = []

        # Tutorial
        self.tutorial_bug: Bug | None = None
        self.tutorial_focus_point: Point | None = None

    def start(self) -> None:
        self.apple = self.find("Apple")
        self.camera_controller = self.find("CameraController")
        self.cutscene = self.find("Cutscene")
        self.player = self.find("Player")
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
        self.cutscene.text("Let's take it for a spin.")
        self.cutscene.text("Click the left mouse to drive.")
        self.cutscene.hide_text_box()
        self.cutscene.add_custom_coroutine(self._tutorial_wait_for_drive())
        self.cutscene.show_text_box()
        self.cutscene.text("Steering is simple: the buggy\nalways drives towards the mouse.")
        self.cutscene.text("(Try not to scratch the paint)")
        self.cutscene.pause(1)
        self.cutscene.disable_player()
        self.cutscene.add_custom_coroutine(self._tutorial_spawn_ant())
        self.cutscene.text("Look alive, soldier!\nAerial recon has spotted a bug.")
        self.cutscene.hide_text_box()
        self.cutscene.add_custom_coroutine(self._tutorial_move_camera_to_bug())
        self.cutscene.pause(1)
        self.cutscene.move_camera_to_player()
        self.cutscene.enable_player()
        self.cutscene.show_text_box()
        self.cutscene.text("Don't just stand there,\nshow 'em who's boss!")
        self.cutscene.hide_text_box()
        self.cutscene.add_custom_coroutine(self._tutorial_wait_for_bug_to_die())
        self.cutscene.show_text_box()
        self.cutscene.text("Target eliminated.")
        self.cutscene.hide_text_box()
        self.cutscene.pause(.5)

        # ToDo: More mechanics go here

        # End tutorial
        self.cutscene.show_text_box()
        self.cutscene.text("That's all for now soldier.")
        self.cutscene.text("Bring the buggy back to the garage\nfor a tune-up.")
        self.cutscene.hide_text_box()
        self.cutscene.fade_out()
        self.cutscene.load_start_screen()
        self.cutscene.start_cutscene()

    def _tutorial_wait_for_drive(self) -> Generator:
        while not self.player.move_input:
            yield

        yield from wait_for_seconds(3)

    def _tutorial_spawn_ant(self) -> Generator:
        points = [
            Point(340, 169),
            Point(460, 169),
            Point(340, 229),
            Point(460, 229),
        ]

        furthest_point = None
        furthest_distance = None

        for point in points:
            this_distance = point.distance_to(self.player.position())

            if furthest_point is None:
                furthest_point = point
                furthest_distance = this_distance

            if this_distance > furthest_distance:
                furthest_point = point
                furthest_distance = this_distance

        from entities.ant import Ant
        ant = Ant()
        ant.set_position(furthest_point)
        self.scene.entities.add(ant)
        self.tutorial_bug = ant
        self.tutorial_focus_point = furthest_point
        yield

    def _tutorial_move_camera_to_bug(self) -> Generator:
        self.camera_controller.target_point = self.tutorial_focus_point
        while not self.camera_controller.in_range_of_target():
            yield

    def _tutorial_wait_for_bug_to_die(self) -> Generator:
        while not self.tutorial_bug.dead:
            # Keep the apple alive no matter what
            if self.apple.hp <= 1:
                self.apple.hp = 1

            yield

        self.cutscene.pause(.5)

    def start_wave_1(self) -> None:
        Log.debug("START Wave 1")
        bugs = ["ant"] * 10
        self.bug_spawner_top_left.spawn(bugs)

    def start_wave_2(self) -> None:
        Log.debug("START Wave 2")
        bugs = ["ant"] * 10
        self.bug_spawner_top_right.spawn(bugs)

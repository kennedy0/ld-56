from __future__ import annotations
import math

from potion import *

from entities.ant import Ant

if TYPE_CHECKING:
    from entities.apple import Apple
    from entities.bug import Bug
    from entities.bug_spawner import BugSpawner
    from entities.camera_controller import CameraController
    from entities.cutscene import Cutscene
    from entities.defeat_screen import DefeatScreen
    from entities.player import Player
    from entities.victory_screen import VictoryScreen
    from entities.wave_banner import WaveBanner


class GameManager(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "GameManager"

        # Entity References
        self.apple: Apple | None = None
        self.camera_controller: CameraController | None = None
        self.cutscene: Cutscene | None = None
        self.defeat_screen: DefeatScreen | None = None
        self.player: Player | None = None
        self.victory_screen: VictoryScreen | None = None
        self.wave_banner: WaveBanner | None = None

        self.bug_spawner_top_left: BugSpawner | None = None
        self.bug_spawner_top_right: BugSpawner | None = None
        self.bug_spawner_bottom_left: BugSpawner | None = None
        self.bug_spawner_bottom_right: BugSpawner | None = None

        # Current bugs in on the map
        self.bugs: list[Bug] = []
        self.bugs_this_wave = 0

        # Game state
        self.game_over = False
        self.wave = -1
        self.total_waves = 4
        self.wave_started = False
        self.wave_ended = False

        # Tutorial
        self.is_tutorial = False
        self.game_started = False
        self.tutorial_bug: Bug | None = None
        self.tutorial_focus_point: Point | None = None

    def start(self) -> None:
        self.apple = self.find("Apple")
        self.camera_controller = self.find("CameraController")
        self.cutscene = self.find("Cutscene")
        self.defeat_screen = self.find("DefeatScreen")
        self.player = self.find("Player")
        self.victory_screen = self.find("VictoryScreen")
        self.wave_banner = self.find("WaveBanner")

        self.bug_spawner_top_left = self.find("BugSpawnerTopLeft")
        self.bug_spawner_top_right = self.find("BugSpawnerTopRight")
        self.bug_spawner_bottom_left = self.find("BugSpawnerBottomLeft")
        self.bug_spawner_bottom_right = self.find("BugSpawnerBottomRight")

    def update(self) -> None:
        # Manually start waves with keyboard
        if __debug__:
            # Kill cutscene and end wave with Escape
            if Keyboard.get_key_down(Keyboard.ESCAPE):
                self.cutscene.stop_cutscene()
                self.wave_ended = True
                self.bugs_this_wave = 0

            # Start waves with keyboard
            if Keyboard.get_key_down(Keyboard.NUM_1):
                self.start_wave_1()
            if Keyboard.get_key_down(Keyboard.NUM_2):
                self.start_wave_2()
            if Keyboard.get_key_down(Keyboard.NUM_3):
                self.start_wave_3()
            if Keyboard.get_key_down(Keyboard.NUM_4):
                self.start_wave_4()

        # Start the game
        if not self.game_started:
            self.game_started = True
            if self.is_tutorial:
                self.start_tutorial()

        # Check for game over
        if self.apple.hp <= 0 and not self.game_over:
            self.game_over = True
            self.start_defeat()
            return

        # Don't do wave logic on the tutorial
        if self.is_tutorial:
            return

        # Advance wave
        if not self.wave_started:
            self.wave_started = True
            self.wave += 1

            if self.wave == 0:
                self.start_wave_1()
            elif self.wave == 1:
                self.start_wave_2()
            elif self.wave == 2:
                self.start_wave_3()
            elif self.wave == 3:
                self.start_wave_4()
            else:
                if not self.game_over:
                    self.game_over = True
                    self.start_victory()

        # End wave
        if self.wave_ended:
            self.wave_started = False
            self.wave_ended = False

    def start_game(self) -> None:
        Log.debug("START GAME")

    def start_tutorial(self) -> None:
        Log.debug("START TUTORIAL")

        self.cutscene.pause(3)

        self.cutscene.show_text_box()
        self.cutscene.text("Hello...\nIs this thing on?")
        self.cutscene.pause(.5)
        self.cutscene.text("Okay soldier, listen up.\nSee that apple over there?")
        self.cutscene.disable_player()
        self.cutscene.move_camera_to_position(Point(400, 200))
        self.cutscene.text("The bugs are gonna be all over it.\nWe can't let that happen.")
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
        self.cutscene.disable_player()
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
            yield

        self.cutscene.pause(.5)

    def start_wave_1(self) -> None:
        Log.debug("START Wave 1")

        def _c() -> Generator:
            # 10 Ants, TopLeft
            for i in range(10):
                self.bug_spawner_top_left.spawn(Ant)
                yield from wait_for_seconds(1)

        self.cutscene.pause(3)
        self.cutscene.add_custom_coroutine(self.show_wave_banner())
        self.cutscene.show_text_box()
        self.cutscene.text("Bugs approaching from North-West!")
        self.cutscene.hide_text_box()
        self.cutscene.add_custom_coroutine(_c())
        self.cutscene.add_custom_coroutine(self.wait_for_wave_to_finish())
        self.cutscene.add_custom_coroutine(self.end_wave())
        self.cutscene.start_cutscene()

    def start_wave_2(self) -> None:
        Log.debug("START Wave 2")

        def _c() -> Generator:
            # 10 Ants, TopRight
            for i in range(10):
                self.bug_spawner_top_right.spawn(Ant)
                yield from wait_for_seconds(1)

        self.cutscene.pause(3)
        self.cutscene.add_custom_coroutine(self.show_wave_banner())
        self.cutscene.show_text_box()
        self.cutscene.text("Bugs approaching from North-East!")
        self.cutscene.hide_text_box()
        self.cutscene.add_custom_coroutine(_c())
        self.cutscene.add_custom_coroutine(self.wait_for_wave_to_finish())
        self.cutscene.add_custom_coroutine(self.end_wave())
        self.cutscene.start_cutscene()

    def start_wave_3(self) -> None:
        Log.debug("START Wave 3")

        def _c() -> Generator:
            # 10 Ants, BottomRight
            for i in range(10):
                self.bug_spawner_bottom_right.spawn(Ant, "9")
                yield from wait_for_seconds(1)

            # 10 Ants, BottomRight
            for i in range(10):
                self.bug_spawner_bottom_right.spawn(Ant, "8")
                yield from wait_for_seconds(1)

            # 10 Ants, BottomRight
            for i in range(10):
                self.bug_spawner_bottom_right.spawn(Ant, "7")
                yield from wait_for_seconds(1)

        self.cutscene.pause(3)
        self.cutscene.add_custom_coroutine(self.show_wave_banner())
        self.cutscene.show_text_box()
        self.cutscene.text("Bugs approaching from South-East!")
        self.cutscene.hide_text_box()
        self.cutscene.add_custom_coroutine(_c())
        self.cutscene.add_custom_coroutine(self.wait_for_wave_to_finish())
        self.cutscene.add_custom_coroutine(self.end_wave())
        self.cutscene.start_cutscene()

    def start_wave_4(self) -> None:
        Log.debug("START Wave 3")

        def _c() -> Generator:
            # 30 Ants, BottomLeft
            waypoints = ["4", "5", "6"]
            waypoint_index = 0

            for i in range(30):
                # Get lane
                lane = waypoints[waypoint_index]

                # Spawn bug
                self.bug_spawner_bottom_left.spawn(Ant, lane)
                yield from wait_for_seconds(1)

                # Advance index
                waypoint_index += 1
                if waypoint_index >= len(waypoints):
                    waypoint_index = 0

        self.cutscene.pause(3)
        self.cutscene.add_custom_coroutine(self.show_wave_banner())
        self.cutscene.show_text_box()
        self.cutscene.text("Bugs approaching from South-West!")
        self.cutscene.hide_text_box()
        self.cutscene.add_custom_coroutine(_c())
        self.cutscene.add_custom_coroutine(self.wait_for_wave_to_finish())
        self.cutscene.add_custom_coroutine(self.end_wave())
        self.cutscene.start_cutscene()

    def show_wave_banner(self) -> Generator:
        left = -320
        center = 0
        right = 320
        self.wave_banner.x = left
        self.wave_banner.visible = True
        yield

        t = 0
        while t < 1.0:
            t += Time.delta_time
            tt = math.sqrt(t)
            self.wave_banner.x = pmath.lerp(left, center, tt)
            yield

        yield from wait_for_seconds(3)

        t = 0
        while t < 1.0:
            t += Time.delta_time
            tt = t ** 2
            self.wave_banner.x = pmath.lerp(center, right, tt)
            yield

        self.wave_banner.visible = False
        self.wave_banner.x = left
        yield from wait_for_seconds(3)

    def wait_for_wave_to_finish(self) -> Generator:
        while self.bugs:
            yield

    def end_wave(self) -> Generator:
        self.wave_ended = True
        self.bugs_this_wave = 0
        yield

    def start_victory(self) -> None:
        if self.cutscene.is_running():
            self.cutscene.stop_cutscene()

        self.cutscene.disable_player()
        self.cutscene.move_camera_to_position(Point(400, 200))
        self.cutscene.show_text_box()
        self.cutscene.text("All hostile bugs eradicated.")
        self.cutscene.text("Great job soldier.")
        self.cutscene.text("Head back to base;\nit's time to celebrate.")
        self.cutscene.text("I think you've earned\nme a promotion!")
        self.cutscene.hide_text_box()
        self.cutscene.fade_out()
        self.cutscene.add_custom_coroutine(self.victory_screen.show_victory_screen())
        self.cutscene.load_start_screen()
        self.cutscene.start_cutscene()

    def start_defeat(self) -> None:
        if self.cutscene.is_running():
            self.cutscene.stop_cutscene()

        self.cutscene.disable_player()
        self.cutscene.move_camera_to_position(Point(400, 200))
        self.cutscene.show_text_box()
        self.cutscene.text("It's over...")
        self.cutscene.text("Abort mission.")
        self.cutscene.hide_text_box()
        self.cutscene.fade_out()
        self.cutscene.add_custom_coroutine(self.defeat_screen.show_defeat_screen())
        self.cutscene.load_start_screen()
        self.cutscene.start_cutscene()

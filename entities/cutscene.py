from __future__ import annotations

from potion import *

if TYPE_CHECKING :
    from entities.camera_controller import CameraController
    from entities.player import Player
    from entities.screen_fade import ScreenFade
    from entities.text_box import TextBox



class Cutscene(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Cutscene"

        # Entity references
        self._text_box: TextBox | None = None
        self._player: Player | None = None
        self._camera_controller: CameraController | None = None
        self._screen_fade: ScreenFade | None = None

        self._cutscene_coroutine: Generator | None = None
        self._coroutines = []

    def is_running(self) -> bool:
        if self._cutscene_coroutine:
            return True
        else:
            return False

    def start(self) -> None:
        self._text_box = self.find("TextBox")
        self._player = self.find("Player")
        self._screen_fade = self.find("ScreenFade")
        self._camera_controller = self.find("CameraController")

    def pause(self, seconds: float) -> None:
        self._coroutines.append(wait_for_seconds(seconds))

    def show_text_box(self) -> None:
        def _c() -> Generator:
            self._text_box.show()
            self._text_box.text.text = ""
            self._text_box.text.visible_characters = 0
            yield

        self._coroutines.append(_c())


    def text(self, text: str) -> None:
        """ Show text in the text box. """
        delay_frames = 3

        def _c() -> Generator:
            yield from wait_for_seconds(.5)

            self._text_box.text.text = text
            while self._text_box.text.visible_characters < len(text):
                if Engine.frame() % delay_frames == 0:
                    self._text_box.text.visible_characters += 1
                yield

            yield from wait_for_seconds(1.5)
            self._text_box.text.text = ""
            self._text_box.text.visible_characters = 0

        self._coroutines.append(_c())

    def hide_text_box(self) -> None:
        def _c() -> Generator:
            self._text_box.hide()
            self._text_box.text.text = ""
            self._text_box.text.visible_characters = 0
            yield

        self._coroutines.append(_c())

    def move_camera_to_position(self, position: Point) -> None:
        def _c() -> Generator:
            self._camera_controller.target_point = position
            while not self._camera_controller.in_range_of_target():
                yield

        self._coroutines.append(_c())

    def move_camera_to_player(self) -> None:
        def _c() -> Generator:
            self._camera_controller.target_point = self._player.position()
            while not self._camera_controller.in_range_of_target():
                yield
            self._camera_controller.target_point = None
            yield

        self._coroutines.append(_c())

    def disable_player(self) -> None:
        def _c() -> Generator:
            self._player.can_control = False
            yield

        self._coroutines.append(_c())

    def enable_player(self) -> None:
        def _c() -> Generator:
            self._player.can_control = True
            yield

        self._coroutines.append(_c())

    def add_custom_coroutine(self, coroutine: Generator) -> None:
        self._coroutines.append(coroutine)

    def fade_out(self) -> None:
        self._coroutines.append(self._screen_fade.fade_out())

    def fade_in(self) -> None:
        self._coroutines.append(self._screen_fade.fade_in())

    def load_start_screen(self) -> None:
        def _c() -> Generator:
            yield
            from scenes.start_screen import StartScreen
            Engine.load_scene(StartScreen())

        self._coroutines.append(_c())

    def start_cutscene(self) -> None:
        if not self._coroutines:
            Log.error(f"Can't start cutscene, there are no coroutines")
            return

        if self._cutscene_coroutine:
            Log.error("Can't start cutscene, there is already one running")
            return

        def _cutscene_coroutine() -> Generator:
            for coroutine in self._coroutines:
                yield from coroutine

            self._coroutines.clear()
            self._cutscene_coroutine = None

        self._cutscene_coroutine = _cutscene_coroutine()
        start_coroutine(self._cutscene_coroutine)

    def stop_cutscene(self) -> None:
        if self._cutscene_coroutine:
            stop_coroutine(self._cutscene_coroutine)
            self._coroutines.clear()
            self._cutscene_coroutine = None
            self._reset_everything()
        else:
            Log.error("There is no cutscene running")

    def _reset_everything(self) -> None:
        # Hide text box
        self._text_box.hide()
        self._text_box.text.text = ""
        self._text_box.text.visible_characters = 0

        # Camera follow player
        self._camera_controller.target_point = None

        # Enable player
        self._player.can_control = True

        # Hide the screen fade
        self._screen_fade.opacity = 0
        self._screen_fade.visible = False

from __future__ import annotations

from potion import *

if TYPE_CHECKING :
    from entities.text_box import TextBox


class Cutscene(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Cutscene"

        # Entity references
        self._text_box: TextBox | None = None

        self._coroutines = []

    def start(self) -> None:
        self._text_box = self.find("TextBox")

    def show_text_box(self) -> None:
        def _c() -> Generator:
            self._text_box.show()
            self._text_box.text.text = ""
            self._text_box.text.visible_characters = 0
            yield

        self._coroutines.append(_c())

    def text(self, text: str, pause: float = 2) -> None:
        """ Show text in the text box. """
        delay_frames = 4

        def _c() -> Generator:
            yield from wait_for_seconds(.5)
            
            self._text_box.text.text = text
            while self._text_box.text.visible_characters < len(text):
                if Engine.frame() % delay_frames == 0:
                    self._text_box.text.visible_characters += 1
                yield

            yield from wait_for_seconds(pause)

        self._coroutines.append(_c())

    def hide_text_box(self) -> None:
        def _c() -> Generator:
            self._text_box.hide()
            self._text_box.text.text = ""
            self._text_box.text.visible_characters = 0
            yield

        self._coroutines.append(_c())

    def start_cutscene(self) -> None:
        if not self._coroutines:
            Log.error(f"Can't start cutscene, there are no coroutines")
            return

        def _cutscene_coroutine() -> Generator:
            for coroutine in self._coroutines:
                yield from coroutine
            self._coroutines.clear()

        start_coroutine(_cutscene_coroutine())

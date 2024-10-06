from __future__ import annotations

from potion import *

if TYPE_CHECKING:
    from entities.game_manager import GameManager


class BugUI(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "BugUI"
        self.tags.add("UI")
        self.game_manager: GameManager | None = None
        self.sprite = Sprite.from_atlas("atlas.png", "bug_ui")
        self.text = Text("fonts/m3x6.16.png")

        self.sprite_position = Point(32, 0)
        self.text_position = Point(47, 0)

    def start(self) -> None:
        self.game_manager = self.find("GameManager")

    def update(self) -> None:
        total = self.game_manager.bugs_this_wave
        killed = total - len(self.game_manager.bugs)
        self.text.text = f"{killed}/{total}"

    def draw(self, camera: Camera) -> None:
        if self.game_manager.wave_started:
            self.sprite.draw(camera, self.sprite_position)
            self.text.draw(camera, self.text_position)

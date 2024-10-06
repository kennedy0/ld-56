from __future__ import annotations

from potion import *

if TYPE_CHECKING:
    from entities.apple import Apple


class AppleUI(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "AppleUI"
        self.tags.add("UI")
        self.apple: Apple | None = None
        self.sprite = Sprite.from_atlas("atlas.png", "apple_ui")
        self.timer = 0
        self.max_timer = 1
        self.timer2 = 0

        self.hp_rect_outline = Rect(14, 5, 12, 4)
        self.hp_rect = Rect(15, 6, 10, 2)

        self.outline_color = Color.black()
        self.black_color = Color.black()
        self.white_color = Color.white()
        self.red_color = Color.from_hex("#ae2334")
        self.green_color = Color.from_hex("#1ebc73")

    def start(self) -> None:
        self.apple = self.find("Apple")

    def update(self) -> None:
        self.timer -= Time.delta_time
        if self.timer < 0:
            self.timer = 0

        if self.timer > 0:
            self.timer2 += Time.delta_time * 3
            if int(self.timer2) % 2 == 0:
                self.sprite.flash_opacity = 128
                self.outline_color = self.white_color
            else:
                self.sprite.flash_opacity = 0
                self.outline_color = self.black_color
        else:
            self.sprite.flash_opacity = 0
            self.outline_color = self.black_color
            self.timer2 = 0


    def flash(self) -> None:
        self.timer = self.max_timer

    def draw(self, camera: Camera) -> None:
        self.sprite.draw(camera, self.position())
        self.hp_rect_outline.draw(camera, self.outline_color)
        self.hp_rect.draw(camera, self.red_color)

        width = int((self.apple.hp / self.apple.max_hp) * 10)
        if width > 0:
            Rect(15, 6, width, 2).draw(camera, self.green_color)

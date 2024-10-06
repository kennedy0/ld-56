from __future__ import annotations

from potion import *

if TYPE_CHECKING:
    from entities.game_manager import GameManager


class WaveBanner(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "WaveBanner"
        self.tags.add("UI")
        self.game_manager: GameManager | None = None
        self.sprite = Sprite.empty()
        self.sprites = [
            Sprite.from_atlas("atlas.png", "wave_banner.0001"),
            Sprite.from_atlas("atlas.png", "wave_banner.0002"),
            Sprite.from_atlas("atlas.png", "wave_banner.0003"),
            Sprite.from_atlas("atlas.png", "wave_banner.0004"),
            Sprite.from_atlas("atlas.png", "wave_banner.0005"),
            Sprite.from_atlas("atlas.png", "wave_banner.0006"),
            Sprite.from_atlas("atlas.png", "wave_banner.0007"),
            Sprite.from_atlas("atlas.png", "wave_banner.0008"),
            Sprite.from_atlas("atlas.png", "wave_banner.0009"),
            Sprite.from_atlas("atlas.png", "wave_banner.0010"),
        ]

        self.visible = False

    def start(self) -> None:
        self.game_manager = self.find("GameManager")
        self.x = -320

    def draw(self, camera: Camera) -> None:
        if self.visible:
            try:
                self.sprite = self.sprites[self.game_manager.wave]
            except:
                self.sprite = Sprite.empty()

            self.sprite.draw(camera, self.position())

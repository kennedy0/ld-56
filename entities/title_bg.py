from potion import *


class TitleBg(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.sprite = Sprite.from_atlas("atlas.png", "title_bg")

    def draw(self, camera: Camera) -> None:
        self.sprite.draw(camera, self.position())
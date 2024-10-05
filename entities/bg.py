from potion import *


class Bg(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.z = 1000
        self.sprite = Sprite("ldtk/bg.png")

    def draw(self, camera: Camera) -> None:
        self.sprite.draw(camera, self.position())

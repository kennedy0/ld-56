import random

from potion import *


class Rock(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.tags.add("Rock")
        self.collisions_enabled = True
        self.solid = True

        sprite_name = random.choice([
            "rock_a",
            "rock_b",
            "rock_c",
            "rock_d",
            "rock_e",
            "rock_f",
        ])

        self.sprite = Sprite.from_atlas("atlas.png", sprite_name)
        self.sprite.pivot.set_center()

    def bbox(self) -> Rect:
        return Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

    def start(self) -> None:
        self.z = self.y * -1

    def draw(self, camera: Camera) -> None:
        self.sprite.draw(camera, self.position())

    def debug_draw(self, camera: Camera) -> None:
        self.bbox().draw(camera, Color.red())

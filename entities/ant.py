from potion import *

from entities.bug import Bug


class Ant(Bug):
    def __init__(self) -> None:
        super().__init__()

        self.move_speed = 5

        # Sprite
        self.sprite = AnimatedSprite.from_atlas("atlas.png", "ant")
        self.sprite.pivot.set_bottom_center()

        self.shadow_sprite = Sprite.from_atlas("atlas.png", "ant_shadow")
        self.shadow_sprite.pivot.set_center()
        self.shadow_sprite.opacity = 64

from potion import *

from entities.bug import Bug
from entities.fast_ant_splat import FastAntSplat


class FastAnt(Bug):
    def __init__(self) -> None:
        super().__init__()

        self.move_speed = 4

        # Sprite
        self.sprite = AnimatedSprite.from_atlas("atlas.png", "fast_ant")
        self.sprite.pivot.set_bottom_center()

        self.shadow_sprite = Sprite.from_atlas("atlas.png", "ant_shadow")
        self.shadow_sprite.pivot.set_center()
        self.shadow_sprite.opacity = 64

        self.splat = FastAntSplat

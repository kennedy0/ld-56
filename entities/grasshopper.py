import random

from potion import *

from entities.bug import Bug
from entities.grasshopper_splat import GrasshopperSplat


class Grasshopper(Bug):
    def __init__(self) -> None:
        super().__init__()

        self.move_speed = 2

        self.walk_speed = 1
        self.fly_speed = 4

        # Sprite
        self.sprite = AnimatedSprite.from_atlas("atlas.png", "grasshopper")
        self.sprite.pivot.set_bottom_center()

        self.shadow_sprite = Sprite.from_atlas("atlas.png", "ant_shadow")
        self.shadow_sprite.pivot.set_center()
        self.shadow_sprite.opacity = 64

        self.splat = GrasshopperSplat

        self.jump_timer_max = 5
        self.jump_timer = self.jump_timer_max

        self.fly_timer = 0
        self.fly_timer_max = 2

    def start(self) -> None:
        super().start()
        self.jump_timer + random.uniform(-1.5, 1.5)

    def update(self) -> None:
        super().update()

        self.jump_timer -= Time.delta_time
        if self.jump_timer < 0:
            self.jump_timer = self.jump_timer_max
            self.fly_timer = self.fly_timer_max

        self.fly_timer -= Time.delta_time
        if self.fly_timer < 0:
            self.fly_timer = 0

        if self.fly_timer > 0:
            if self.fly_timer > 1.5:
                t = pmath.remap(self.fly_timer, 2.0, 1.5, 0, 1)
                y = pmath.lerp(0, -14, t)
                self.sprite_offset = Point(0, y)
            elif self.fly_timer < .5:
                t = pmath.remap(self.fly_timer, 0.5, 0, 0, 1)
                y = pmath.lerp(-14, 0, t)
                self.sprite_offset = Point(0, y)
            else:
                self.sprite_offset = Point(0, -14)
            self.move_speed = self.fly_speed
        else:
            self.sprite_offset = Point.zero()
            self.move_speed = self.walk_speed

    def update_animation(self) -> None:
        self.sprite.update()

        if self.mx or self.my:
            if self.fly_timer:
                self.sprite.play("Fly")
            else:
                self.sprite.play("Run")
        elif self.done_moving:
            self.sprite.play("Attack")
        else:
            self.sprite.play("Idle")

        if self.mx > 0:
            self.sprite.flip_horizontal = False
        elif self.mx < 0:
            self.sprite.flip_horizontal = True

        if self.done_moving:
            if self.apple.x > self.x:
                self.sprite.flip_horizontal = False
            elif self.apple.x < self.x:
                self.sprite.flip_horizontal = True

    def kill(self) -> None:
        if self.fly_timer > 0:
            return

        super().kill()

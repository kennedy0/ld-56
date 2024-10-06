import random

from potion import *

from entities.bug import Bug
from entities.ladybug_splat import LadybugSplat


class Ladybug(Bug):
    def __init__(self) -> None:
        super().__init__()
        self.tags.add("Rock")

        self.move_speed = 1

        # Sprite
        self.sprite = AnimatedSprite.from_atlas("atlas.png", "ladybug")
        self.sprite.pivot.set_bottom_center()

        self.shadow_sprite = Sprite.from_atlas("atlas.png", "ant_shadow")
        self.shadow_sprite.pivot.set_center()
        self.shadow_sprite.opacity = 64

        self.splat = LadybugSplat

        self.shell_cooldown_timer = 0
        self.shell_cooldown_max_timer = 7

        self.shell_timer = 0
        self.shell_max_timer = 5

        self.width = 4
        self.height = 4

    def bbox(self) -> Rect:
        return Rect(self.x - self.width // 2, self.y - self.width // 2, self.width, self.height)

    def start(self) -> None:
        super().start()

    def update(self) -> None:
        super().update()

        self.shell_timer -= Time.delta_time
        if self.shell_timer < 0:
            self.shell_timer = 0

        self.shell_cooldown_timer -= Time.delta_time
        if self.shell_cooldown_timer < 0:
            self.shell_cooldown_timer = 0

        if self.shell_timer > 0:
            self.collisions_enabled = True
            self.solid = True

        else:
            self.collisions_enabled = False
            self.solid = False

    def update_movement(self) -> None:
        if self.shell_timer > 0:
            return

        super().update_movement()

    def update_animation(self) -> None:
        self.sprite.update()

        if self.shell_timer == 0 and self.shell_cooldown_timer > 0:
            if (Engine.frame() // 8) % 2 == 0:
                self.sprite.flash_opacity = 128
                self.sprite.flash_color = Color.red()
            else:
                self.sprite.flash_opacity = 0
        else:
            self.sprite.flash_opacity = 0

        if self.shell_timer > 0:
            self.sprite.play("Hide")
        elif self.mx or self.my:
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
        if self.shell_cooldown_timer <= 0:
            self.shell_cooldown_timer = self.shell_cooldown_max_timer
            self.shell_timer = self.shell_max_timer + random.uniform(-1.5, 1.5)

        if self.shell_timer > 0:
            return

        super().kill()

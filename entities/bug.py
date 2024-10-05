from potion import *

from entities.actor import Actor


class Bug(Actor):
    def __init__(self) -> None:
        super().__init__()

        # Sprite
        self.sprite = AnimatedSprite.from_atlas("atlas.png", "ant")
        self.sprite.pivot.set_bottom_center()

        self.shadow_sprite = Sprite.from_atlas("atlas.png", "ant_shadow")
        self.shadow_sprite.pivot.set_center()
        self.shadow_sprite.opacity = 64

    def update(self) -> None:
        super().update()
        self.update_move_target()
        self.update_animation()

    def update_move_target(self) -> None:
        if Mouse.get_right_mouse_down():
            self.set_move_target(Mouse.world_position())

    def update_animation(self) -> None:
        self.sprite.update()

        if self.mx or self.my:
            self.sprite.play("Run")
        else:
            self.sprite.play("Idle")

        if self.mx > 0:
            self.sprite.flip_horizontal = False
        elif self.mx < 0:
            self.sprite.flip_horizontal = True

    def draw(self, camera: Camera) -> None:
        self.shadow_sprite.draw(camera, self.position())
        self.sprite.draw(camera, self.position())

    def debug_draw(self, camera: Camera) -> None:
        if self.move_target:
            Circle(self.position().x, self.position().y, self.stop_distance_to_move_target).draw(camera, Color.cyan())
            Line(self.position(), self.move_target).draw(camera, Color.blue())
            self.move_target.draw(camera, Color.red())
        self.position().draw(camera, Color.red())


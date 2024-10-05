from potion import *


class Bug(Entity):
    def __init__(self) -> None:
        super().__init__()

        # Sprite
        self.sprite = AnimatedSprite.from_atlas("atlas.png", "ant")
        self.sprite.pivot.set_bottom_center()

        self.shadow_sprite = Sprite.from_atlas("atlas.png", "ant_shadow")
        self.shadow_sprite.pivot.set_center()
        self.shadow_sprite.opacity = 64

        # Movement
        self.move_frame = 0
        self.move_speed = 1
        self.move_target: Point | None = None
        self.stop_at_distance_to_target = 4
        self.mx = 0
        self.my = 0

    def update(self) -> None:
        super().update()
        self.update_move_target()
        self.update_movement()
        self.zsort()
        self.update_animation()

    def update_move_target(self) -> None:
        if Mouse.get_right_mouse_down():
            self.move_target = Mouse.world_position()

    def update_movement(self) -> None:
        if self.move_target:
            # Stop moving if we're close to the target
            delta = self.move_target - self.position()
            distance = delta.to_vector2().length()
            if distance < self.stop_at_distance_to_target:
                self.move_target = None
                self.mx = 0
                self.my = 0
                return

            # Snap movement to 8 directions
            self.mx = 0
            self.my = 0
            dx, dy = delta
            if dx:
                self.mx = pmath.sign(dx)
                if abs(dx) > 1:
                    self.mx *= 2
            if dy:
                self.my = pmath.sign(dy)

            # Accumulate move frames
            self.move_frame += 1

            # Figure out movement frames based on move speed:
            if self.move_speed == 0:
                frame_threshold = 0
                self.move_frame = 0
                self.mx = 0
                self.my = 0
            elif self.move_speed == 1:
                frame_threshold = 8
            elif self.move_speed == 2:
                frame_threshold = 6
            elif self.move_speed == 3:
                frame_threshold = 4
            elif self.move_speed == 4:
                frame_threshold = 2
            else:
                frame_threshold = 1

            # Move if we've accumulated enough frames
            if self.move_frame >= frame_threshold:
                self.move_frame = 0
                if self.mx:
                    self.move_x(self.mx)
                if self.my:
                    self.move_y(self.my)

    def zsort(self) -> None:
        self.z = self.y * -1

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
            Circle(self.position().x, self.position().y, self.stop_at_distance_to_target).draw(camera, Color.cyan())
            Line(self.position(), self.move_target).draw(camera, Color.blue())
            self.move_target.draw(camera, Color.red())
        self.position().draw(camera, Color.red())


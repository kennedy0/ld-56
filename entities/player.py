from potion import *


class Player(Entity):
    def __init__(self) -> None:
        super().__init__()

        # Sprite
        self.sprite = AnimatedSprite.from_atlas("atlas.png", "player")
        self.sprite.pivot.set_bottom_center()
        self.gun_sprite = Sprite.from_atlas("atlas.png", "gun")
        self.gun_sprite.pivot.set_center_left()

        # Move
        self.move_speed = 1
        self.mx = 0
        self.my = 0
        self.fractional_move_frames = 0
        self.fractional_move_counter = 0
        self.fractional_move_axis: str | None = None
        self.move_target: Point | None = None
        self.stop_distance_to_move_target = 5

    def update(self) -> None:
        self.sprite.update()
        self.update_move_target()
        self.update_movement()
        self.update_animation()

    def update_move_target(self) -> None:
        if Mouse.get_left_mouse_down():
            self.set_move_target(Mouse.world_position())

    def set_move_target(self, target: Point) -> None:
        # Update the target
        self.move_target = target

        # Calculate delta
        move_delta = self.move_target - self.position()
        self.mx = pmath.sign(move_delta.x)
        self.my = pmath.sign(move_delta.y)

        # Figure out fractional movement for smoothness
        self.fractional_move_counter = 0
        self.fractional_move_axis = None
        if move_delta.x and move_delta.y:
            if abs(move_delta.x) > abs(move_delta.y):
                self.fractional_move_axis = "y"
                self.fractional_move_frames = abs(move_delta.x / move_delta.y)
            elif abs(move_delta.y) > abs(move_delta.x):
                self.fractional_move_axis = "x"
                self.fractional_move_frames = abs(move_delta.y / move_delta.x)

    def update_movement(self) -> None:
        if self.move_target:
            # Stop moving if close to move target
            if self.position().distance_to(self.move_target) < self.stop_distance_to_move_target:
                self.move_target = None
                self.mx = 0
                self.my = 0
                return

            # Figure out movement this frame
            self.fractional_move_counter += 1
            x = 0
            y = 0

            if self.fractional_move_axis == "x":
                y = self.my
                if self.fractional_move_counter > self.fractional_move_frames:
                    self.fractional_move_counter -= self.fractional_move_frames
                    x = self.mx
            elif self.fractional_move_axis == "y":
                x = self.mx
                if self.fractional_move_counter > self.fractional_move_frames:
                    self.fractional_move_counter -= self.fractional_move_frames
                    y = self.my
            else:
                x = self.mx
                y = self.my

            # Move the player
            self.x += x
            self.y += y

    def update_animation(self) -> None:
        if self.mx or self.my:
            self.sprite.play("Run")
        else:
            self.sprite.play("Idle")

        if self.mx > 0:
            self.sprite.flip_horizontal = False
        elif self.mx < 0:
            self.sprite.flip_horizontal = True

    def draw(self, camera: Camera) -> None:
        self.sprite.draw(camera, self.position())

    def debug_draw(self, camera: Camera) -> None:
        if self.move_target:
            Circle(self.position().x, self.position().y, self.stop_distance_to_move_target).draw(camera, Color.cyan())
            Line(self.position(), self.move_target).draw(camera, Color.blue())
            self.move_target.draw(camera, Color.red())
        self.position().draw(camera, Color.red())


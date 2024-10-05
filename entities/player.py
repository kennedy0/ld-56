from potion import *


class Player(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Player"

        # Sprite
        self.sprite = AnimatedSprite.from_atlas("atlas.png", "player")
        self.sprite.pivot.set_center()

        # Movement
        self.move_input_timer = 0
        self.move_input = False
        self.move_direction = Vector2.zero()
        self.move_speed = 0
        self.max_move_speed = 1
        self.brake_multiplier = 2

        self.move_frame = 0
        self.move_target: Point | None = None
        self.mx = 0
        self.my = 0

    def update(self) -> None:
        self.update_move_input()
        self.update_move_direction()
        self.update_movement()
        self.zsort()

    def update_move_input(self) -> None:
        if Mouse.get_left_mouse():
            self.move_input = True
            self.move_target = Mouse.world_position()
        else:
            self.move_input = False

    def update_move_direction(self) -> None:
        if self.move_input:
            delta = (Mouse.world_position() - self.position()).to_vector2().normalized()
            self.move_direction = delta

    def update_movement(self) -> None:
        # Accelerate when input movement is held
        if self.move_input:
            self.move_speed += Time.delta_time
        else:
            self.move_speed -= Time.delta_time * self.brake_multiplier

        # Clamp move speed
        self.move_speed = pmath.clamp(self.move_speed, 0, self.max_move_speed)

        # Get movement amount
        self.mx = self.move_direction.x * self.move_speed
        self.my = self.move_direction.y * self.move_speed

        # Move
        if self.mx:
            self.move_x(self.mx)
        if self.my:
            self.move_y(self.my)

        return

        # Clamp move timer
        self.move_input_timer = pmath.clamp(self.move_input_timer, 0, 10)

        # Set move speed
        if self.move_input_timer == 0:
            self.move_speed = 0
        elif self.move_input_timer < 1:
            self.move_speed = 1
        elif self.move_input_timer < 3:
            self.move_speed = 2
        elif self.move_input_timer < 6:
            self.move_speed = 3
        elif self.move_input_timer < 10:
            self.move_speed = 4
        else:
            self.move_speed = 5

        # Get move direction
        self.mx = 1
        self.my = 0

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

    def draw(self, camera: Camera) -> None:
        self.sprite.draw(camera, self.position())

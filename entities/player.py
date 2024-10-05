from potion import *


class Player(Entity):
    def __init__(self) -> None:
        super().__init__()

        # Sprite
        self.sprite = AnimatedSprite.from_atlas("atlas.png", "player")
        self.sprite.pivot.set_center()

        # Movement
        self.move_input = False
        self.move_frame = 0
        self.move_speed = 2
        self.move_target: Point | None = None
        self.mx = 0
        self.my = 0

    def update(self) -> None:
        self.handle_input()
        self.update_movement()
        self.zsort()

    def handle_input(self) -> None:
        if Mouse.get_left_mouse():
            self.move_input = True
            self.move_target = Mouse.world_position()
        else:
            self.move_input = False

    def update_movement(self) -> None:
        if self.move_input:
            pass

        if self.move_target:
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

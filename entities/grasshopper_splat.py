from potion import *


class GrasshopperSplat(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.sprite = Sprite.from_atlas("atlas.png", "grashopper_splat")
        self.sprite.pivot.set_center()
        self.timer = 2

    def start(self) -> None:
        self.z = 0 - self.y  + 20
        self.sprite.flip_horizontal = pmath.random_bool()
        self.sprite.flip_vertical = pmath.random_bool()

    def update(self) -> None:
        self.timer -= Time.delta_time
        if self.timer < 1:
            self.sprite.opacity = int(pmath.lerp(0, 255, self.timer))
        if self.timer <= 0:
            self.destroy()

    def draw(self, camera: Camera) -> None:
        self.sprite.draw(camera, self.position())
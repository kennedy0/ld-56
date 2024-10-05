from __future__ import annotations

from potion import *


if TYPE_CHECKING:
    from entities.player import Player


class CameraController(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.player: Player | None = None
        self.camera_speed = 1
        self.epsilon_x = 20
        self.epsilon_y = 10
        self.x_min = 0
        self.x_max = 0
        self.y_min = 0
        self.y_max = 0

    def start(self) -> None:
        self.player = self.find("Player")
        self.x_min = -400
        self.x_max = 400 - self.scene.main_camera.resolution[0]
        self.y_min = -200
        self.y_max = 200 - self.scene.main_camera.resolution[1]

    def update(self) -> None:
        delta = self.player.position().to_vector2() - self.scene.main_camera.center()
        dx, dy = delta
        nx, ny = delta.normalized()

        if abs(dx) > self.epsilon_x:
            self.scene.main_camera.x += nx
        if abs(dy) > self.epsilon_y:
            self.scene.main_camera.y += ny

        self.scene.main_camera.x = pmath.clamp(self.scene.main_camera.x, self.x_min, self.x_max)
        self.scene.main_camera.y = pmath.clamp(self.scene.main_camera.y, self.y_min, self.y_max)

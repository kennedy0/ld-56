from __future__ import annotations

from potion import *


if TYPE_CHECKING:
    from entities.player import Player


class CameraController(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "CameraController"
        self.target_point: Point | None = None
        self.player: Player | None = None
        self.epsilon_x = 10
        self.epsilon_y = 5

    def start(self) -> None:
        self.player = self.find("Player")

    def update(self) -> None:
        if self.target_point:
            delta = self.target_point.to_vector2() - self.scene.main_camera.center()
        else:
            delta = self.player.position().to_vector2() - self.scene.main_camera.center()

        dx = abs(delta.x)
        dy = abs(delta.y)
        nx, ny = delta.normalized()

        if self.target_point:
            if abs(dx) > nx:
                self.scene.main_camera.x += nx
            if abs(dy) > ny:
                self.scene.main_camera.y += ny
        else:
            if abs(dx) > self.epsilon_x:
                self.scene.main_camera.x += nx
            if abs(dy) > self.epsilon_y:
                self.scene.main_camera.y += ny

        self.scene.main_camera.x = pmath.clamp(self.scene.main_camera.x, 0, 480)
        self.scene.main_camera.y = pmath.clamp(self.scene.main_camera.y, 0, 220)

    def in_range_of_target(self) -> bool:
        if self.target_point:
            if self.scene.main_camera.center().distance_to(self.target_point.to_vector2()) < 4:
                return True

        return False

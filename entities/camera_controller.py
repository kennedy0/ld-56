from __future__ import annotations

from potion import *


if TYPE_CHECKING:
    from entities.player import Player


class CameraController(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.player: Player | None = None
        self.epsilon_x = 10
        self.epsilon_y = 5

    def start(self) -> None:
        self.player = self.find("Player")

    def update(self) -> None:
        delta = self.player.position().to_vector2() - self.scene.main_camera.center()
        dx = abs(delta.x)
        dy = abs(delta.y)
        nx, ny = delta.normalized()

        if abs(dx) > self.epsilon_x:
            self.scene.main_camera.x += nx
        if abs(dy) > self.epsilon_y:
            self.scene.main_camera.y += ny

        self.scene.main_camera.x = pmath.clamp(self.scene.main_camera.x, 0, 480)
        self.scene.main_camera.y = pmath.clamp(self.scene.main_camera.y, 0, 220)

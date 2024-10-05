from potion import *

from entities.player import Player


class MainScene(Scene):
    def setup_cameras(self) -> None:
        self.main_camera.x -= self.main_camera.resolution[0] / 2
        self.main_camera.y -= self.main_camera.resolution[1] / 2

    def load_entities(self) -> None:
        self.entities.add(Player())

from potion import *

from entities.bg import Bg
from entities.bug import Bug
from entities.camera_controller import CameraController
from entities.player import Player


class MainScene(Scene):
    def setup_cameras(self) -> None:
        self.main_camera.x -= self.main_camera.resolution[0] / 2
        self.main_camera.y -= self.main_camera.resolution[1] / 2

    def load_entities(self) -> None:
        LDtk.load_simplified(self, "ldtk/picnic.ldtk")
        for ldtk_entity in LDtk.ldtk_entities(self):
            print(ldtk_entity)

        self.entities.add(CameraController())
        self.entities.add(Bg())
        self.entities.add(Player())

        bug = Bug()
        bug.x = 50
        self.entities.add(bug)

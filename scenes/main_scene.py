from potion import *

from entities.bg import Bg
from entities.bug_spawner import BugSpawner
from entities.camera_controller import CameraController
from entities.game_manager import GameManager
from entities.player import Player


class MainScene(Scene):
    def setup_cameras(self) -> None:
        self.main_camera.x -= self.main_camera.resolution[0] / 2
        self.main_camera.y -= self.main_camera.resolution[1] / 2

    def load_entities(self) -> None:
        self.entities.add(GameManager())
        self.entities.add(CameraController())
        self.entities.add(Bg())
        self.entities.add(Player())

        # Create bug spawners
        bug_spawner_top_left = BugSpawner()
        bug_spawner_top_left.name = "BugSpawnerTopLeft"
        bug_spawner_top_left.x = -400
        bug_spawner_top_left.y = -200
        self.entities.add(bug_spawner_top_left)

        bug_spawner_top_right = BugSpawner()
        bug_spawner_top_right.name = "BugSpawnerTopRight"
        bug_spawner_top_right.x = 400
        bug_spawner_top_right.y = -200
        self.entities.add(bug_spawner_top_right)

        bug_spawner_bottom_left = BugSpawner()
        bug_spawner_bottom_left.name = "BugSpawnerBottomLeft"
        bug_spawner_bottom_left.x = -400
        bug_spawner_bottom_left.y = 200
        self.entities.add(bug_spawner_bottom_left)

        bug_spawner_bottom_right = BugSpawner()
        bug_spawner_bottom_right.name = "BugSpawnerBottomRight"
        bug_spawner_bottom_right.x = 400
        bug_spawner_bottom_right.y = 200
        self.entities.add(bug_spawner_bottom_right)

        # Load LDtk
        LDtk.load_simplified(self, "ldtk/picnic.ldtk")
        for ldtk_entity in LDtk.ldtk_entities(self):
            if ldtk_entity.name.startswith("Path-"):
                name = ldtk_entity.metadata['ldtk_custom_fields']['Name']
                waypoints = ldtk_entity.metadata['ldtk_custom_fields']['Waypoints']

                match name:
                    case "Path1":
                        for waypoint in waypoints:
                            x = waypoint['cx'] - 400
                            y = waypoint['cy'] - 200
                            bug_spawner_top_left.waypoints.append(Point(x, y))
                        pass
                    case _:
                        Log.error(f"Path is not implemented: {name}")

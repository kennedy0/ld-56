from __future__ import annotations

from potion import *

if TYPE_CHECKING:
    from entities.bug import Bug
    from entities.game_manager import GameManager


class BugSpawner(Entity):
    def __init__(self) -> None:
        super().__init__()

        self.game_manager: GameManager | None = None

        self.waypoints: list[Point] = []

        # BottomLeft
        self.waypoints_4: list[Point] = []
        self.waypoints_5: list[Point] = []
        self.waypoints_6: list[Point] = []

        # BottomRight
        self.waypoints_7: list[Point] = []
        self.waypoints_8: list[Point] = []
        self.waypoints_9: list[Point] = []

    def start(self) -> None:
        self.game_manager = self.find("GameManager")

    def spawn(self, bug_class: type[Bug], alt_waypoints: str | None = None) -> None:
        """ Spawn Bugs. """
        if alt_waypoints == "4":
            waypoints = self.waypoints_4
        elif alt_waypoints == "5":
            waypoints = self.waypoints_5
        elif alt_waypoints == "6":
            waypoints = self.waypoints_6
        elif alt_waypoints == "7":
            waypoints = self.waypoints_7
        elif alt_waypoints == "8":
            waypoints = self.waypoints_8
        elif alt_waypoints == "9":
            waypoints = self.waypoints_9
        else:
            waypoints = self.waypoints

        bug = bug_class()
        bug.set_position(self.position())
        bug.waypoints = [w for w in waypoints]

        self.scene.entities.add(bug)
        self.game_manager.bugs_this_wave += 1

    def debug_draw(self, camera: Camera) -> None:
        w_lists = [self.waypoints,
                   self.waypoints_4, self.waypoints_5, self.waypoints_6,
                   self.waypoints_7, self.waypoints_8, self.waypoints_9]

        for wlist in w_lists:
            if not wlist:
                continue

            for i, waypoint in enumerate(wlist):
                waypoint.draw(camera, Color.white())

                if i + 1 < len(wlist):
                    next_waypoint = wlist[i+1]
                    Line(waypoint, next_waypoint).draw(camera, Color.red())

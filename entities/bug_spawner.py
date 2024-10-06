from __future__ import annotations

from potion import *

from entities.ant import Ant

if TYPE_CHECKING:
    from entities.bug import Bug


class BugSpawner(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.waypoints: list[Point] = []

        # BottomLeft
        self.waypoints_4: list[Point] = []
        self.waypoints_5: list[Point] = []
        self.waypoints_6: list[Point] = []

        # BottomRight
        self.waypoints_7: list[Point] = []
        self.waypoints_8: list[Point] = []
        self.waypoints_9: list[Point] = []

    def spawn(self, bugs: list[str]) -> None:
        """ Spawn Bugs. """
        for i, bug in enumerate(bugs):
            delay = i
            match bug:
                case "ant":
                    start_coroutine(self._spawn_bug(delay, Ant))

    def _spawn_bug(self, delay: float, bug_class: type[Bug]) -> Generator:
        yield from wait_for_seconds(delay)
        bug = bug_class()
        bug.set_position(self.position())
        bug.waypoints = [w for w in self.waypoints]
        self.scene.entities.add(bug)

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

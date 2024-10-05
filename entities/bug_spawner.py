from __future__ import annotations

from potion import *

from entities.ant import Ant

if TYPE_CHECKING:
    from entities.bug import Bug


class BugSpawner(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.waypoints: list[Point] = []

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
        for waypoint in self.waypoints:
            waypoint.draw(camera, Color.white())

from __future__ import annotations

import random

from potion import *

from entities.ant_splat import AntSplat

if TYPE_CHECKING:
    from entities.apple import Apple
    from entities.game_manager import GameManager


class Bug(Entity):
    def __init__(self) -> None:
        super().__init__()

        # Entity references
        self.apple: Apple | None = None
        self.game_manager: GameManager | None = None

        # Sprite
        self.sprite = AnimatedSprite.empty()
        self.shadow_sprite = Sprite.empty()

        # Movement
        self.move_frame = 0
        self.move_speed = 1
        self.move_target: Point | None = None
        self.stop_at_distance_to_target = 4
        self.mx = 0
        self.my = 0

        # Pathfinding
        self.waypoints: list[Point] = []
        self.has_final_target = False
        self.is_at_final_target = False
        self.done_moving = False

        self.final_points = [
            Point(360, 179),
            Point(440, 179),
            Point(360, 219),
            Point(440, 219),
        ]

        # Collision
        self.radius = 6

        # Death
        self.dead = False

    def start(self) -> None:
        self.apple = self.find("Apple")
        self.game_manager = self.find("GameManager")
        self.game_manager.bugs.append(self)

    def update(self) -> None:
        super().update()
        self.update_move_target()
        self.update_movement()
        self.zsort()
        self.update_animation()
        self.update_attack()

    def update_move_target(self) -> None:
        if self.done_moving:
            return

        # Move to the next waypoint
        if not self.move_target and self.waypoints:
            self.move_target = self.waypoints.pop(0)

        # If we don't have a final target, get one
        elif not self.move_target and not self.has_final_target:
            self.move_target = self.get_final_target()
            self.has_final_target = True

        # At this point, we are at the final target
        # Make sure we're not standing on top of another bug
        elif not self.move_target and self.is_at_final_target:
            for other_bug in self.game_manager.bugs:
                if other_bug == self:
                    continue
                distance_to_bug = other_bug.position().distance_to(self.position())
                if distance_to_bug < self.radius + other_bug.radius:
                    x = self.x + random.randint(-20, 20)
                    y = self.y + random.randint(-10, 10)
                    self.move_target = Point(x, y)
                    return

            # Make sure we're not too close to the apple
            distance_to_apple = self.apple.position().distance_to(self.position())
            if distance_to_apple < 30:
                x = self.x + random.randint(-20, 20)
                y = self.y + random.randint(-10, 10)
                self.move_target = Point(x, y)
                return

            # If we got all the way here, we're done moving. Hooray!!!
            self.done_moving = True

    def get_final_target(self) -> Point:
        # Get the closest final point
        closest_point = None
        closest_distance = 9999
        for point in self.final_points:
            if closest_point is None:
                closest_point = point
                closest_distance = self.position().distance_to(point)
            else:
                this_distance = self.position().distance_to(point)
                if this_distance < closest_distance:
                    closest_point = point
                    closest_distance = this_distance

        return closest_point

    def update_movement(self) -> None:
        if self.move_target:
            # Stop moving if we're close to the target
            delta = self.move_target - self.position()
            distance = delta.to_vector2().length()
            if distance < self.stop_at_distance_to_target:
                self.move_target = None
                self.mx = 0
                self.my = 0
                if self.has_final_target:
                    self.is_at_final_target = True
                return

            # Snap movement to 8 directions
            self.mx = 0
            self.my = 0
            dx, dy = delta
            if dx:
                self.mx = pmath.sign(dx)
                if abs(dx) > 1:
                    self.mx *= 2
            if dy:
                self.my = pmath.sign(dy)

            # Accumulate move frames
            self.move_frame += 1

            # Figure out movement frames based on move speed:
            if self.move_speed == 0:
                frame_threshold = 0
                self.move_frame = 0
                self.mx = 0
                self.my = 0
            elif self.move_speed == 1:
                frame_threshold = 8
            elif self.move_speed == 2:
                frame_threshold = 6
            elif self.move_speed == 3:
                frame_threshold = 4
            elif self.move_speed == 4:
                frame_threshold = 2
            else:
                frame_threshold = 1

            # Move if we've accumulated enough frames
            if self.move_frame >= frame_threshold:
                self.move_frame = 0
                if self.mx:
                    self.x += self.mx
                if self.my:
                    self.y += self.my

    def zsort(self) -> None:
        self.z = self.y * -1

    def update_animation(self) -> None:
        self.sprite.update()

        if self.mx or self.my:
            self.sprite.play("Run")
        elif self.done_moving:
            self.sprite.play("Attack")
        else:
            self.sprite.play("Idle")

        if self.mx > 0:
            self.sprite.flip_horizontal = False
        elif self.mx < 0:
            self.sprite.flip_horizontal = True

        if self.done_moving:
            if self.apple.x > self.x:
                self.sprite.flip_horizontal = False
            elif self.apple.x < self.x:
                self.sprite.flip_horizontal = True

    def update_attack(self) -> None:
        if self.sprite.animation == "Attack" and self.sprite.frame_started(2):
            self.apple.hp -= 1

    def kill(self) -> None:
        self.dead = True

        try:
            self.game_manager.bugs.remove(self)
        except:
            Log.warning(f"Could not remove {self} from game manager")

        self.destroy()

        ant_splat = AntSplat()
        ant_splat.set_position(self.position())
        self.scene.entities.add(ant_splat)

    def draw(self, camera: Camera) -> None:
        self.shadow_sprite.draw(camera, self.position())
        self.sprite.draw(camera, self.position())

    def debug_draw(self, camera: Camera) -> None:
        if self.move_target:
            Circle(self.position().x, self.position().y, self.stop_at_distance_to_target).draw(camera, Color.cyan())
            Line(self.position(), self.move_target).draw(camera, Color.blue())
            self.move_target.draw(camera, Color.red())
        self.position().draw(camera, Color.red())

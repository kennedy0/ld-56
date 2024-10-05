from __future__ import annotations

import random

from entities.game_manager import GameManager
from potion import *

from entities.ant_splat import AntSplat


class Bug(Entity):
    def __init__(self) -> None:
        super().__init__()

        # Entity references
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

        # Collision
        self.radius = 6

    def start(self) -> None:
        self.game_manager = self.find("GameManager")
        self.game_manager.bugs.append(self)

    def update(self) -> None:
        super().update()
        self.update_move_target()
        self.update_movement()
        self.zsort()
        self.update_animation()

    def update_move_target(self) -> None:
        if not self.move_target:
            # Move to the next waypoint
            if self.waypoints:
                self.move_target = self.waypoints.pop(0)

            # Don't stand right on top of another bug
            else:
                for other_bug in self.game_manager.bugs:
                    if other_bug == self:
                        continue
                    distance = other_bug.position().distance_to(self.position())
                    if distance < self.radius + other_bug.radius:
                        x = self.x + random.randint(-20, 20)
                        y = self.y + random.randint(-10, 10)
                        self.move_target = Point(x, y)

    def update_movement(self) -> None:
        if self.move_target:
            # Stop moving if we're close to the target
            delta = self.move_target - self.position()
            distance = delta.to_vector2().length()
            if distance < self.stop_at_distance_to_target:
                self.move_target = None
                self.mx = 0
                self.my = 0
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
        else:
            self.sprite.play("Idle")

        if self.mx > 0:
            self.sprite.flip_horizontal = False
        elif self.mx < 0:
            self.sprite.flip_horizontal = True

    def kill(self) -> None:
        self.game_manager.bugs.remove(self)
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

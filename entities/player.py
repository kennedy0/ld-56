from __future__ import annotations

from math import atan2, degrees

from potion import *

if TYPE_CHECKING:
    from entities.game_manager import GameManager


class Player(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Player"

        # Entity references
        self.game_manager: GameManager | None = None

        # Sprite
        self.sprite = Sprite.empty()
        self.sprites = [
            Sprite.from_atlas("atlas.png", "player.0001"),
            Sprite.from_atlas("atlas.png", "player.0002"),
            Sprite.from_atlas("atlas.png", "player.0003"),
            Sprite.from_atlas("atlas.png", "player.0004"),
            Sprite.from_atlas("atlas.png", "player.0005"),
            Sprite.from_atlas("atlas.png", "player.0006"),
            Sprite.from_atlas("atlas.png", "player.0007"),
            Sprite.from_atlas("atlas.png", "player.0008"),
        ]
        for s in self.sprites:
            s.pivot.set_center()

        # Movement
        self.move_input = False
        self.move_input_timer = 0
        self.move_direction = Vector2.zero()
        self.move_speed = 0
        self.max_move_speed = 1
        self.brake_multiplier = 2
        self.mx = 0
        self.my = 0
        self.facing_angle = 0

        # Collision
        self.collisions_enabled = True
        self.width = 20
        self.height = 10
        self.radius = 10

        self.water_rect = Rect(517, 41, 217, 118)
        self.water_radius = 32
        self.water_points = [
            Point(550, 106),
            Point(667, 111),
            Point(593, 128),
            Point(703, 75),
            Point(644, 76),
            Point(580, 111),
            Point(613, 103),
            Point(672, 73),
            Point(628, 117),
            Point(687, 92),
            Point(647, 115),
            Point(610, 124),
            Point(568, 121),
            Point(593, 108),
            Point(566, 112),
            Point(630, 90),
            Point(658, 74),
            Point(690, 73),
        ]

    def start(self) -> None:
        self.game_manager = self.find("GameManager")

        self.x = 400
        self.y = 200

    def bbox(self) -> Rect:
        return Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

    def update(self) -> None:
        self.update_move_input()
        self.update_move_direction()
        self.update_movement()
        self.update_facing_angle()
        self.handle_bug_collisions()
        self.handle_water_collision()
        self.update_sprite()
        self.zsort()

    def update_move_input(self) -> None:
        if Mouse.get_left_mouse():
            self.move_input = True
        else:
            self.move_input = False

    def update_move_direction(self) -> None:
        if self.move_input:
            delta = (Mouse.world_position() - self.position()).to_vector2().normalized()
            self.move_direction = delta

    def update_movement(self) -> None:
        # Accelerate when input movement is held
        if self.move_input:
            self.move_speed += Time.delta_time
        else:
            self.move_speed -= Time.delta_time * self.brake_multiplier

        # Clamp move speed
        self.move_speed = pmath.clamp(self.move_speed, 0, self.max_move_speed)

        # Get movement amount
        self.mx = self.move_direction.x * self.move_speed
        self.my = self.move_direction.y * self.move_speed

        # Move
        if self.mx:
            self.move_x(self.mx)
        if self.my:
            self.move_y(self.my)

        self.x = pmath.clamp(self.x, 0, 800)
        self.y = pmath.clamp(self.y, 0, 400)

    def handle_bug_collisions(self) -> None:
        for bug in self.game_manager.bugs:
            d = self.position().distance_to(bug.position())
            if d < self.radius + bug.radius:
                bug.kill()

    def handle_water_collision(self) -> None:
        player_p = self.position()
        if self.water_rect.contains_point(player_p):
            distances = [p.distance_to(player_p) for p in self.water_points]
            if min(distances) < self.water_radius:
                print("WATER")

    def update_facing_angle(self) -> None:
        self.facing_angle = degrees(atan2(self.move_direction.y, self.move_direction.x))

    def update_sprite(self) -> None:
        self.sprite.frame = int(Engine.frame() % 4)

        if -13 < self.facing_angle < 13:
            i = 0
        elif 13 < self.facing_angle < 60:
            i = 1
        elif 60 < self.facing_angle < 120:
            i = 2
        elif 120 < self.facing_angle < 167:
            i = 3
        elif 167 < self.facing_angle <= 180:
            i = 4
        elif self.facing_angle <= -167:
            i = 4
        elif self.facing_angle <= -120:
            i = 5
        elif self.facing_angle <= -60:
            i = 6
        elif self.facing_angle <= -13:
            i = 7
        else:
            i = 0

        self.sprite = self.sprites[i]

    def zsort(self) -> None:
        self.z = self.y * -1

    def draw(self, camera: Camera) -> None:
        self.sprite.draw(camera, self.position())

    def debug_draw(self, camera: Camera) -> None:
        self.bbox().draw(camera, Color.white())

    def _check_collision_at(self, x: int, y: int, other: Entity) -> bool:
        """ Check if this entity, at a given position, will intersect another entity. """
        if not self.active or not other.active:
            return False

        if not self.collisions_enabled or not other.collisions_enabled:
            return False

        bbox = Rect(x - self.width // 2, y - self.height // 2, self.width, self.height)
        return other.intersects(bbox)

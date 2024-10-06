from potion import *


class Apple(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Apple"

        # Collision
        self.solid = True
        self.collisions_enabled = True
        self.width = 20
        self.height = 20
        
        # Sprite
        self.sprite = Sprite.empty()
        self.sprites = [
            Sprite.from_atlas("atlas.png", "apple.0001"),
            Sprite.from_atlas("atlas.png", "apple.0002"),
            Sprite.from_atlas("atlas.png", "apple.0003"),
            Sprite.from_atlas("atlas.png", "apple.0004"),
            Sprite.from_atlas("atlas.png", "apple.0005"),
            Sprite.from_atlas("atlas.png", "apple.0006"),
            Sprite.from_atlas("atlas.png", "apple.0007"),
            Sprite.from_atlas("atlas.png", "apple.0008"),
            Sprite.from_atlas("atlas.png", "apple.0009"),
            Sprite.from_atlas("atlas.png", "apple.0010"),
        ]
        for s in self.sprites:
            s.pivot.set_center()
        
            
        # HP
        self.max_hp = 100
        self.hp = 100

    def bbox(self) -> Rect:
        return Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

    def start(self) -> None:
        self.x = 400
        self.y = 200
        self.z = self.y * -1

    def update(self) -> None:
        perc = self.hp / self.max_hp

        if Keyboard.get_key(Keyboard.SPACE):
            self.hp -= 1

        if perc > .9:
            self.sprite = self.sprites[0]
        elif perc > .8:
            self.sprite = self.sprites[1]
        elif perc > .7:
            self.sprite = self.sprites[2]
        elif perc > .6:
            self.sprite = self.sprites[3]
        elif perc > .5:
            self.sprite = self.sprites[4]
        elif perc > .4:
            self.sprite = self.sprites[5]
        elif perc > .3:
            self.sprite = self.sprites[6]
        elif perc > .2:
            self.sprite = self.sprites[7]
        elif perc > .1:
            self.sprite = self.sprites[8]
        else:
            self.sprite = self.sprites[9]

    def draw(self, camera: Camera) -> None:
        self.sprite.draw(camera, self.position())

    def debug_draw(self, camera: Camera) -> None:
        self.bbox().draw(camera, Color.white())

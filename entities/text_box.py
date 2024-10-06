from potion import *


class TextBox(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "TextBox"
        self.tags.add("UI")

        self.text = Text("fonts/udon.16.png")
        self.text.text = "Come in, can you hear me?\nPick up the damn radio!"
        self.text.color = Color.from_hex("#c7dcd0")
        self.text_position = Point(65, 137)

        self.bg_rect = Rect(0, 136, 320, 44)
        self.bg_color = Color(0, 0, 0, 210)

        self.radio_sprite = Sprite.from_atlas("atlas.png", "radio")
        self.radio_position = Point(10, 114)

    def draw(self, camera: Camera) -> None:
        self.bg_rect.draw(camera, self.bg_color, solid=True)
        self.radio_sprite.draw(camera, self.radio_position)
        self.text.draw(camera, self.text_position)

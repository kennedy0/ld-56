from potion import *


class StartGameButton(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.text = Text("fonts/udon.16.png")
        self.text.text = "Start Game"
        self.text.align_horizontal_center()

        self.normal_color = Color.from_hex("#3e3546")
        self.hover_color = Color.from_hex("#c7dcd0")

    def start(self) -> None:
        self.x = 160
        self.y = 125

    def update(self) -> None:
        rect = Rect(self.x - self.text.width // 2, self.y, self.text.width, self.text.height)
        if rect.contains_point(Mouse.world_position()):
            self.text.color = self.hover_color
            if Mouse.get_left_mouse_down():
                self.on_click()
        else:
            self.text.color = self.normal_color

    def on_click(self) -> None:
        from scenes.main_scene import MainScene
        scene = MainScene(is_tutorial=False, is_test=False)
        Engine.load_scene(scene)

    def draw(self, camera: Camera) -> None:
        self.text.draw(camera, self.position())

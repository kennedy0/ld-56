from potion import *


class ScreenFade(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.name = "ScreenFade"
        self.tags.add("UI")
        self.rect = Rect(0, 0, 320, 180)
        self.opacity = 255
        self.fade_speed = 2
        self.visible = True

    def start(self) -> None:
        start_coroutine(self.fade_in())

    def fade_out(self) -> Generator:
        self.visible = True
        self.opacity = 0

        while self.opacity < 255:
            self.opacity += self.fade_speed
            if self.opacity > 255:
                self.opacity = 255
            yield

    def fade_in(self) -> Generator:
        self.visible = True
        self.opacity = 255

        while self.opacity > 0:
            self.opacity -= self.fade_speed
            if self.opacity < 0:
                self.opacity = 0
            yield

        self.visible = False

    def draw(self, camera: Camera) -> None:
        if not self.visible:
            return

        color = Color(0, 0, 0, self.opacity)
        self.rect.draw(camera, color, solid=True)

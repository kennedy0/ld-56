from potion import *


class DefeatScreen(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.tags.add("UI")
        self.name = "DefeatScreen"

        self.visible = False


        self.defeat_text = Text("fonts/udon.16.png")
        self.defeat_text.text = "Better Luck Next Time :("
        self.defeat_text.color = Color.from_hex("#9babb2")
        self.defeat_text.align_horizontal_center()
        self.defeat_text_position = Point(160, 10)

        self.apple_sprite = Sprite.empty()
        self.apple_sprite_position = Point(160, 90)

        self.wave_text = Text("fonts/udon.16.png")
        self.wave_text.text = ""
        self.wave_text.color = Color.from_hex("#9babb2")
        self.wave_text.align_horizontal_center()
        self.wave_text_position = Point(160, 110)

        self.click_to_continue_text = Text("fonts/udon.16.png")
        self.click_to_continue_text.text = "Click anywhere to continue"
        self.click_to_continue_text.color = Color.from_hex("#3e3546")
        self.click_to_continue_text.align_horizontal_center()
        self.click_to_continue_text_position = Point(160, 150)

    def show_defeat_screen(self) -> Generator:
        self.visible = True

        try:
            apple = self.find("Apple")
            game_manager = self.find("GameManager")
            self.defeat_text.text = "Better Luck Next Time :("
            wave = game_manager.wave
            total_waves = game_manager.total_waves
            self.apple_sprite = apple.sprite
            self.wave_text.text = f"Waves Cleared: {wave} / {total_waves}"

            if game_manager.is_tutorial:
                self.apple_sprite_position = Point(160, 55)
                self.defeat_text.text = "How on Earth Did You Fail the Tutorial?!"
                self.defeat_text_position = Point(160, 5)
                self.wave_text.text = (f"Waves Cleared: {wave} / {total_waves}\nYou cleared NEGATIVE ONE waves. We didn't\n"
                                       f"even get the chance to increment the\n"
                                       f"wave counter.")
                self.wave_text_position = Point(160, 70)
        except:
            pass


        # Continue on mouse click
        yield from wait_for_seconds(1)
        while not Mouse.get_left_mouse_down():
            yield

    def draw(self, camera: Camera) -> None:
        if not self.visible:
            return

        self.defeat_text.draw(camera, self.defeat_text_position)
        self.apple_sprite.draw(camera, self.apple_sprite_position)
        self.wave_text.draw(camera, self.wave_text_position)
        self.click_to_continue_text.draw(camera, self.click_to_continue_text_position)

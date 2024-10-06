from potion import *


class VictoryScreen(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.tags.add("UI")
        self.name = "VictoryScreen"

        self.visible = False


        self.victory_text = Text("fonts/udon.16.png")
        self.victory_text.text = "Thank You for Playing :)"
        self.victory_text.color = Color.from_hex("#9babb2")
        self.victory_text.align_horizontal_center()
        self.victory_text_position = Point(160, 10)

        self.apple_sprite = Sprite.empty()
        self.apple_sprite_position = Point(160, 90)

        self.apple_text = Text("fonts/udon.16.png")
        self.apple_text.text = ""
        self.apple_text.color = Color.from_hex("#9babb2")
        self.apple_text.align_horizontal_center()
        self.apple_text_position = Point(160, 110)

        self.click_to_continue_text = Text("fonts/udon.16.png")
        self.click_to_continue_text.text = "Click anywhere to continue"
        self.click_to_continue_text.color = Color.from_hex("#3e3546")
        self.click_to_continue_text.align_horizontal_center()
        self.click_to_continue_text_position = Point(160, 150)

    def show_victory_screen(self) -> Generator:
        self.visible = True

        try:
            apple = self.find("Apple")
            self.apple_sprite = apple.sprite
            perc = apple.hp / apple.max_hp

            if perc > .9:
                # t = "Apple Condition: <RAINBOW>PERFECT!!!</RAINBOW>"
                t = "Apple Condition: PERFECT!!!"
            elif perc > .8:
                # t = "Apple Condition: <EXCITING>Excellent!</EXCITING>"
                t = "Apple Condition: Excellent!"
            elif perc > .7:
                t = "Apple Condition: Great!"
            elif perc > .6:
                t = "Apple Condition: Good"
            elif perc > .5:
                t = "Apple Condition: Average"
            elif perc > .4:
                t = "Apple Condition: Poor"
            elif perc > .3:
                t = "Apple Condition: Gross"
            elif perc > .2:
                t = "Apple Condition: Yuck!"
            else:
                t = "Apple Condition: Just A Core"

            self.apple_text.text = t
        except:
            pass


        # Continue on mouse click
        yield from wait_for_seconds(1)
        while not Mouse.get_left_mouse_down():
            yield

    def draw(self, camera: Camera) -> None:
        if not self.visible:
            return

        self.victory_text.draw(camera, self.victory_text_position)
        self.apple_sprite.draw(camera, self.apple_sprite_position)
        self.apple_text.draw(camera, self.apple_text_position)
        self.click_to_continue_text.draw(camera, self.click_to_continue_text_position)

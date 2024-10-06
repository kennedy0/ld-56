from potion import *

from entities.title_bg import TitleBg
from entities.start_tutorial_button import StartTutorialButton
from entities.start_game_button import StartGameButton


class StartScreen(Scene):
    def load_entities(self) -> None:
        self.entities.add(TitleBg())
        self.entities.add(StartTutorialButton())
        self.entities.add(StartGameButton())

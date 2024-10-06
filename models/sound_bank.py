import random

from potion import *


class SoundBank:
    def __init__(self, content_path: str) -> None:
        self._content_path = content_path
        self._sfx: list[SoundEffect] = []
        self._last_index = None
        self._count = 0
        for file in Content.iterdir(content_path):
            self._sfx.append(SoundEffect(f"{content_path}/{file.name}"))
            self._count += 1

    def play(self) -> None:
        """ Play a sound effect at random. """
        if not self._count:
            Log.error(f"Sound bank for '{self._content_path}' has no SoundEffects")
            return

        # Get a random index
        index = self._get_index()

        # If there's more than 1 sound in the bank, re-roll the index if it's the same one played last time
        if self._count > 1:
            while index == self._last_index:
                index = self._get_index()

        # Play the sound
        self._sfx[index].play()
        self._last_index = index

    def _get_index(self) -> int:
        return random.randrange(0, self._count)

import arcade
from constants import SPRITE_SIZE, GROUND_TOP


# Placeholder color
PLAYER_COLOR = (255, 160, 40)


class Player(arcade.SpriteSolidColor):
    """The player character.

    Placeholder: solid orange square.
    TODO Replace with a 16x16 px sprite sheet at SPRITE_SCALE=3 when art is ready.
    """

    def __init__(self):
        super().__init__(SPRITE_SIZE, SPRITE_SIZE, PLAYER_COLOR)

    @property
    def is_on_ground(self) -> bool:
        """True when the player's feet are resting on the ground surface."""
        return self.bottom <= GROUND_TOP + 1

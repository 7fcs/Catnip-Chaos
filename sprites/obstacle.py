import arcade
from constants import SPRITE_SIZE, GROUND_TOP, SCREEN_WIDTH


OBSTACLE_COLOR = (101, 67, 33)


class Obstacle(arcade.SpriteSolidColor):
    """An oncoming obstacle.

    height_tiles controls how many 16 px tiles tall the obstacle is (1 or 2).
    TODO Replace with sprite art when ready; keep the same SPRITE_SIZE grid.
    """

    def __init__(self, speed: float, height_tiles: int = 1):
        width = SPRITE_SIZE
        height = SPRITE_SIZE * height_tiles
        super().__init__(width, height, OBSTACLE_COLOR)

        self.speed = speed  # px / sec, set by GameView based on difficulty

        # Spawn just off the right edge of the screen
        self.center_x = SCREEN_WIDTH + width / 2 + 4
        self.center_y = GROUND_TOP + height / 2

    def update_position(self, delta_time: float) -> None:
        """Move the obstacle leftward. Called each frame from GameView."""
        self.center_x -= self.speed * delta_time

    @property
    def is_off_screen(self) -> bool:
        return self.right < 0

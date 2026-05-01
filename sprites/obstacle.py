import random
import arcade
from constants import SPRITE_SIZE, GROUND_TOP, SCREEN_WIDTH


class Obstacle(arcade.Sprite):
    """An oncoming obstacle with random sprite selection."""

    # Sprite paths for small (1-tile) and large (2-tile) obstacles
    SMALL_SPRITES = [
        "sprites/obstacles/spikes.png",
        "sprites/obstacles/trash_pile.png",
        "sprites/obstacles/small_potted_plant.png",
    ]

    LARGE_SPRITES = [
        "sprites/obstacles/crystal.png",
        "sprites/obstacles/fire_hydrant.png",
        "sprites/obstacles/cactus.png",
    ]

    def __init__(self, speed: float, height_tiles: int = 1):
        super().__init__()

        self.speed = speed  # px / sec, set by GameView based on difficulty

        # Select random sprite based on height
        if height_tiles == 1:
            sprite_path = random.choice(self.SMALL_SPRITES)
        else:
            sprite_path = random.choice(self.LARGE_SPRITES)

        # Load and set texture
        self.texture = arcade.load_texture(sprite_path)
        self.scale = 3.0  # 3x scale to match SPRITE_SIZE (16 * 3 = 48)

        # Position
        self.center_x = SCREEN_WIDTH + self.width / 2 + 4
        self.center_y = GROUND_TOP + self.height / 2

    def update_position(self, delta_time: float) -> None:
        """Move the obstacle leftward. Called each frame from GameView."""
        self.center_x -= self.speed * delta_time

    @property
    def is_off_screen(self) -> bool:
        return self.right < 0

import random
import arcade
from constants import GROUND_TOP, SCREEN_WIDTH, OVERHEAD_OBSTACLE_BOTTOM


class Obstacle(arcade.Sprite):
    """An oncoming obstacle. Ground obstacles are jumped; overhead obstacles are ducked."""

    GROUND_SPRITES = [
        "sprites/obstacles/obstacle_bin.png",
        "sprites/obstacles/obstacle_fishbowl.png",
        "sprites/obstacles/obstacle_scratcher.png",
        "sprites/obstacles/obstacle_yarn.png",
    ]

    OVERHEAD_SPRITES = [
        "sprites/obstacles/cloud_1.png",
        "sprites/obstacles/cloud_2.png",
        "sprites/obstacles/cloud_3.png",
    ]

    def __init__(self, speed: float, obstacle_type: str = "ground"):
        super().__init__()

        self.speed = speed
        self.obstacle_type = obstacle_type

        if obstacle_type == "overhead":
            sprite_path = random.choice(self.OVERHEAD_SPRITES)
        else:
            sprite_path = random.choice(self.GROUND_SPRITES)

        self.texture = arcade.load_texture(sprite_path)
        self.scale = 1.0

        self.center_x = SCREEN_WIDTH + self.width / 2 + 4
        if obstacle_type == "overhead":
            self.center_y = OVERHEAD_OBSTACLE_BOTTOM + self.height / 2
        else:
            self.center_y = GROUND_TOP + self.height / 2

    def update_position(self, delta_time: float) -> None:
        self.center_x -= self.speed * delta_time

    @property
    def is_off_screen(self) -> bool:
        return self.right < 0

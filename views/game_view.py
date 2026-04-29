import random
import arcade

from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    GROUND_HEIGHT, GROUND_TOP,
    PLAYER_START_X, SPRITE_SIZE,
    GRAVITY, JUMP_SPEED,
    OBSTACLE_BASE_SPEED, OBSTACLE_SPEED_INCREMENT, OBSTACLE_MAX_SPEED,
    OBSTACLE_BASE_INTERVAL, OBSTACLE_MIN_INTERVAL, OBSTACLE_DIFFICULTY_EVERY,
    SCORE_RATE,
)
from sprites.player import Player, DISPLAY_HEIGHT
from sprites.obstacle import Obstacle


BACKGROUND_COLOR = (135, 200, 235)
GROUND_COLOR = (34, 100, 34)
SCORE_TEXT_COLOR = arcade.color.WHITE
HUD_FONT_SIZE = 18


class GameView(arcade.View):
    """Main gameplay screen."""

    def setup(self):
        """Reset the game to its initial state. Call to start or restart."""
        arcade.set_background_color(BACKGROUND_COLOR)

        # ── Player
        self.player = Player()
        self.player.center_x = PLAYER_START_X
        self.player.center_y = GROUND_TOP + DISPLAY_HEIGHT / 2

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # ── Ground platform (physics wall)
        ground_sprite = arcade.SpriteSolidColor(
            SCREEN_WIDTH + 200, GROUND_HEIGHT, GROUND_COLOR
        )
        ground_sprite.center_x = SCREEN_WIDTH / 2
        ground_sprite.center_y = GROUND_HEIGHT / 2

        self.wall_list = arcade.SpriteList()
        self.wall_list.append(ground_sprite)

        # ── Physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            gravity_constant=GRAVITY,
            walls=self.wall_list,
        )

        # ── Obstacles
        self.obstacle_list = arcade.SpriteList()
        self.obstacle_speed = OBSTACLE_BASE_SPEED   # px / sec
        self.spawn_interval = OBSTACLE_BASE_INTERVAL
        self.time_since_spawn = 0.0
        self.obstacles_passed = 0

        # ── Score
        self.score = 0.0

        # ── Input state
        self.jump_pressed = False

    # —— Drawing
    def on_draw(self):
        self.clear()

        self.wall_list.draw()
        self.obstacle_list.draw()
        self.player_list.draw()

        self._draw_hud()

    def _draw_hud(self):
        arcade.draw_text(
            f"Score: {int(self.score)}",
            SCREEN_WIDTH - 16, SCREEN_HEIGHT - 16,
            SCORE_TEXT_COLOR,
            font_size=HUD_FONT_SIZE,
            anchor_x="right",
            anchor_y="top",
        )
        arcade.draw_text(
            f"Speed: {int(self.obstacle_speed)}",
            SCREEN_WIDTH - 16, SCREEN_HEIGHT - 44,
            SCORE_TEXT_COLOR,
            font_size=12,
            anchor_x="right",
            anchor_y="top",
        )
        arcade.draw_text(
            "SPACE / UP — Jump",
            16, SCREEN_HEIGHT - 16,
            SCORE_TEXT_COLOR,
            font_size=12,
            anchor_x="left",
            anchor_y="top",
        )

    # —— Update
    def on_update(self, delta_time: float):
        # Player physics
        self.physics_engine.update()

        # Player animation
        self._update_player_animation()
        self.player.update_animation(delta_time)

        # Score
        self.score += SCORE_RATE * delta_time

        # Spawn obstacles
        self.time_since_spawn += delta_time
        if self.time_since_spawn >= self.spawn_interval:
            self._spawn_obstacle()
            self.time_since_spawn = 0.0

        # Move and cull obstacles
        for obstacle in list(self.obstacle_list):
            obstacle.update_position(delta_time)
            if obstacle.is_off_screen:
                obstacle.remove_from_sprite_lists()
                self.obstacles_passed += 1
                self._maybe_increase_difficulty()

        # Collision -> game over
        if self.player.collides_with_list(self.obstacle_list):
            self._end_game()

    def _update_player_animation(self) -> None:
        if not self.player.is_on_ground:
            if self.player.change_y > 0:
                self.player.set_animation('jump_up')
            else:
                self.player.set_animation('jump_fall')
        else:
            self.player.set_animation('run')

    def _spawn_obstacle(self):
        # Randomly alternate between 1-tile and 2-tile tall obstacles
        height_tiles = random.choices([1, 2], weights=[0.65, 0.35])[0]
        obs = Obstacle(speed=self.obstacle_speed, height_tiles=height_tiles)
        self.obstacle_list.append(obs)

    def _maybe_increase_difficulty(self):
        if self.obstacles_passed % OBSTACLE_DIFFICULTY_EVERY == 0:
            self.obstacle_speed = min(
                self.obstacle_speed + OBSTACLE_SPEED_INCREMENT,
                OBSTACLE_MAX_SPEED,
            )
            # Shrink spawn interval proportionally, but not below the floor
            ratio = OBSTACLE_BASE_SPEED / self.obstacle_speed
            self.spawn_interval = max(
                OBSTACLE_BASE_INTERVAL * ratio,
                OBSTACLE_MIN_INTERVAL,
            )

    def _end_game(self):
        from views.gameover_view import GameOverView
        # Store high score on the window so it persists between sessions
        prev_best = getattr(self.window, "high_score", 0)
        self.window.high_score = max(prev_best, int(self.score))
        view = GameOverView(score=int(self.score), high_score=self.window.high_score)
        self.window.show_view(view)

    # —— Input
    def on_key_press(self, key, modifiers):
        if key in (arcade.key.SPACE, arcade.key.UP, arcade.key.W):
            if self.physics_engine.can_jump():
                self.player.change_y = JUMP_SPEED

    def on_key_release(self, key, modifiers):
        pass  # TODO reserved for future double-jump / variable jump height

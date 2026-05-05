import math
import random
import arcade

from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    GROUND_HEIGHT, GROUND_TOP,
    GRASS_TILE_PATH, GRASS_TILE_WIDTH, BACKGROUND_PATH,
    PLAYER_START_X,
    GRAVITY, JUMP_SPEED,
    OBSTACLE_BASE_SPEED, OBSTACLE_SPEED_INCREMENT, OBSTACLE_MAX_SPEED,
    OBSTACLE_BASE_INTERVAL, OBSTACLE_MIN_INTERVAL, OBSTACLE_DIFFICULTY_EVERY,
    OVERHEAD_OBSTACLE_CHANCE,
    SCORE_RATE,
    CATNIP_PATH, CATNIP_INTERVAL, CATNIP_SCORE, CATNIP_MIN_Y, CATNIP_MAX_Y,
    CATNIP_HIGH_TRIGGER_COUNT, CATNIP_HIGH_WINDOW, CATNIP_HIGH_DURATION,
    CATNIP_HIGH_WOBBLE_PIXELS, CATNIP_HIGH_PULSE_PIXELS,
)
from sprites.player import Player, DISPLAY_HEIGHT, PLAYER_FOOT_OFFSET
from sprites.obstacle import Obstacle


BACKGROUND_COLOR = (135, 200, 235)
SCORE_TEXT_COLOR = arcade.color.WHITE
HUD_FONT_SIZE = 18


class GameView(arcade.View):
    """Main gameplay screen."""

    def setup(self):
        """Reset the game to its initial state. Call to start or restart."""
        arcade.set_background_color(BACKGROUND_COLOR)

        self.background = arcade.Sprite(BACKGROUND_PATH)
        self.background.center_x = SCREEN_WIDTH / 2
        self.background.center_y = SCREEN_HEIGHT / 2
        self.background_list = arcade.SpriteList()
        self.background_list.append(self.background)

        # ── Player
        self.player = Player()
        self.player.center_x = PLAYER_START_X
        self.player.center_y = GROUND_TOP + DISPLAY_HEIGHT / 2 - PLAYER_FOOT_OFFSET

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # ── Ground platform (physics wall)
        self.wall_list = arcade.SpriteList()
        wall = arcade.SpriteSolidColor(SCREEN_WIDTH + 200, GROUND_HEIGHT, (34, 100, 34))
        wall.center_x = SCREEN_WIDTH / 2
        wall.center_y = GROUND_HEIGHT / 2
        self.wall_list.append(wall)

        # ── Grass tiles (visual only, scrolls with obstacles)
        self.grass_list = arcade.SpriteList()
        self.grass_tex = arcade.load_texture(GRASS_TILE_PATH)
        self.grass_tiles = []
        self.grass_offset = 0.0
        for x in range(-GRASS_TILE_WIDTH, SCREEN_WIDTH + GRASS_TILE_WIDTH * 2, GRASS_TILE_WIDTH):
            tile = arcade.Sprite()
            tile.texture = self.grass_tex
            tile.center_x = x
            tile.center_y = GROUND_HEIGHT / 2
            self.grass_list.append(tile)
            self.grass_tiles.append(tile)

        # ── Physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            gravity_constant=GRAVITY,
            walls=self.wall_list,
        )

        # ── Obstacles
        self.obstacle_list = arcade.SpriteList()
        self.obstacle_speed = OBSTACLE_BASE_SPEED
        self.spawn_interval = OBSTACLE_BASE_INTERVAL
        self.time_since_spawn = 0.0
        self.obstacles_passed = 0

        # ── Catnip pickups
        self.catnip_list = arcade.SpriteList()
        self.time_since_catnip = 0.0
        self.catnip_collect_times = []

        # ── Catnip overload visual effect
        self.elapsed_time = 0.0
        self.catnip_high_timer = 0.0
        self.high_overlay_list = arcade.SpriteList()
        pastel_colors = [
            (255, 204, 229),
            (207, 232, 255),
            (221, 255, 214),
            (255, 246, 181),
            (226, 205, 255),
        ]
        for i in range(42):
            size = random.choice((6, 8, 10, 12, 14))
            block = arcade.SpriteSolidColor(size, size, random.choice(pastel_colors))
            block.center_x = random.randint(0, SCREEN_WIDTH)
            block.center_y = random.randint(GROUND_TOP + 20, SCREEN_HEIGHT - 20)
            block.base_x = block.center_x
            block.base_y = block.center_y
            block.phase = random.random() * math.tau
            block.drift_speed = random.uniform(30, 85)
            self.high_overlay_list.append(block)

        # Color-cycle border flashes. Avoid a full-screen tint because some Arcade/Pyglet
        # setups render transparent SpriteSolidColor layers as solid white. Borders keep
        # the effect crazy without hiding gameplay.
        self.high_border_lists = []
        border_thickness = 18
        for color in (
            (255, 175, 220),
            (170, 225, 255),
            (210, 255, 190),
            (255, 245, 165),
            (215, 185, 255),
        ):
            border_list = arcade.SpriteList()

            top = arcade.SpriteSolidColor(SCREEN_WIDTH, border_thickness, color)
            top.center_x = SCREEN_WIDTH / 2
            top.center_y = SCREEN_HEIGHT - border_thickness / 2
            border_list.append(top)

            bottom = arcade.SpriteSolidColor(SCREEN_WIDTH, border_thickness, color)
            bottom.center_x = SCREEN_WIDTH / 2
            bottom.center_y = border_thickness / 2
            border_list.append(bottom)

            left = arcade.SpriteSolidColor(border_thickness, SCREEN_HEIGHT, color)
            left.center_x = border_thickness / 2
            left.center_y = SCREEN_HEIGHT / 2
            border_list.append(left)

            right = arcade.SpriteSolidColor(border_thickness, SCREEN_HEIGHT, color)
            right.center_x = SCREEN_WIDTH - border_thickness / 2
            right.center_y = SCREEN_HEIGHT / 2
            border_list.append(right)

            self.high_border_lists.append(border_list)

        # Cute floating pixel effects for the catnip craze state.
        self.high_cute_effects = arcade.SpriteList()
        effect_paths = [
            "sprites/effects/heart.png",
            "sprites/effects/star.png",
            "sprites/effects/sparkle.png",
            "sprites/effects/paw.png",
            "sprites/effects/fish.png",
        ]
        for i in range(34):
            effect = arcade.Sprite(random.choice(effect_paths), scale=random.choice((2.0, 3.0, 4.0)))
            effect.center_x = random.randint(0, SCREEN_WIDTH)
            effect.center_y = random.randint(GROUND_TOP + 40, SCREEN_HEIGHT - 25)
            effect.base_x = effect.center_x
            effect.base_y = effect.center_y
            effect.phase = random.random() * math.tau
            effect.drift_speed = random.uniform(35, 105)
            effect.bob_amount = random.choice((8, 12, 16, 20))
            self.high_cute_effects.append(effect)

        # ── Score
        self.score = 0.0

        # ── Input state
        self.duck_pressed = False

        # ── HUD Text objects
        self.score_text = arcade.Text(
            "Score: 0",
            SCREEN_WIDTH - 16, SCREEN_HEIGHT - 16,
            SCORE_TEXT_COLOR,
            font_size=HUD_FONT_SIZE,
            anchor_x="right",
            anchor_y="top",
        )
        self.speed_text = arcade.Text(
            f"Speed: {int(self.obstacle_speed)}",
            SCREEN_WIDTH - 16, SCREEN_HEIGHT - 44,
            SCORE_TEXT_COLOR,
            font_size=12,
            anchor_x="right",
            anchor_y="top",
        )
        self.controls_text = arcade.Text(
            "SPACE / UP — Jump    DOWN / S — Duck",
            16, SCREEN_HEIGHT - 16,
            SCORE_TEXT_COLOR,
            font_size=12,
            anchor_x="left",
            anchor_y="top",
        )
        self.catnip_effect_text = arcade.Text(
            "CATNIP CRAZE!",
            SCREEN_WIDTH / 2, SCREEN_HEIGHT - 60,
            (255, 235, 255),
            font_size=28,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )

    # —— Drawing
    def on_draw(self):
        self.clear()

        if self._catnip_high_active:
            wobble_x = int(math.sin(self.elapsed_time * 15.0) * CATNIP_HIGH_WOBBLE_PIXELS)
            wobble_y = int(math.cos(self.elapsed_time * 11.0) * CATNIP_HIGH_PULSE_PIXELS)
            pulse = CATNIP_HIGH_PULSE_PIXELS if int(self.elapsed_time * 8) % 2 == 0 else -CATNIP_HIGH_PULSE_PIXELS

            self._draw_sprite_list_shifted(self.background_list, -wobble_x // 2 + pulse, 0)
            self._draw_sprite_list_shifted(self.wall_list, wobble_x, 0)
            self._draw_sprite_list_shifted(self.grass_list, wobble_x - pulse, 0)
            self._draw_sprite_list_shifted(self.catnip_list, -wobble_x, wobble_y)
            self._draw_sprite_list_shifted(self.obstacle_list, wobble_x, wobble_y)

            self._draw_sprite_list_shifted(self.player_list, -wobble_x + pulse * 2, wobble_y)
            self._draw_sprite_list_shifted(self.player_list, -wobble_x, wobble_y)

            border_index = int(self.elapsed_time * 9) % len(self.high_border_lists)
            self.high_border_lists[border_index].draw()
            self.high_overlay_list.draw()
            self.high_cute_effects.draw()
            self.catnip_effect_text.draw()
        else:
            self.background_list.draw()
            self.wall_list.draw()
            self.grass_list.draw()
            self.catnip_list.draw()
            self.obstacle_list.draw()
            self.player_list.draw()

        self._draw_hud()

    def _draw_hud(self):
        self.score_text.draw()
        self.speed_text.draw()
        self.controls_text.draw()

    def _draw_sprite_list_shifted(self, sprite_list, dx: int, dy: int) -> None:
        """Temporarily offset sprites for a crisp pixel-art wobble, then restore."""
        if len(sprite_list) == 0:
            return

        for sprite in sprite_list:
            sprite.center_x += dx
            sprite.center_y += dy

        sprite_list.draw()

        for sprite in sprite_list:
            sprite.center_x -= dx
            sprite.center_y -= dy

    @property
    def _catnip_high_active(self) -> bool:
        return self.catnip_high_timer > 0

    def _update_hud_text(self):
        self.score_text.text = f"Score: {int(self.score)}"
        self.speed_text.text = f"Speed: {int(self.obstacle_speed)}"

    # —— Update
    def on_update(self, delta_time: float):
        self.elapsed_time += delta_time
        if self.catnip_high_timer > 0:
            self.catnip_high_timer = max(0.0, self.catnip_high_timer - delta_time)
            self._update_high_overlay(delta_time)

        # Player physics
        self.physics_engine.update()

        # Duck only while grounded. This prevents ducking from replacing jump collision midair
        self.player.set_ducking(self.duck_pressed and self.player.is_on_ground)

        # Player animation
        self._update_player_animation()
        self.player.update_animation(delta_time)

        # Score
        self.score += SCORE_RATE * delta_time
        self._update_hud_text()

        # Spawn obstacles
        self.time_since_spawn += delta_time
        if self.time_since_spawn >= self.spawn_interval:
            self._spawn_obstacle()
            self.time_since_spawn = 0.0

        # Spawn catnip pickups
        self.time_since_catnip += delta_time
        if self.time_since_catnip >= CATNIP_INTERVAL:
            self._spawn_catnip()
            self.time_since_catnip = 0.0

        # Move and cull obstacles
        for obstacle in list(self.obstacle_list):
            obstacle.update_position(delta_time)
            if obstacle.is_off_screen:
                obstacle.remove_from_sprite_lists()
                self.obstacles_passed += 1
                self._maybe_increase_difficulty()

        # Move and cull catnip
        for catnip in list(self.catnip_list):
            catnip.center_x -= self.obstacle_speed * delta_time
            if catnip.right < 0:
                catnip.remove_from_sprite_lists()

        # Collect catnip
        for catnip in self.player.collides_with_list(self.catnip_list):
            catnip.remove_from_sprite_lists()
            self._collect_catnip()

        # Scroll grass
        self.grass_offset -= self.obstacle_speed * delta_time
        if self.grass_offset <= -GRASS_TILE_WIDTH:
            self.grass_offset += GRASS_TILE_WIDTH

        for i, tile in enumerate(self.grass_tiles):
            tile.center_x = (i * GRASS_TILE_WIDTH) - GRASS_TILE_WIDTH + self.grass_offset

        # Collision = game over
        if self.player.collides_with_list(self.obstacle_list):
            self._end_game()

    def _update_player_animation(self) -> None:
        if self.player.is_ducking:
            self.player.set_animation('duck')
        elif not self.player.is_on_ground:
            if self.player.change_y > 0:
                self.player.set_animation('jump_up')
            else:
                self.player.set_animation('jump_fall')
        else:
            self.player.set_animation('run')

    def _spawn_obstacle(self):
        obstacle_type = "overhead" if random.random() < OVERHEAD_OBSTACLE_CHANCE else "ground"
        obs = Obstacle(speed=self.obstacle_speed, obstacle_type=obstacle_type)
        self.obstacle_list.append(obs)

    def _spawn_catnip(self):
        catnip = arcade.Sprite(CATNIP_PATH)
        catnip.center_x = SCREEN_WIDTH + catnip.width / 2 + 12
        catnip.center_y = random.randint(CATNIP_MIN_Y, CATNIP_MAX_Y)
        self.catnip_list.append(catnip)

    def _collect_catnip(self):
        self.score += CATNIP_SCORE
        self.catnip_collect_times.append(self.elapsed_time)
        cutoff = self.elapsed_time - CATNIP_HIGH_WINDOW
        self.catnip_collect_times = [t for t in self.catnip_collect_times if t >= cutoff]

        if len(self.catnip_collect_times) >= CATNIP_HIGH_TRIGGER_COUNT:
            self.catnip_high_timer = CATNIP_HIGH_DURATION
            self.catnip_collect_times.clear()

    def _update_high_overlay(self, delta_time: float) -> None:
        text_colors = [
            (255, 245, 255),
            (255, 210, 235),
            (205, 240, 255),
            (230, 255, 210),
            (255, 245, 180),
        ]
        self.catnip_effect_text.color = text_colors[int(self.elapsed_time * 9) % len(text_colors)]

        for i, block in enumerate(self.high_overlay_list):
            block.base_x -= block.drift_speed * delta_time
            if block.base_x < -20:
                block.base_x = SCREEN_WIDTH + random.randint(20, 180)
                block.base_y = random.randint(GROUND_TOP + 30, SCREEN_HEIGHT - 30)

            jitter_x = random.choice((-2, 0, 2))
            jitter_y = random.choice((-2, 0, 2))
            block.center_x = int(block.base_x + math.sin(self.elapsed_time * 8.0 + block.phase) * 18 + jitter_x)
            block.center_y = int(block.base_y + math.cos(self.elapsed_time * 6.0 + block.phase + i) * 14 + jitter_y)

        for i, effect in enumerate(self.high_cute_effects):
            effect.base_x -= effect.drift_speed * delta_time
            if effect.base_x < -40:
                effect.base_x = SCREEN_WIDTH + random.randint(30, 240)
                effect.base_y = random.randint(GROUND_TOP + 50, SCREEN_HEIGHT - 30)
                effect.scale = random.choice((2.0, 3.0, 4.0))

            effect.center_x = int(effect.base_x + math.sin(self.elapsed_time * 4.5 + effect.phase) * 24)
            effect.center_y = int(effect.base_y + math.cos(self.elapsed_time * 5.5 + effect.phase + i) * effect.bob_amount)
            effect.angle = 0 if int(self.elapsed_time * 10 + i) % 2 == 0 else random.choice((-12, 12))

    def _maybe_increase_difficulty(self):
        if self.obstacles_passed % OBSTACLE_DIFFICULTY_EVERY == 0:
            self.obstacle_speed = min(
                self.obstacle_speed + OBSTACLE_SPEED_INCREMENT,
                OBSTACLE_MAX_SPEED,
            )
            ratio = OBSTACLE_BASE_SPEED / self.obstacle_speed
            self.spawn_interval = max(
                OBSTACLE_BASE_INTERVAL * ratio,
                OBSTACLE_MIN_INTERVAL,
            )

    def _end_game(self):
        from views.gameover_view import GameOverView
        prev_best = getattr(self.window, "high_score", 0)
        self.window.high_score = max(prev_best, int(self.score))
        view = GameOverView(score=int(self.score), high_score=self.window.high_score)
        self.window.show_view(view)

    # —— Input
    def on_key_press(self, key, modifiers):
        if key in (arcade.key.SPACE, arcade.key.UP, arcade.key.W):
            if self.physics_engine.can_jump() and not self.player.is_ducking:
                self.player.change_y = JUMP_SPEED
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.duck_pressed = True

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.DOWN, arcade.key.S):
            self.duck_pressed = False

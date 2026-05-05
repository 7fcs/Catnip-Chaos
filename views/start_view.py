import arcade
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_TOP, GROUND_HEIGHT,
    GRASS_TILE_PATH, GRASS_TILE_WIDTH, BACKGROUND_PATH,
    TITLE_SCREEN_PATH, BUTTON_START_PATH, BUTTON_EXIT_PATH,
)
from sprites.player import Player, DISPLAY_HEIGHT, PLAYER_FOOT_OFFSET


BACKGROUND_COLOR = (30, 30, 60)


class StartView(arcade.View):
    """Title / start screen shown when the game first launches."""

    def on_show_view(self):
        arcade.set_background_color(BACKGROUND_COLOR)

        self.background = arcade.Sprite(BACKGROUND_PATH)
        self.background.center_x = SCREEN_WIDTH / 2
        self.background.center_y = SCREEN_HEIGHT / 2
        self.background_list = arcade.SpriteList()
        self.background_list.append(self.background)

        self.player = Player()
        self.player.center_x = SCREEN_WIDTH / 2
        self.player.center_y = GROUND_TOP + DISPLAY_HEIGHT / 2 - PLAYER_FOOT_OFFSET

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        self.wall_list = arcade.SpriteList()
        wall = arcade.SpriteSolidColor(SCREEN_WIDTH + 200, GROUND_HEIGHT, (34, 100, 34))
        wall.center_x = SCREEN_WIDTH / 2
        wall.center_y = GROUND_HEIGHT / 2
        self.wall_list.append(wall)

        self.grass_list = arcade.SpriteList()
        grass_tex = arcade.load_texture(GRASS_TILE_PATH)
        for x in range(-GRASS_TILE_WIDTH, SCREEN_WIDTH + GRASS_TILE_WIDTH * 2, GRASS_TILE_WIDTH):
            tile = arcade.Sprite()
            tile.texture = grass_tex
            tile.center_x = x
            tile.center_y = GROUND_HEIGHT / 2
            self.grass_list.append(tile)

        self.title_sprite = arcade.Sprite(TITLE_SCREEN_PATH)
        self.title_sprite.center_x = SCREEN_WIDTH / 2
        self.title_sprite.center_y = SCREEN_HEIGHT - 105
        self.title_list = arcade.SpriteList()
        self.title_list.append(self.title_sprite)

        self.start_button = arcade.Sprite(BUTTON_START_PATH)
        self.start_button.center_x = SCREEN_WIDTH / 2
        self.start_button.center_y = SCREEN_HEIGHT / 2 - 20

        self.exit_button = arcade.Sprite(BUTTON_EXIT_PATH)
        self.exit_button.center_x = SCREEN_WIDTH / 2
        self.exit_button.center_y = SCREEN_HEIGHT / 2 - 100

        self.button_list = arcade.SpriteList()
        self.button_list.append(self.start_button)
        self.button_list.append(self.exit_button)

    def on_update(self, delta_time: float):
        self.player.update_animation(delta_time)

    def on_draw(self):
        self.clear()
        self.background_list.draw()
        self.wall_list.draw()
        self.grass_list.draw()
        self.player_list.draw()
        self.title_list.draw()
        self.button_list.draw()

    def _start_game(self):
        from views.game_view import GameView
        game = GameView()
        game.setup()
        self.window.show_view(game)

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.SPACE, arcade.key.RETURN):
            self._start_game()
        elif key == arcade.key.ESCAPE:
            arcade.close_window()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.start_button.collides_with_point((x, y)):
            self._start_game()
        elif self.exit_button.collides_with_point((x, y)):
            arcade.close_window()

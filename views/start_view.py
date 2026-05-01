import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_TOP, GROUND_HEIGHT, GRASS_TILE_PATH, GRASS_TILE_WIDTH
from sprites.player import Player, DISPLAY_HEIGHT


BACKGROUND_COLOR = (30, 30, 60)
TEXT_COLOR = arcade.color.WHITE
ACCENT_COLOR = (255, 160, 40)


class StartView(arcade.View):
    """Title / start screen shown when the game first launches."""

    def on_show_view(self):
        arcade.set_background_color(BACKGROUND_COLOR)

        self.player = Player()
        self.player.center_x = SCREEN_WIDTH / 2
        self.player.center_y = GROUND_TOP + DISPLAY_HEIGHT / 2

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

        cx = SCREEN_WIDTH / 2
        cy = SCREEN_HEIGHT / 2
        self.title_text = arcade.Text(
            "CATNIP CHAOS", cx, cy + 150, ACCENT_COLOR,
            font_size=56, anchor_x="center", anchor_y="center", bold=True
        )
        self.subtitle_text = arcade.Text(
            "Jump over obstacles — don't get hit!", cx, cy + 80, TEXT_COLOR,
            font_size=18, anchor_x="center", anchor_y="center"
        )
        self.controls_text = arcade.Text(
            "SPACE / UP  —  Jump", cx, cy + 40, TEXT_COLOR,
            font_size=14, anchor_x="center", anchor_y="center"
        )
        self.start_text = arcade.Text(
            "Press SPACE to start", cx, cy - 30, ACCENT_COLOR,
            font_size=20, anchor_x="center", anchor_y="center"
        )

    def on_update(self, delta_time: float):
        self.player.update_animation(delta_time)

    def on_draw(self):
        self.clear()

        self.wall_list.draw()
        self.grass_list.draw()
        self.player_list.draw()

        self.title_text.draw()
        self.subtitle_text.draw()
        self.controls_text.draw()
        self.start_text.draw()

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.SPACE, arcade.key.RETURN):
            from views.game_view import GameView
            game = GameView()
            game.setup()
            self.window.show_view(game)

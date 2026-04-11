import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


BACKGROUND_COLOR = (30, 30, 60)
TEXT_COLOR = arcade.color.WHITE
ACCENT_COLOR = (255, 160, 40)


class StartView(arcade.View):
    """Title / start screen shown when the game first launches."""

    def on_show_view(self):
        arcade.set_background_color(BACKGROUND_COLOR)

    def on_draw(self):
        self.clear()

        cx = SCREEN_WIDTH / 2
        cy = SCREEN_HEIGHT / 2

        arcade.draw_text(
            "CATNIP CHAOS",
            cx, cy + 80,
            ACCENT_COLOR,
            font_size=56,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )

        arcade.draw_text(
            "Jump over obstacles — don't get hit!",
            cx, cy,
            TEXT_COLOR,
            font_size=18,
            anchor_x="center",
            anchor_y="center",
        )

        arcade.draw_text(
            "SPACE / UP  —  Jump",
            cx, cy - 50,
            TEXT_COLOR,
            font_size=14,
            anchor_x="center",
            anchor_y="center",
        )

        arcade.draw_text(
            "Press SPACE to start",
            cx, cy - 120,
            ACCENT_COLOR,
            font_size=20,
            anchor_x="center",
            anchor_y="center",
        )

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.SPACE, arcade.key.RETURN):
            from views.game_view import GameView
            game = GameView()
            game.setup()
            self.window.show_view(game)

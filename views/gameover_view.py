import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


BACKGROUND_COLOR = (20, 20, 40)
TEXT_COLOR = arcade.color.WHITE
ACCENT_COLOR = (255, 80, 80)
GOLD_COLOR = (255, 215, 0)


class GameOverView(arcade.View):
    """Game over / results screen."""

    def __init__(self, score: int, high_score: int):
        super().__init__()
        self.score = score
        self.high_score = high_score

    def on_show_view(self):
        arcade.set_background_color(BACKGROUND_COLOR)

    def on_draw(self):
        self.clear()

        cx = SCREEN_WIDTH / 2
        cy = SCREEN_HEIGHT / 2

        arcade.draw_text(
            "GAME OVER",
            cx, cy + 100,
            ACCENT_COLOR,
            font_size=52,
            anchor_x="center",
            anchor_y="center",
            bold=True,
        )

        arcade.draw_text(
            f"Score: {self.score}",
            cx, cy + 20,
            TEXT_COLOR,
            font_size=28,
            anchor_x="center",
            anchor_y="center",
        )

        is_new_best = self.score >= self.high_score
        best_color = GOLD_COLOR if is_new_best else TEXT_COLOR
        best_label = "NEW BEST!" if is_new_best else f"Best: {self.high_score}"

        arcade.draw_text(
            best_label,
            cx, cy - 30,
            best_color,
            font_size=20,
            anchor_x="center",
            anchor_y="center",
        )

        arcade.draw_text(
            "Press SPACE to play again",
            cx, cy - 100,
            ACCENT_COLOR,
            font_size=18,
            anchor_x="center",
            anchor_y="center",
        )

        arcade.draw_text(
            "Press ESC for title screen",
            cx, cy - 130,
            TEXT_COLOR,
            font_size=14,
            anchor_x="center",
            anchor_y="center",
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            from views.game_view import GameView
            game = GameView()
            game.setup()
            self.window.show_view(game)
        elif key == arcade.key.ESCAPE:
            from views.start_view import StartView
            self.window.show_view(StartView())

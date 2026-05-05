import arcade
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_PATH,
    BUTTON_RETRY_PATH, BUTTON_EXIT_PATH,
)


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

        cx = SCREEN_WIDTH / 2
        cy = SCREEN_HEIGHT / 2

        self.background = arcade.Sprite(BACKGROUND_PATH)
        self.background.center_x = cx
        self.background.center_y = SCREEN_HEIGHT / 2
        self.background_list = arcade.SpriteList()
        self.background_list.append(self.background)

        self.game_over_text = arcade.Text(
            "GAME OVER", cx, cy + 120, ACCENT_COLOR,
            font_size=52, anchor_x="center", anchor_y="center", bold=True
        )
        self.score_text = arcade.Text(
            f"Score: {self.score}", cx, cy + 50, TEXT_COLOR,
            font_size=28, anchor_x="center", anchor_y="center"
        )
        self.best_text = arcade.Text(
            "", cx, cy + 5, TEXT_COLOR,
            font_size=20, anchor_x="center", anchor_y="center"
        )

        self.retry_button = arcade.Sprite(BUTTON_RETRY_PATH)
        self.retry_button.center_x = cx
        self.retry_button.center_y = cy - 70

        self.exit_button = arcade.Sprite(BUTTON_EXIT_PATH)
        self.exit_button.center_x = cx
        self.exit_button.center_y = cy - 150

        self.button_list = arcade.SpriteList()
        self.button_list.append(self.retry_button)
        self.button_list.append(self.exit_button)

        self._update_text()

    def _update_text(self):
        is_new_best = self.score >= self.high_score
        self.best_text.color = GOLD_COLOR if is_new_best else TEXT_COLOR
        self.best_text.text = "NEW BEST!" if is_new_best else f"Best: {self.high_score}"

    def on_show_view(self):
        arcade.set_background_color(BACKGROUND_COLOR)

    def on_draw(self):
        self.clear()
        self.background_list.draw()
        self.game_over_text.draw()
        self.score_text.draw()
        self.best_text.draw()
        self.button_list.draw()

    def _retry(self):
        from views.game_view import GameView
        game = GameView()
        game.setup()
        self.window.show_view(game)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self._retry()
        elif key == arcade.key.ESCAPE:
            arcade.close_window()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.retry_button.collides_with_point((x, y)):
            self._retry()
        elif self.exit_button.collides_with_point((x, y)):
            arcade.close_window()

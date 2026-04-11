import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from views.start_view import StartView


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.high_score = 0
    window.show_view(StartView())
    arcade.run()


if __name__ == "__main__":
    main()

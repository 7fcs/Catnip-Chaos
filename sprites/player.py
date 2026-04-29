import os
import arcade
from arcade.hitbox import HitBox

from constants import GROUND_TOP


SPRITE_SHEET_DIR = os.path.join(os.path.dirname(__file__), 'cat', 'sheets')
FRAME_WIDTH = 379
FRAME_HEIGHT = 363
CAT_SCALE = 0.25

DISPLAY_WIDTH = FRAME_WIDTH * CAT_SCALE
DISPLAY_HEIGHT = FRAME_HEIGHT * CAT_SCALE

FPS = 60

ANIMATION_FPS = {
    'run': 14,
    'jump_up': 10,
    'jump_fall': 10,
}

COLLISION_WIDTH_RATIO = 0.55
COLLISION_HEIGHT_RATIO = 0.80


class Player(arcade.Sprite):
    """The player cat with frame-by-frame animations."""

    def __init__(self):
        super().__init__()

        self.animations = {}
        self._load_animation('run')
        self._load_animation('jump_up')
        self._load_animation('jump_fall')

        self.current_animation = 'run'
        self.cur_frame_idx = 0
        self.frame_timer = 0.0

        self.texture = self.animations['run'][0]
        self.scale = CAT_SCALE
        self._update_hitbox()

    def _load_animation(self, name: str) -> None:
        sheet_path = os.path.join(SPRITE_SHEET_DIR, f'{name}.png')
        sheet = arcade.SpriteSheet(path=sheet_path)

        num_frames = sheet.image.width // FRAME_WIDTH
        textures = sheet.get_texture_grid(
            size=(FRAME_WIDTH, FRAME_HEIGHT),
            columns=num_frames,
            count=num_frames,
        )

        self.animations[name] = textures

    def set_animation(self, name: str) -> None:
        if name != self.current_animation and name in self.animations:
            self.current_animation = name
            self.cur_frame_idx = 0
            self.frame_timer = 0.0
            self.texture = self.animations[name][0]
            self._update_hitbox()

    def update_animation(self, delta_time: float) -> None:
        frames = self.animations[self.current_animation]
        if len(frames) <= 1:
            return

        anim_fps = ANIMATION_FPS.get(self.current_animation, 12)
        self.frame_timer += delta_time

        frame_duration = 1.0 / anim_fps
        if self.frame_timer >= frame_duration:
            self.frame_timer -= frame_duration
            self.cur_frame_idx = (self.cur_frame_idx + 1) % len(frames)
            self.texture = frames[self.cur_frame_idx]

    def _update_hitbox(self) -> None:
        hw = (DISPLAY_WIDTH * COLLISION_WIDTH_RATIO) / 2
        hh = (DISPLAY_HEIGHT * COLLISION_HEIGHT_RATIO) / 2
        points = [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]
        self.hit_box = HitBox(points)

    @property
    def is_on_ground(self) -> bool:
        return self.bottom <= GROUND_TOP + 1

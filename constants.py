# —— Screen
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
SCREEN_TITLE = "Catnip Chaos"
TARGET_FPS = 60

# —— Pixel Art Specs  (for sprite design)
# All sprites are designed on a 16x16 px grid and displayed at 3x scale.
#   Native tile:   16 x 16 px
#   Display tile:  48 x 48 px  (16 x 3)
#   Aspect ratio:  1:1 per tile, 16:9 screen
#
# Character sheet guidelines:
#   Player (cat):        16 x 16 px  — idle(1f), run(4f), jump(1f)
#   Small obstacle:      16 x 16 px  — static (e.g. trash can lid)
#   Tall obstacle:       16 x 32 px  — static (e.g. trash can)
#   Ground tile:         16 x 16 px  — seamless horizontal repeat
#   Background layer 1:  96 x 54 px  — far buildings (parallax slow)
#   Background layer 2:  96 x 54 px  — mid buildings (parallax fast)
#   Catnip pickup:       16 x 16 px  — 3-frame spin loop
#
# Export: PNG with transparency; no padding between frames

SPRITE_NATIVE_SIZE = 16     # px at 1x (design canvas size per tile)
SPRITE_SCALE = 3            # display multiplier
SPRITE_SIZE = SPRITE_NATIVE_SIZE * SPRITE_SCALE  # 48 px on screen

# —— Layout
GROUND_HEIGHT = 60          # px — visual + physics ground thickness
GROUND_TOP = GROUND_HEIGHT  # y-coordinate of the ground surface
GRASS_TILE_PATH = "sprites/ground/grass_tile.png"
GRASS_TILE_WIDTH = 64       # px — width of one grass tile

PLAYER_START_X = 160        # fixed horizontal position of the player

# —— Physics  (frame-based, tuned for 60 fps)
GRAVITY = 1.0               # px/frame² downward acceleration
JUMP_SPEED = 20.0           # px/frame initial upward velocity on jump

# —— Obstacles
OBSTACLE_BASE_SPEED = 300.0       # px/sec starting speed
OBSTACLE_SPEED_INCREMENT = 15.0   # px/sec added each time difficulty increases
OBSTACLE_MAX_SPEED = 650.0
OBSTACLE_BASE_INTERVAL = 2.2      # seconds between spawns at start
OBSTACLE_MIN_INTERVAL = 0.75      # floor for spawn interval
OBSTACLE_DIFFICULTY_EVERY = 5     # obstacles passed before next difficulty tick

# —— Scoring
SCORE_RATE = 1             # points awarded per second of survival

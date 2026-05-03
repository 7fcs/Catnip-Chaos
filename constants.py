# —— Screen
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
SCREEN_TITLE = "Catnip Chaos"
TARGET_FPS = 60

# —— Pixel Art / Assets
SPRITE_NATIVE_SIZE = 16
SPRITE_SCALE = 3
SPRITE_SIZE = SPRITE_NATIVE_SIZE * SPRITE_SCALE

BACKGROUND_PATH = "sprites/background.png"
TITLE_SCREEN_PATH = "sprites/ui/title_screen.png"
BUTTON_START_PATH = "sprites/ui/btn_start.png"
BUTTON_EXIT_PATH = "sprites/ui/btn_exit.png"
BUTTON_RETRY_PATH = "sprites/ui/btn_retry.png"
CATNIP_PATH = "sprites/catnip_3.png"

# —— Layout
GROUND_HEIGHT = 60
GROUND_TOP = GROUND_HEIGHT
GRASS_TILE_PATH = "sprites/ground/grass_tile.png"
GRASS_TILE_WIDTH = 64
PLAYER_START_X = 160

# —— Physics
GRAVITY = 1.0
JUMP_SPEED = 20.0

# —— Ducking
DUCK_KEYS = "DOWN / S"
DUCK_HITBOX_HEIGHT_RATIO = 0.42
DUCK_HITBOX_WIDTH_RATIO = 0.65

# —— Obstacles
OBSTACLE_BASE_SPEED = 300.0
OBSTACLE_SPEED_INCREMENT = 15.0
OBSTACLE_MAX_SPEED = 650.0
OBSTACLE_BASE_INTERVAL = 2.2
OBSTACLE_MIN_INTERVAL = 0.75
OBSTACLE_DIFFICULTY_EVERY = 5
OVERHEAD_OBSTACLE_CHANCE = 0.32
OVERHEAD_OBSTACLE_BOTTOM = 112

# —— Catnip pickups
CATNIP_INTERVAL = 3.0
CATNIP_SCORE = 5
CATNIP_MIN_Y = GROUND_TOP + 95
CATNIP_MAX_Y = GROUND_TOP + 165


# —— Catnip overload effect
CATNIP_HIGH_TRIGGER_COUNT = 3       # pickups needed inside the window below
CATNIP_HIGH_WINDOW = 9.0            # seconds
CATNIP_HIGH_DURATION = 7.0          # seconds of cute visual distortion
CATNIP_HIGH_WOBBLE_PIXELS = 9       # integer pixel offset keeps pixel art crisp
CATNIP_HIGH_PULSE_PIXELS = 4       # extra snap offset for crazier visual rhythm

# —— Scoring
SCORE_RATE = 1

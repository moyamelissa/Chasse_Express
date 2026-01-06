# Game constants, configuration, colors, and difficulty presets

# Screen dimensions
WIDTH = 800
HEIGHT = 600
OUTLINE_W = 3

# Colors
MAGPIE_BLACK = (25, 25, 25)
MAGPIE_WHITE = (240, 240, 240)
MAGPIE_BLUE = (50, 110, 210)
MAGPIE_BEAK = (60, 60, 60)
MAGPIE_HIGHLIGHT = (210, 210, 220)
RED = (255, 0, 0)

# Magpie
MAGPIE_BODY_RADIUS = 32

# Difficulty presets
DIFFICULTY_SETTINGS = {
    "Facile": {"magpie_count": 1, "speed": 3, "ammo": 10, "goal": 5, "time": 30, "label": "Facile"},
    "Moyen": {"magpie_count": 2, "speed": 5, "ammo": 15, "goal": 10, "time": 30, "label": "Moyen"},
    "Difficile": {"magpie_count": 4, "speed": 8, "ammo": 10, "goal": 10, "time": 30, "label": "Difficile"},
}

# Resource paths (centralized here)
SHELTIE_IMG_PATH = "assets/images/sheltie.png"
BARKING_SOUND_PATH = "assets/audio/barking.mp3"
AMBIANCE_MUSIC_PATH = "assets/audio/ambiance.mp3"
TREE_IMG_PATH = "assets/images/tree.png"
BACKGROUND_IMG_PATH = "assets/images/background.jpg"
BIRD_IMG_PATH = "assets/images/bird.png"
AMMO_IMG_PATH = "assets/images/ammo.png"
TIMER_IMG_PATH = "assets/images/timer.png"
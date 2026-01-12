# Constantes du jeu, configuration, couleurs et préréglages de difficulté

# Dimensions de l'écran
WIDTH = 800
HEIGHT = 600
OUTLINE_W = 3

# Couleurs
MAGPIE_BLACK = (25, 25, 25)
MAGPIE_WHITE = (240, 240, 240)
MAGPIE_BLUE = (50, 110, 210)
MAGPIE_BEAK = (60, 60, 60)
MAGPIE_HIGHLIGHT = (210, 210, 220)
RED = (255, 0, 0)

# Pie
MAGPIE_BODY_RADIUS = 32

# Préréglages de difficulté
DIFFICULTY_SETTINGS = {
    "Facile": {"magpie_count": 1, "speed": 3, "ammo": 10, "goal": 5, "time": 30, "label": "Facile"},
    "Moyen": {"magpie_count": 2, "speed": 5, "ammo": 15, "goal": 10, "time": 30, "label": "Moyen"},
    "Difficile": {"magpie_count": 4, "speed": 8, "ammo": 10, "goal": 10, "time": 30, "label": "Difficile"},
}


# Chemins des ressources (centralisés ici, toujours absolus)
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SHELTIE_IMG_PATH = os.path.join(BASE_DIR, "assets", "images", "sheltie.png")
BARKING_SOUND_PATH = os.path.join(BASE_DIR, "assets", "audio", "barking.mp3")
AMBIANCE_MUSIC_PATH = os.path.join(BASE_DIR, "assets", "audio", "ambiance.mp3")
TREE_IMG_PATH = os.path.join(BASE_DIR, "assets", "images", "tree.png")
BACKGROUND_IMG_PATH = os.path.join(BASE_DIR, "assets", "images", "background.jpg")
BIRD_IMG_PATH = os.path.join(BASE_DIR, "assets", "images", "bird.png")
AMMO_IMG_PATH = os.path.join(BASE_DIR, "assets", "images", "ammo.png")
TIMER_IMG_PATH = os.path.join(BASE_DIR, "assets", "images", "timer.png")

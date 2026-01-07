import os
import pygame

# Caches globaux
FONT_CACHE = {}
ICON_CACHE = {}
IMAGE_CACHE = {}
SOUND_CACHE = {}

# Tu peux franciser les fonctions de chargement :
def load_image(path):
    if path in IMAGE_CACHE:
        return IMAGE_CACHE[path]
    base_dir = os.path.dirname(os.path.abspath(__file__))
    abs_path = os.path.join(base_dir, path)
    try:
        img = pygame.image.load(abs_path).convert_alpha()
        IMAGE_CACHE[path] = img
        return img
    except (pygame.error, FileNotFoundError):
        return None

def load_sound(path):
    if path in SOUND_CACHE:
        return SOUND_CACHE[path]
    try:
        sound = pygame.mixer.Sound(path)
        SOUND_CACHE[path] = sound
        return sound
    except (pygame.error, FileNotFoundError):
        return None

def load_font(font_names, size):
    key = (tuple(font_names) if isinstance(font_names, list) else font_names, size)
    if key in FONT_CACHE:
        return FONT_CACHE[key]
    if isinstance(font_names, str):
        font_names = [font_names]
    for fname in font_names:
        for suffix in ["", "-Regular"]:
            for ext in [".ttf"]:
                path = fname + suffix + ext
                if os.path.exists(path):
                    font = pygame.font.Font(path, size)
                    FONT_CACHE[key] = font
                    return font
    for sys_name in font_names:
        try:
            font = pygame.font.SysFont(sys_name, size)
            FONT_CACHE[key] = font
            return font
        except Exception:
            continue
    font = pygame.font.SysFont(None, size)
    FONT_CACHE[key] = font
    return font

def load_icon(path, fallback_size=32):
    if path in ICON_CACHE:
        return ICON_CACHE[path]
    try:
        img = pygame.image.load(path)
        icon = img.convert_alpha()
        ICON_CACHE[path] = icon
        return icon
    except (pygame.error, FileNotFoundError):
        surf = pygame.Surface((fallback_size, fallback_size), pygame.SRCALPHA)
        pygame.draw.rect(surf, (180, 180, 180, 200), (0, 0, fallback_size, fallback_size), border_radius=6)
        pygame.draw.rect(surf, (120, 120, 120, 220), (0, 0, fallback_size, fallback_size), 2, border_radius=6)
        ICON_CACHE[path] = surf
        return surf

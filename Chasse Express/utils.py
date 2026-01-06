# =========================
# Fonctions utilitaires pour Chasse Express (chargement police, icône, gestion des erreurs)
# =========================
import os
import pygame

FONT_CACHE = {}
ICON_CACHE = {}

def charger_police(noms_polices: str | list, taille: int) -> "pygame.font.Font":
    """
    Charge la première police trouvée dans la liste, sinon une police système.
    Utilise un cache pour éviter de recharger plusieurs fois la même police.
    """
    key = (tuple(noms_polices) if isinstance(noms_polices, list) else noms_polices, taille)
    if key in FONT_CACHE:
        return FONT_CACHE[key]
    if isinstance(noms_polices, str):
        noms_polices = [noms_polices]
    for fname in noms_polices:
        for suffix in ["", "-Regular"]:
            for ext in [".ttf"]:
                path = fname + suffix + ext
                if os.path.exists(path):
                    font = pygame.font.Font(path, taille)
                    FONT_CACHE[key] = font
                    return font
    for sys_name in noms_polices:
        try:
            font = pygame.font.SysFont(sys_name, taille)
            FONT_CACHE[key] = font
            return font
        except Exception:
            continue
    font = pygame.font.SysFont(None, taille)
    FONT_CACHE[key] = font
    return font

def charger_icone(chemin: str, taille_secours: int = 32) -> "pygame.Surface":
    """
    Charge une icône depuis un fichier, ou crée une icône de secours si le fichier n'existe pas.
    Utilise un cache pour éviter de recharger plusieurs fois la même icône.
    """
    if chemin in ICON_CACHE:
        return ICON_CACHE[chemin]
    try:
        img = pygame.image.load(chemin)
        icon = img.convert_alpha()
        ICON_CACHE[chemin] = icon
        return icon
    except (pygame.error, FileNotFoundError) as e:
        try:
            surf = pygame.Surface((taille_secours, taille_secours), pygame.SRCALPHA)
            pygame.draw.rect(surf, (180, 180, 180, 200), (0, 0, taille_secours, taille_secours), border_radius=6)
            pygame.draw.rect(surf, (120, 120, 120, 220), (0, 0, taille_secours, taille_secours), 2, border_radius=6)
            ICON_CACHE[chemin] = surf
            return surf
        except Exception as fallback_error:
            raise ErreurRessourceJeu(f"Impossible de charger ou de créer une icône pour {chemin}") from fallback_error

class ErreurRessourceJeu(Exception):
    """
    Exception levée lors d'une erreur de chargement de ressource du jeu.
    """
    pass

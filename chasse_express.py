# === Importations des modules ===
import sys
import os
import random
import math
from dataclasses import dataclass, field
from typing import List, Tuple, Optional

# === Fonctions utilitaires modulaires ===
# === Cache pour les polices et icônes ===
FONT_CACHE = {}
ICON_CACHE = {}

def load_font(font_names: str | list, size: int) -> "pygame.font.Font":
    """
    Charge la première police trouvée dans la liste, sinon une police système.
    Utilise un cache pour éviter de recharger plusieurs fois la même police.

    Args:
        font_names (str | list): Nom ou liste de noms de polices à essayer.
        size (int): Taille de la police.

    Returns:
        pygame.font.Font: Objet police pygame.
    """
    import pygame
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

def load_icon(path: str, fallback_size: int = 32) -> "pygame.Surface":
    """
    Charge une icône depuis un fichier, ou crée une icône de secours si le fichier n'existe pas.
    Utilise un cache pour éviter de recharger plusieurs fois la même icône.

    Args:
        path (str): Chemin du fichier image.
        fallback_size (int): Taille de l'icône de secours.

    Returns:
        pygame.Surface: Surface de l'icône.

    Raises:
        GameResourceError: Si le chargement échoue et le fallback n'est pas possible.
    """
    import pygame
    if path in ICON_CACHE:
        return ICON_CACHE[path]
    try:
        img = pygame.image.load(path)
        icon = img.convert_alpha()
        ICON_CACHE[path] = icon
        return icon
    except (pygame.error, FileNotFoundError) as e:
        try:
            surf = pygame.Surface((fallback_size, fallback_size), pygame.SRCALPHA)
            pygame.draw.rect(surf, (180, 180, 180, 200), (0, 0, fallback_size, fallback_size), border_radius=6)
            pygame.draw.rect(surf, (120, 120, 120, 220), (0, 0, fallback_size, fallback_size), 2, border_radius=6)
            ICON_CACHE[path] = surf
            return surf
        except Exception as fallback_error:
            raise GameResourceError(f"Impossible de charger ou de créer une icône pour {path}") from fallback_error

def draw_text_with_outline(
    surface: "pygame.Surface",
    text: str,
    font: "pygame.font.Font",
    pos: tuple,
    main_color: tuple,
    outline_color: tuple = (255,255,255),
    shadow_color: tuple = (0,0,0),
    outline_offset: int = 2,
    shadow_offset: int = 4
) -> None:
    """
    Dessine un texte avec ombre et contour sur une surface pygame.

    Args:
        surface (pygame.Surface): Surface cible.
        text (str): Texte à afficher.
        font (pygame.font.Font): Police utilisée.
        pos (tuple): Position (x, y).
        main_color (tuple): Couleur principale.
        outline_color (tuple): Couleur du contour.
        shadow_color (tuple): Couleur de l'ombre.
        outline_offset (int): Décalage du contour.
        shadow_offset (int): Décalage de l'ombre.
    """
    import pygame
    x, y = pos
    shadow = font.render(text, True, shadow_color)
    surface.blit(shadow, (x+shadow_offset, y+shadow_offset))
    for dx in [-outline_offset, 0, outline_offset]:
        for dy in [-outline_offset, 0, outline_offset]:
            if dx != 0 or dy != 0:
                outline = font.render(text, True, outline_color)
                surface.blit(outline, (x+dx, y+dy))
    main = font.render(text, True, main_color)
    surface.blit(main, (x, y))

def draw_icon_text(
    surface: "pygame.Surface",
    icon: Optional["pygame.Surface"],
    text: str,
    font: "pygame.font.Font",
    pos: tuple,
    icon_size: int,
    gap: int = 10
) -> None:
    """
    Dessine une icône suivie d'un texte, centrés verticalement.

    Args:
        surface (pygame.Surface): Surface cible.
        icon (pygame.Surface): Icône à afficher.
        text (str): Texte à afficher.
        font (pygame.font.Font): Police utilisée.
        pos (tuple): Position (x, y).
        icon_size (int): Taille de l'icône.
        gap (int): Espace entre l'icône et le texte.
    """
    import pygame
    x, y = pos
    if icon:
        icon_img = pygame.transform.smoothscale(icon, (icon_size, icon_size))
        surface.blit(icon_img, (x, y))
        x += icon_size + gap
    label = font.render(text, True, (30,30,30))
    surface.blit(label, (x, y + (icon_size - label.get_height()) // 2))

def get_panel_surface(panel_width: int, panel_height: int, border_radius: int = 24) -> tuple:
    """
    Crée un panneau semi-transparent avec ombre.

    Args:
        panel_width (int): Largeur du panneau.
        panel_height (int): Hauteur du panneau.
        border_radius (int): Rayon des coins arrondis.

    Returns:
        tuple: (surface du panneau, surface de l'ombre)
    """
    import pygame
    panel_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    shadow = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    pygame.draw.rect(shadow, (0,0,0,40), (0,0,panel_width,panel_height), border_radius=border_radius)
    pygame.draw.rect(panel_surf, (245, 248, 255, 230), (0,0,panel_width,panel_height), border_radius=border_radius)
    pygame.draw.rect(panel_surf, (200,200,220,180), (0,0,panel_width,panel_height), 2, border_radius=border_radius)
    return panel_surf, shadow

def get_best_font(size: int) -> "pygame.font.Font":
    """
    Retourne une police sans empattement conviviale pour titres/boutons.

    Args:
        size (int): Taille de la police.

    Returns:
        pygame.font.Font: Objet police pygame.
    """
    return load_font([
        "Montserrat", "Segoe UI", "Arial", "Verdana", "Liberation Sans", "DejaVu Sans"
    ], size)

def get_panel_font(size: int) -> "pygame.font.Font":
    """
    Retourne une police monospace conviviale pour chiffres/timers.

    Args:
        size (int): Taille de la police.

    Returns:
        pygame.font.Font: Objet police pygame.
    """
    return load_font([
        "Consolas", "Menlo", "DejaVu Sans Mono", "Liberation Mono", "Courier New"
    ], size)

# === Fonction pour dessiner le panneau d'état ===
def draw_status_panel(
    surface: "pygame.Surface",
    x: int, y: int, label: str, score: int, goal: int, ammo: int, time_left: int,
    BIRD_IMG: Optional["pygame.Surface"], AMMO_IMG: Optional["pygame.Surface"], TIMER_IMG: Optional["pygame.Surface"],
    stat_font: "pygame.font.Font", label_font: "pygame.font.Font", get_panel_surface_func,
    padding_x: int = 24, padding_y: int = 14, section_gap: int = 32, icon_text_gap: int = 10
) -> None:
    """
    Dessine le panneau d'état du jeu (niveau, score, munitions, temps).

    Args:
        surface (pygame.Surface): Surface cible.
        x (int): Position X du panneau.
        y (int): Position Y du panneau.
        label (str): Nom du niveau.
        score (int): Score actuel.
        goal (int): Score à atteindre.
        ammo (int): Nombre de munitions.
        time_left (int): Temps restant.
        BIRD_IMG, AMMO_IMG, TIMER_IMG: Icônes.
        stat_font, label_font: Polices utilisées.
        get_panel_surface_func: Fonction pour obtenir la surface du panneau.
        padding_x, padding_y, section_gap, icon_text_gap: Espacements.
    """
    import pygame
    icon_size = stat_font.get_height()
    panel_height = icon_size + 2 * padding_y
    groups = []
    niveau_text = label_font.render(f"Niveau : {label}", True, (0,0,0))
    groups.append({'icon': None, 'text_surf': niveau_text})
    bird_text = stat_font.render(f"{score}/{goal}", True, (30,30,30))
    bird_icon = pygame.transform.smoothscale(BIRD_IMG, (icon_size, icon_size)) if BIRD_IMG else None
    groups.append({'icon': bird_icon, 'text_surf': bird_text})
    ammo_text = stat_font.render(f"{ammo}", True, (30,30,30))
    ammo_icon = pygame.transform.smoothscale(AMMO_IMG, (icon_size, icon_size)) if AMMO_IMG else None
    groups.append({'icon': ammo_icon, 'text_surf': ammo_text})
    timer_text = stat_font.render(f"{time_left}s", True, (30,30,30))
    timer_icon = pygame.transform.smoothscale(TIMER_IMG, (icon_size, icon_size)) if TIMER_IMG else None
    groups.append({'icon': timer_icon, 'text_surf': timer_text})
    group_widths = []
    for g in groups:
        w = 0
        if g['icon']:
            w += icon_size + icon_text_gap
        w += g['text_surf'].get_width()
        group_widths.append(w)
    panel_width = sum(group_widths) + section_gap * (len(groups)-1) + 2 * padding_x
    panel_surf, shadow = get_panel_surface_func(panel_width, panel_height)
    surface.blit(shadow, (x+2, y+10))
    draw_x = padding_x
    center_y = panel_height // 2
    for idx, g in enumerate(groups):
        icon_y = center_y - icon_size // 2
        if g['icon']:
            panel_surf.blit(g['icon'], (draw_x, icon_y))
            draw_x += icon_size + icon_text_gap
        text_y = center_y - g['text_surf'].get_height() // 2
        panel_surf.blit(g['text_surf'], (draw_x, text_y))
        draw_x += g['text_surf'].get_width()
        if idx < len(groups) - 1:
            draw_x += section_gap
    surface.blit(panel_surf, (x, y))

# === Chargement et dessin du fond d'écran ===
def draw_landfill_background(surface: "pygame.Surface", BACKGROUND_IMG: Optional["pygame.Surface"] = None) -> None:
    """
    Dessine le fond d'écran du jeu.

    Args:
        surface (pygame.Surface): Surface cible.
        BACKGROUND_IMG (pygame.Surface | None): Image de fond, ou None pour couleur par défaut.
    """
    import pygame
    if BACKGROUND_IMG:
        surface.blit(BACKGROUND_IMG, (0, 0))
    else:
        surface.fill((100, 180, 255))

# === Fonctions de dessin des éléments du jeu ===
def draw_dog(surface: "pygame.Surface", x: int, y: int, jump_phase: float) -> None:
    """
    Dessine le chien sur la surface.

    Args:
        surface (pygame.Surface): Surface cible.
        x (int): Position X.
        y (int): Position Y.
        jump_phase (float): Phase du saut.
    """
    import pygame
    surface.blit(SHELTIE_IMG, (x, y))

MAGPIE_BODY_RADIUS = 32

def draw_magpie(surface: "pygame.Surface", pos: tuple) -> None:
    """
    Dessine une pie à la position donnée.

    Args:
        surface (pygame.Surface): Surface cible.
        pos (tuple): Position (x, y) de la pie.
    """
    import pygame
    x, y = pos
    pygame.draw.ellipse(surface, (0,0,0), (x - 28, y - 12, 56, 24), OUTLINE_W)
    pygame.draw.ellipse(surface, MAGPIE_BLACK, (x - 28, y - 12, 56, 24))
    pygame.draw.ellipse(surface, MAGPIE_WHITE, (x - 10, y - 10, 30, 18))
    pygame.draw.polygon(surface, (0,0,0), [(x - 28, y), (x - 60, y - 6), (x - 55, y + 6)], OUTLINE_W)
    pygame.draw.polygon(surface, MAGPIE_BLUE, [(x - 28, y), (x - 60, y - 6), (x - 55, y + 6)])
    pygame.draw.ellipse(surface, (0,0,0), (x - 10, y - 14, 32, 18), OUTLINE_W)
    pygame.draw.ellipse(surface, MAGPIE_BLUE, (x - 10, y - 14, 32, 18))
    pygame.draw.circle(surface, (0,0,0), (x + 22, y - 6), 13, OUTLINE_W)
    pygame.draw.circle(surface, MAGPIE_BLACK, (x + 22, y - 6), 13)
    pygame.draw.polygon(surface, (0,0,0), [(x + 34, y - 8), (x + 44, y - 12), (x + 36, y - 2)], OUTLINE_W)
    pygame.draw.polygon(surface, MAGPIE_BEAK, [(x + 34, y - 8), (x + 44, y - 12), (x + 36, y - 2)])
    pygame.draw.circle(surface, MAGPIE_WHITE, (x + 28, y - 10), 4)
    pygame.draw.circle(surface, MAGPIE_BLACK, (x + 28, y - 10), 2)

def draw_crosshair(surface: "pygame.Surface", pos: tuple) -> None:
    """
    Dessine le viseur à la position donnée.

    Args:
        surface (pygame.Surface): Surface cible.
        pos (tuple): Position (x, y) du viseur.
    """
    import pygame
    x, y = pos
    crosshair_surf = pygame.Surface((44, 44), pygame.SRCALPHA)
    center = 22
    red = (255, 0, 0, 140)
    pygame.draw.circle(crosshair_surf, red, (center, center), 20, 5)
    pygame.draw.line(crosshair_surf, red, (center - 22, center), (center + 22, center), 5)
    pygame.draw.line(crosshair_surf, red, (center, center - 22), (center, center + 22), 5)
    pygame.draw.circle(crosshair_surf, red, (center, center), 5, 2)
    surface.blit(crosshair_surf, (x - center, y - center))

def draw_button(
    surface: "pygame.Surface",
    rect: "pygame.Rect",
    text: str,
    font: "pygame.font.Font",
    color: tuple,
    hover: bool = False
) -> None:
    """
    Dessine un bouton stylisé.

    Args:
        surface (pygame.Surface): Surface cible.
        rect (pygame.Rect): Rectangle du bouton.
        text (str): Texte du bouton.
        font (pygame.font.Font): Police utilisée.
        color (tuple): Couleur principale.
        hover (bool): Si True, effet survol.
    """
    import pygame
    btn_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(btn_surf, (*color, 170), (0,0,rect.width,rect.height), border_radius=22)
    pygame.draw.rect(btn_surf, (200,200,220,120), (0,0,rect.width,rect.height), 3, border_radius=22)
    if hover:
        pygame.draw.rect(btn_surf, (255,255,255,180), (0,0,rect.width,rect.height), 4, border_radius=22)
    label = font.render(text, True, (255,255,255))
    btn_surf.blit(label, ((rect.width-label.get_width())//2, (rect.height-label.get_height())//2))
    surface.blit(btn_surf, (rect.x, rect.y))

# === Classes POO pour les entités du jeu ===
@dataclass
class Magpie:
    """
    Représente une pie (oiseau) dans le jeu.

    Attributs:
        pos (List[float]): Position [x, y].
        vel (List[float]): Vitesse [vx, vy].
        flying_away (bool): Si la pie s'envole.
        fly_away_timer (int): Timer d'envol.
    """
    pos: List[float] = field(default_factory=lambda: [0.0, 0.0])
    vel: List[float] = field(default_factory=lambda: [0.0, 0.0])
    flying_away: bool = False
    fly_away_timer: int = 0

    @classmethod
    def create_random(cls, speed: float, screen_height: int, body_radius: int) -> "Magpie":
        """
        Crée une pie avec position et vitesse aléatoires.

        Args:
            speed (float): Vitesse de base.
            screen_height (int): Hauteur de l'écran.
            body_radius (int): Rayon du corps.

        Returns:
            Magpie: Instance de pie.
        """
        start_x = body_radius
        start_y = random.randint(body_radius, screen_height - 150 - body_radius)
        vx = speed * random.uniform(0.9, 1.2)
        vy = random.uniform(-2, 2)
        return cls(pos=[start_x, start_y], vel=[vx, vy])

    def update(self, speed: float, width: int, height: int, body_radius: int) -> None:
        """
        Met à jour la position et l'état de la pie.

        Args:
            speed (float): Vitesse de base.
            width (int): Largeur de l'écran.
            height (int): Hauteur de l'écran.
            body_radius (int): Rayon du corps.
        """
        if self.flying_away:
            self.pos[1] -= 12
            self.fly_away_timer -= 1
            if self.pos[1] < -body_radius or self.fly_away_timer <= 0:
                self._respawn(speed, width, height)
        else:
            self._move_and_bounce(speed, width, height, body_radius)

    def _respawn(self, speed: float, width: int, height: int) -> None:
        """
        Replace la pie à une nouvelle position aléatoire.

        Args:
            speed (float): Vitesse de base.
            width (int): Largeur de l'écran.
            height (int): Hauteur de l'écran.
        """
        self.pos[0] = random.randint(100, width - 100)
        self.pos[1] = random.randint(200, height - 200)
        direction_x = 1 if random.random() < 0.5 else -1
        direction_y = 1 if random.random() < 0.5 else -1
        self.vel[0] = speed * direction_x
        self.vel[1] = speed * direction_y
        self.flying_away = False

    def _move_and_bounce(self, speed: float, width: int, height: int, body_radius: int) -> None:
        """
        Déplace la pie et gère les rebonds sur les bords.

        Args:
            speed (float): Vitesse de base.
            width (int): Largeur de l'écran.
            height (int): Hauteur de l'écran.
            body_radius (int): Rayon du corps.
        """
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        bounced = False
        if self.pos[0] < body_radius or self.pos[0] > width - body_radius:
            self.vel[0] *= -1
            bounced = True
        if self.pos[1] < body_radius or self.pos[1] > height - 150 - body_radius:
            self.vel[1] *= -1
            bounced = True
        if bounced and self.vel[0] == 0:
            self.vel[0] = speed * (1 if random.random() < 0.5 else -1)
        if bounced and self.vel[1] == 0:
            self.vel[1] = speed * (1 if random.random() < 0.5 else -1)

    def check_hit(self, mx: int, my: int, body_radius: int) -> bool:
        """
        Vérifie si la pie est touchée par un clic.

        Args:
            mx (int): Position X du clic.
            my (int): Position Y du clic.
            body_radius (int): Rayon du corps.

        Returns:
            bool: True si touchée, False sinon.
        """
        if not self.flying_away:
            dx = mx - self.pos[0]
            dy = my - self.pos[1]
            if dx * dx + dy * dy <= body_radius * body_radius:
                self.flying_away = True
                self.fly_away_timer = 30
                return True
        return False

    def get_position(self) -> Tuple[int, int]:
        """
        Retourne la position entière de la pie.

        Returns:
            Tuple[int, int]: (x, y)
        """
        return (int(self.pos[0]), int(self.pos[1]))

@dataclass
class Dog:
    """
    Représente le chien dans le jeu.

    Attributs:
        x (int): Position X.
        y (int): Position Y.
        jump_phase (float): Phase du saut.
        jumping (bool): Si le chien saute.
        jump_total (float): Durée totale du saut.
        jump_started (bool): Si le saut a commencé.
    """
    x: int
    y: int
    jump_phase: float = 0.0
    jumping: bool = False
    jump_total: float = field(default_factory=lambda: math.pi)
    jump_started: bool = False

    def start_jump(self) -> None:
        """
        Démarre l'animation de saut.
        """
        self.jump_started = True
        self.jumping = True
        self.jump_phase = 0.0

    def update_jump(self) -> bool:
        """
        Met à jour l'animation de saut.

        Returns:
            bool: True si le saut est terminé.
        """
        if self.jumping:
            self.jump_phase += 0.07
            if self.jump_phase >= self.jump_total:
                self.jumping = False
                return True
        return False

    def get_jump_y(self) -> int:
        """
        Retourne la position Y pendant le saut.

        Returns:
            int: Position Y actuelle.
        """
        if self.jumping:
            return self.y - int(30 * abs(math.sin(self.jump_phase)))
        return self.y

    def is_clicked(self, mx: int, my: int, img_width: int, img_height: int) -> bool:
        """
        Vérifie si le chien est cliqué.

        Args:
            mx (int): Position X du clic.
            my (int): Position Y du clic.
            img_width (int): Largeur de l'image.
            img_height (int): Hauteur de l'image.

        Returns:
            bool: True si cliqué, False sinon.
        """
        return (self.x <= mx <= self.x + img_width and 
                self.y <= my <= self.y + img_height)

def get_difficulty_settings(difficulty: str) -> Optional[dict]:
    """
    Retourne les paramètres de difficulté selon le niveau choisi.

    Args:
        difficulty (str): "Facile", "Moyen", "Difficile".

    Returns:
        dict | None: Paramètres de difficulté ou None si inconnu.
    """
    match difficulty:
        case "Facile":
            return {"magpie_count": 1, "speed": 3, "ammo": 10, "goal": 5, "time": 30, "label": "Facile"}
        case "Moyen":
            return {"magpie_count": 2, "speed": 5, "ammo": 15, "goal": 10, "time": 30, "label": "Moyen"}
        case "Difficile":
            return {"magpie_count": 4, "speed": 8, "ammo": 10, "goal": 10, "time": 30, "label": "Difficile"}
        case _:
            return None

def create_magpies(count: int, speed: float, screen_height: int, body_radius: int) -> List[Magpie]:
    """
    Crée une liste de pies aléatoires.

    Args:
        count (int): Nombre de pies.
        speed (float): Vitesse de base.
        screen_height (int): Hauteur de l'écran.
        body_radius (int): Rayon du corps.

    Returns:
        List[Magpie]: Liste de pies.
    """
    return [Magpie.create_random(speed, screen_height, body_radius) for _ in range(count)]

# Exemple d'exception personnalisée pour le jeu
class GameResourceError(Exception):
    """Exception levée lors d'une erreur de chargement de ressource du jeu."""
    pass

# === Fonction principale du jeu ===
def main() -> None:
    """
    Fonction principale du jeu. Initialise pygame, charge les ressources,
    gère le menu, la boucle de jeu et les événements.
    """
    import pygame
    try:
        pygame.init()
        pygame.mixer.init()
    except Exception as e:
        print(f"Erreur lors de l'initialisation de Pygame : {e}")
        sys.exit(1)

    try:
        WIDTH, HEIGHT = 800, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chasse Express')
    except pygame.error as e:
        print(f"Erreur lors de la création de la fenêtre : {e}")
        sys.exit(1)

    # === Chargement des images et sons ===
    global SHELTIE_IMG, BARKING_SOUND_PATH, AMBIANCE_MUSIC_PATH, TREE_IMG_PATH, BACKGROUND_IMG_PATH
    SHELTIE_IMG_PATH = "sheltie.png"
    try:
        sheltie_img_raw = pygame.image.load(SHELTIE_IMG_PATH).convert_alpha()
    except (pygame.error, FileNotFoundError) as e:
        print(f"Erreur lors du chargement de l'image {SHELTIE_IMG_PATH} : {e}")
        sys.exit(1)
    SHELTIE_IMG = pygame.transform.smoothscale(sheltie_img_raw, (200, 170))

    BARKING_SOUND_PATH = "barking.mp3"
    if os.path.exists(BARKING_SOUND_PATH):
        try:
            barking_sound = pygame.mixer.Sound(BARKING_SOUND_PATH)
        except (pygame.error, FileNotFoundError) as e:
            barking_sound = None
    else:
        barking_sound = None
    AMBIANCE_MUSIC_PATH = "ambiance.mp3"
    ambiance_music_exists = os.path.exists(AMBIANCE_MUSIC_PATH)

    TREE_IMG_PATH = "tree.png"
    try:
        tree_img_raw = pygame.image.load(TREE_IMG_PATH).convert_alpha()
    except (pygame.error, FileNotFoundError) as e:
        print(f"Erreur lors du chargement de l'image {TREE_IMG_PATH} : {e}")
        sys.exit(1)
    TREE_IMG = pygame.transform.smoothscale(tree_img_raw, (150, 240))
    def draw_tree(surface, x, y):
        if surface and TREE_IMG:
            surface.blit(TREE_IMG, (x, y))

    BACKGROUND_IMG_PATH = "background.jpg"
    if os.path.exists(BACKGROUND_IMG_PATH):
        try:
            BACKGROUND_IMG = pygame.image.load(BACKGROUND_IMG_PATH)
            BACKGROUND_IMG = pygame.transform.smoothscale(BACKGROUND_IMG, (WIDTH, HEIGHT))
        except (pygame.error, FileNotFoundError) as e:
            BACKGROUND_IMG = None
    else:
        BACKGROUND_IMG = None

    global OUTLINE_W, MAGPIE_BLACK, MAGPIE_WHITE, MAGPIE_BLUE, MAGPIE_BEAK, MAGPIE_HIGHLIGHT, RED
    OUTLINE_W = 3
    MAGPIE_BLACK = (25, 25, 25)
    MAGPIE_WHITE = (240, 240, 240)
    MAGPIE_BLUE = (50, 110, 210)
    MAGPIE_BEAK = (60, 60, 60)
    MAGPIE_HIGHLIGHT = (210, 210, 220)
    RED = (255, 0, 0)

    try:
        pygame.mouse.set_visible(True)
        clock = pygame.time.Clock()
        title_font = load_font(["NeutraText", "Neutra Text", "NeutraText-Book", "Montserrat"], 96)
        menu = True
        difficulty = None
        running = True

        DIFFICULTY_SETTINGS = {
            "Facile": {"magpie_count": 1, "speed": 3, "ammo": 10, "goal": 5, "time": 30, "label": "Facile"},
            "Moyen": {"magpie_count": 2, "speed": 5, "ammo": 15, "goal": 10, "time": 30, "label": "Moyen"},
            "Difficile": {"magpie_count": 4, "speed": 8, "ammo": 10, "goal": 10, "time": 30, "label": "Difficile"},
        }
        
        # === Boucle principale ===
        while running:
            # === Menu principal ===
            if menu:
                try:
                    draw_landfill_background(screen, BACKGROUND_IMG)
                    tree_x = 55
                    tree_y = HEIGHT - 110 - 240//2 - 10
                    draw_tree(screen, tree_x, tree_y)
                    tree2_x = WIDTH - 55 - 150
                    tree2_y = tree_y
                    draw_tree(screen, tree2_x, tree2_y)
                    dog_x = tree_x + 150 + 18
                    dog_y = HEIGHT - 170
                    screen.blit(SHELTIE_IMG, (dog_x, dog_y))
                    title_text = "Chasse Express"
                    gradient_colors = [
                        (255, 140, 0), (34, 139, 34), (72, 61, 139), (30, 144, 255)
                    ]
                    n = len(title_text)
                    color_steps = []
                    for i in range(n):
                        grad_pos = i / max(n-1, 1)
                        grad_idx = grad_pos * (len(gradient_colors)-1)
                        idx0 = int(grad_idx)
                        idx1 = min(idx0+1, len(gradient_colors)-1)
                        t = grad_idx - idx0
                        c1, c2 = gradient_colors[idx0], gradient_colors[idx1]
                        color = tuple(int(c1[j] + (c2[j] - c1[j]) * t) for j in range(3))
                        color_steps.append(color)
                    total_width = sum(title_font.size(ch)[0] for ch in title_text)
                    title_x = WIDTH//2 - total_width//2
                    title_y = 60
                    x = title_x
                    for i, ch in enumerate(title_text):
                        draw_text_with_outline(screen, ch, title_font, (x, title_y), color_steps[i])
                        x += title_font.size(ch)[0]
                    btn_font = get_best_font(44)
                    btns = [
                        (pygame.Rect(WIDTH//2-120, 200, 240, 60), "Facile", (120, 220, 120)),
                        (pygame.Rect(WIDTH//2-120, 280, 240, 60), "Moyen", (220, 200, 80)),
                        (pygame.Rect(WIDTH//2-120, 360, 240, 60), "Difficile", (220, 80, 80)),
                    ]
                    mx, my = pygame.mouse.get_pos()
                    hover_idx = -1
                    for i, (rect, text, color) in enumerate(btns):
                        hover = rect.collidepoint(mx, my)
                        draw_button(screen, rect, text, btn_font, color, hover)
                        if hover:
                            hover_idx = i
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            for i, (rect, text, color) in enumerate(btns):
                                if rect and rect.collidepoint(mx, my):
                                    difficulty = text
                                    menu = False
                    pygame.display.flip()
                    clock.tick(60)
                except Exception as e:
                    print(f"Erreur dans le menu : {e}")
                    continue

            if not menu and (not difficulty or get_difficulty_settings(difficulty) is None):
                menu = True
                difficulty = None
                continue

            if menu:
                continue
            
            try:
                settings = get_difficulty_settings(difficulty)
                if settings is None:
                    menu = True
                    continue
                    
                pygame.mouse.set_visible(False)
                score = 0
                ammo = settings.get("ammo", 10)
                goal = settings.get("goal", 5)
                magpie_count = max(1, settings.get("magpie_count", 1))
                speed = max(1, settings.get("speed", 1))
                round_time = max(5, settings.get("time", 30))
                label = settings.get("label", "Facile")
                tree_x = 55
                tree_y = HEIGHT - 110 - 240//2 - 10
                dog = Dog(x=tree_x + 150 + 18, y=HEIGHT - 170)
                magpies: List[Magpie] = []
                magpies_released = False
                timer_start = None
                running_round = True
                game_over = False
                win = False
                timer_frozen = False
                frozen_time_left = None
                try:
                    BIRD_IMG = load_icon('bird.png')
                    AMMO_IMG = load_icon('ammo.png')
                    TIMER_IMG = load_icon('timer.png')
                except GameResourceError as e:
                    print(f"Erreur critique de ressource : {e}")
                    BIRD_IMG = AMMO_IMG = TIMER_IMG = None
                while running_round:
                    try:
                        draw_landfill_background(screen, BACKGROUND_IMG)
                        draw_tree(screen, tree_x, tree_y)
                        draw_tree(screen, WIDTH - 55 - 150, tree_y)
                        if not dog.jump_started:
                            screen.blit(SHELTIE_IMG, (dog.x, dog.y))
                            instruct_font = pygame.font.SysFont(None, 36)
                            instruct = instruct_font.render("Cliquez sur le chien pour commencer !", True, (255,255,255))
                            screen.blit(instruct, (WIDTH//2 - instruct.get_width()//2, HEIGHT//2))
                        elif dog.jumping:
                            jump_finished = dog.update_jump()
                            screen.blit(SHELTIE_IMG, (dog.x, dog.get_jump_y()))
                            if jump_finished:
                                magpies_released = True
                                timer_start = pygame.time.get_ticks()
                        else:
                            screen.blit(SHELTIE_IMG, (dog.x, dog.y))
                        if magpies_released:
                            if not magpies:
                                magpies = create_magpies(magpie_count, speed, HEIGHT, MAGPIE_BODY_RADIUS)
                            for m in magpies:
                                m.update(speed, WIDTH, HEIGHT, MAGPIE_BODY_RADIUS)
                                if not m.flying_away:
                                    draw_magpie(screen, m.get_position())
                        mx, my = pygame.mouse.get_pos()
                        draw_crosshair(screen, (mx, my))
                        if magpies_released:
                            if timer_frozen and frozen_time_left is not None:
                                time_left = frozen_time_left
                            else:
                                elapsed = (pygame.time.get_ticks() - timer_start) // 1000 if timer_start else 0
                                time_left = max(0, round_time - elapsed)
                            stat_font = get_panel_font(28)
                            label_font = get_best_font(28)
                            draw_status_panel(
                                screen, 10, 10, label, score, goal, ammo, time_left,
                                BIRD_IMG, AMMO_IMG, TIMER_IMG,
                                stat_font, label_font, get_panel_surface
                            )
                        if magpies_released:
                            if score >= goal:
                                win = True
                                game_over = True
                                if not timer_frozen:
                                    frozen_time_left = time_left if time_left is not None else 0
                                    timer_frozen = True
                            elif ammo <= 0 or (timer_start and time_left <= 0):
                                win = False
                                game_over = True
                                if not timer_frozen:
                                    frozen_time_left = time_left if time_left is not None else 0
                                    timer_frozen = True
                        if game_over:
                            over_font = pygame.font.SysFont(None, 64, bold=True)
                            msg = "Bravo ! Vous avez gagné !" if win else "Partie terminée !"
                            over_text = over_font.render(msg, True, (255, 255, 255))
                            screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 40))
                            sub_font = pygame.font.SysFont(None, 36)
                            sub_text = sub_font.render("Cliquez pour revenir au menu principal", True, (255, 255, 255))
                            screen.blit(sub_text, (WIDTH//2 - sub_text.get_width()//2, HEIGHT//2 + 30))
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                                running_round = False
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                mx, my = pygame.mouse.get_pos()
                                if not dog.jump_started:
                                    if dog.is_clicked(mx, my, SHELTIE_IMG.get_width(), SHELTIE_IMG.get_height()):
                                        if barking_sound:
                                            barking_sound.play()
                                        if ambiance_music_exists:
                                            pygame.mixer.music.load(AMBIANCE_MUSIC_PATH)
                                            pygame.mixer.music.play(-1)
                                        dog.start_jump()
                                if game_over:
                                    pygame.mixer.music.stop()
                                    running_round = False
                                    menu = True
                                    pygame.mouse.set_visible(True)
                                elif magpies_released:
                                    if ammo > 0:
                                        for m in magpies:
                                            if m.check_hit(mx, my, MAGPIE_BODY_RADIUS):
                                                score += 1
                                                break
                                        ammo -= 1
                        pygame.display.flip()
                        clock.tick(60)
                    except Exception as e:
                        print(f"Erreur dans la boucle de manche : {e}")
                        running_round = False
            except (KeyError, ValueError, TypeError) as e:
                print(f"Erreur de configuration de difficulté : {e}")
                menu = True
                continue
        pygame.quit()
        sys.exit()
    except Exception as e:
        print(f"Erreur fatale dans la fonction main : {e}")
        pygame.quit()
        sys.exit(1)

# === Point d'entrée principal ===
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'Erreur non traitée : {e}')
        sys.exit(1)

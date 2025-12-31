import pygame
import os
import random
import sys
import math




# === Initialisation de Pygame et de la fenêtre ===
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chasse Express')



# === Chargement des images et sons ===
SHELTIE_IMG_PATH = os.path.join(os.path.dirname(__file__), "sheltie.png")
sheltie_img_raw = pygame.image.load(SHELTIE_IMG_PATH).convert_alpha()
SHELTIE_IMG = pygame.transform.smoothscale(sheltie_img_raw, (200, 170))



BARKING_SOUND_PATH = os.path.join(os.path.dirname(__file__), "barking.mp3")
if os.path.exists(BARKING_SOUND_PATH):
    barking_sound = pygame.mixer.Sound(BARKING_SOUND_PATH)
else:
    barking_sound = None
AMBIANCE_MUSIC_PATH = os.path.join(os.path.dirname(__file__), "ambiance.mp3")
ambiance_music_exists = os.path.exists(AMBIANCE_MUSIC_PATH)



# === Fonctions de dessin des éléments ===
TREE_IMG_PATH = os.path.join(os.path.dirname(__file__), "tree.png")
tree_img_raw = pygame.image.load(TREE_IMG_PATH).convert_alpha()
TREE_IMG = pygame.transform.smoothscale(tree_img_raw, (150, 240))
def draw_tree(surface, x, y):
    surface.blit(TREE_IMG, (x, y))






# === Couleurs utilisées ===
OUTLINE_W = 3
MAGPIE_BLACK = (25, 25, 25)
MAGPIE_WHITE = (240, 240, 240)
MAGPIE_BLUE = (50, 110, 210)
MAGPIE_BEAK = (60, 60, 60)
MAGPIE_HIGHLIGHT = (210, 210, 220)
RED = (255, 0, 0)



# === Fond d'écran ===
BACKGROUND_IMG_PATH = os.path.join(os.path.dirname(__file__), "background.jpg")
if os.path.exists(BACKGROUND_IMG_PATH):
    BACKGROUND_IMG = pygame.image.load(BACKGROUND_IMG_PATH)
    BACKGROUND_IMG = pygame.transform.smoothscale(BACKGROUND_IMG, (WIDTH, HEIGHT))
else:
    BACKGROUND_IMG = None
def draw_landfill_background(surface):
    surface.blit(BACKGROUND_IMG, (0, 0))


# === Utilitaires de dessin ===
def draw_dog(surface, x, y, jump_phase, smile=True):
    surface.blit(SHELTIE_IMG, (x, y))

MAGPIE_BODY_RADIUS = 32

def draw_magpie(surface, pos):
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

def draw_crosshair(surface, pos):
    x, y = pos
    crosshair_surf = pygame.Surface((44, 44), pygame.SRCALPHA)
    center = 22
    red = (255, 0, 0, 140)
    pygame.draw.circle(crosshair_surf, red, (center, center), 20, 5)
    pygame.draw.line(crosshair_surf, red, (center - 22, center), (center + 22, center), 5)
    pygame.draw.line(crosshair_surf, red, (center, center - 22), (center, center + 22), 5)
    pygame.draw.circle(crosshair_surf, red, (center, center), 5, 2)
    surface.blit(crosshair_surf, (x - center, y - center))


def draw_button(surface, rect, text, font, color, hover=False):
    btn_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(btn_surf, (*color, 170), (0,0,rect.width,rect.height), border_radius=22)
    pygame.draw.rect(btn_surf, (200,200,220,120), (0,0,rect.width,rect.height), 3, border_radius=22)
    if hover:
        pygame.draw.rect(btn_surf, (255,255,255,180), (0,0,rect.width,rect.height), 4, border_radius=22)
    label = font.render(text, True, (255,255,255))
    btn_surf.blit(label, ((rect.width-label.get_width())//2, (rect.height-label.get_height())//2))
    surface.blit(btn_surf, (rect.x, rect.y))

def main():
    pygame.mouse.set_visible(True)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)
    # Tente de charger une police personnalisée (Montserrat ou Baloo 2)
    def get_custom_font(font_name, size):
        font_paths = [
            os.path.join(os.path.dirname(__file__), font_name + ".ttf"),
            os.path.join(os.path.dirname(__file__), font_name + "-Regular.ttf"),
            font_name + ".ttf",
            font_name + "-Regular.ttf"
        ]
        for path in font_paths:
            if os.path.exists(path):
                return pygame.font.Font(path, size)
        return pygame.font.SysFont(None, size)

    # Tente d'abord Neutra Text, puis Montserrat, puis la police système
    def get_best_font(size):
        for fname in ["NeutraText", "Neutra Text", "NeutraText-Book", "Montserrat"]:
            font_paths = [
                os.path.join(os.path.dirname(__file__), fname + ".ttf"),
                os.path.join(os.path.dirname(__file__), fname + "-Regular.ttf"),
                fname + ".ttf",
                fname + "-Regular.ttf"
            ]
            for path in font_paths:
                if os.path.exists(path):
                    return pygame.font.Font(path, size)
        return pygame.font.SysFont(None, size)

    title_font = get_best_font(96)
    menu = True
    difficulty = None
    running = True
    while running:
        if menu:
            draw_landfill_background(screen)
            # Dessine l'arbre et le chien pour le menu
            tree_x = 55
            tree_y = HEIGHT - 110 - 240//2 - 10  # Plus haut et plus grand
            draw_tree(screen, tree_x, tree_y)
            # Dessine le deuxième arbre de l'autre côté
            tree2_x = WIDTH - 55 - 150  # 150 is tree width
            tree2_y = tree_y
            draw_tree(screen, tree2_x, tree2_y)
            dog_x = tree_x + 150 + 18  # largeur de l'arbre + marge
            dog_y = HEIGHT - 170  # Position cohérente pour le menu et le jeu
            screen.blit(SHELTIE_IMG, (dog_x, dog_y))
            # Titre avec effet de dégradé brillant
            title_text = "Chasse Express"
            title_size = 96
            title_font = get_best_font(title_size)
            shadow_color = (0, 0, 0)
            outline_color = (255, 255, 255)
            # Couleurs du dégradé (de gauche à droite) : orange -> vert -> bleu/violet foncé -> bleu (pas de rose)
            gradient_colors = [
                (255, 140, 0),    # orange (darker, less yellow)
                (34, 139, 34),    # green (forest green)
                (72, 61, 139),    # dark slate blue (darker purple/blue)
                (30, 144, 255),   # dodger blue (bright blue)
            ]
            # Fonction pour interpoler entre deux couleurs
            def lerp_color(c1, c2, t):
                return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
            # Crée une couleur pour chaque lettre
            n = len(title_text)
            color_steps = []
            for i in range(n):
                # Map i to gradient
                grad_pos = i / max(n-1, 1)
                grad_idx = grad_pos * (len(gradient_colors)-1)
                idx0 = int(grad_idx)
                idx1 = min(idx0+1, len(gradient_colors)-1)
                t = grad_idx - idx0
                color = lerp_color(gradient_colors[idx0], gradient_colors[idx1], t)
                color_steps.append(color)
            # Rendu de l'ombre et du contour pour chaque lettre
            letter_surfs = []
            for i, ch in enumerate(title_text):
                # Main letter
                surf = title_font.render(ch, True, color_steps[i])
                # Outline
                outline_surfs = []
                for dx in [-2, 0, 2]:
                    for dy in [-2, 0, 2]:
                        if dx != 0 or dy != 0:
                            outline_surfs.append((dx, dy, title_font.render(ch, True, outline_color)))
                # Shadow
                shadow_surf = title_font.render(ch, True, shadow_color)
                letter_surfs.append({
                    'main': surf,
                    'outline': outline_surfs,
                    'shadow': shadow_surf
                })
            # Calcule la largeur totale
            total_width = sum(s['main'].get_width() for s in letter_surfs)
            title_x = WIDTH//2 - total_width//2
            title_y = 60
            # Affiche chaque lettre avec ombre et contour
            x = title_x
            for s in letter_surfs:
                # Shadow
                screen.blit(s['shadow'], (x+4, title_y+4))
                # Outline
                for dx, dy, surf in s['outline']:
                    screen.blit(surf, (x+dx, title_y+dy))
                # Main letter
                screen.blit(s['main'], (x, title_y))
                x += s['main'].get_width()
            # Boutons
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
                        if rect.collidepoint(mx, my):
                            difficulty = text
                            menu = False
            pygame.display.flip()
            clock.tick(60)
            continue

        # --- GAMEPLAY ---
        # --- Difficulty settings ---
        DIFFICULTY_SETTINGS = {
            "Facile": {"magpie_count": 1, "speed": 3, "ammo": 10, "goal": 5, "time": 30, "label": "Facile"},
            "Moyen": {"magpie_count": 2, "speed": 5, "ammo": 15, "goal": 10, "time": 30, "label": "Moyen"},
            "Difficile": {"magpie_count": 4, "speed": 8, "ammo": 10, "goal": 10, "time": 30, "label": "Difficile"},
        }
        if difficulty in DIFFICULTY_SETTINGS:
            settings = DIFFICULTY_SETTINGS[difficulty]
            pygame.mouse.set_visible(False)
            score = 0
            ammo = settings["ammo"]
            goal = settings["goal"]
            magpie_count = settings["magpie_count"]
            speed = settings["speed"]
            round_time = settings["time"]
            label = settings["label"]
            # --- Dog jump intro ---
            tree_x = 55
            tree_y = HEIGHT - 110 - 240//2 - 10
            dog_x = tree_x + 150 + 18
            dog_y = HEIGHT - 170  # Match menu position for consistency
            dog_jump_phase = 0
            dog_jumping = False
            dog_jump_total = math.pi
            jump_started = False
            magpies = []
            magpies_released = False
            timer_start = None
            running_round = True
            game_over = False
            win = False
            timer_frozen = False
            frozen_time_left = None
            # --- Load panel icons ---
            BIRD_IMG = pygame.image.load('bird.png').convert_alpha()
            AMMO_IMG = pygame.image.load('ammo.png').convert_alpha()
            TIMER_IMG = pygame.image.load('timer.png').convert_alpha()
            while running_round:
                draw_landfill_background(screen)
                # Dessine l'arbre
                draw_tree(screen, tree_x, tree_y)
                # Dessine le deuxième arbre de l'autre côté
                draw_tree(screen, WIDTH - 55 - 150, tree_y)
                # Animation du saut du chien
                if not jump_started:
                    screen.blit(SHELTIE_IMG, (dog_x, dog_y))
                    # Affiche l'instruction de cliquer sur le chien
                    instruct_font = pygame.font.SysFont(None, 36)
                    instruct = instruct_font.render("Cliquez sur le chien pour commencer !", True, (255,255,255))
                    screen.blit(instruct, (WIDTH//2 - instruct.get_width()//2, HEIGHT//2))
                elif dog_jumping:
                    dog_jump_phase += 0.07
                    jump_y = dog_y - int(30 * abs(math.sin(dog_jump_phase)))
                    screen.blit(SHELTIE_IMG, (dog_x, jump_y))
                    if dog_jump_phase >= dog_jump_total:
                        dog_jumping = False
                        magpies_released = True
                        timer_start = pygame.time.get_ticks()
                else:
                    screen.blit(SHELTIE_IMG, (dog_x, dog_y))
                # Mouvement des pies (après le saut du chien seulement)
                if magpies_released:
                    if not magpies:
                        # Les pies commencent à une position y aléatoire sur le bord gauche, se déplacent vers la droite avec une variation verticale
                        for i in range(magpie_count):
                            start_x = 0 + MAGPIE_BODY_RADIUS
                            start_y = random.randint(MAGPIE_BODY_RADIUS, HEIGHT - 150 - MAGPIE_BODY_RADIUS)
                            vx = speed * random.uniform(0.9, 1.2)
                            vy = random.uniform(-2, 2)
                            magpies.append({
                                'pos': [start_x, start_y],
                                'vel': [vx, vy],
                                'flying_away': False,
                                'fly_away_timer': 0
                            })
                    for m in magpies:
                        if m['flying_away']:
                            m['pos'][1] -= 12
                            m['fly_away_timer'] -= 1
                            if m['pos'][1] < -MAGPIE_BODY_RADIUS or m['fly_away_timer'] <= 0:
                                m['pos'][0] = random.randint(100, WIDTH-100)
                                m['pos'][1] = random.randint(200, HEIGHT-200)
                                # Toujours en diagonale : vx et vy non nuls
                                while True:
                                    direction_x = 1 if random.random() < 0.5 else -1
                                    direction_y = 1 if random.random() < 0.5 else -1
                                    if direction_x != 0 and direction_y != 0:
                                        break
                                m['vel'][0] = speed * direction_x
                                m['vel'][1] = speed * direction_y
                                m['flying_away'] = False
                        else:
                            m['pos'][0] += m['vel'][0]
                            m['pos'][1] += m['vel'][1]
                            bounced = False
                            if m['pos'][0] < MAGPIE_BODY_RADIUS or m['pos'][0] > WIDTH - MAGPIE_BODY_RADIUS:
                                m['vel'][0] *= -1
                                bounced = True
                            if m['pos'][1] < MAGPIE_BODY_RADIUS or m['pos'][1] > HEIGHT - 150 - MAGPIE_BODY_RADIUS:
                                m['vel'][1] *= -1
                                bounced = True
                            if bounced and m['vel'][0] == 0:
                                m['vel'][0] = speed * (1 if random.random() < 0.5 else -1)
                            if bounced and m['vel'][1] == 0:
                                m['vel'][1] = speed * (1 if random.random() < 0.5 else -1)
                            draw_magpie(screen, (int(m['pos'][0]), int(m['pos'][1])))
                # Affiche le statut
                mx, my = pygame.mouse.get_pos()
                draw_crosshair(screen, (mx, my))
                if magpies_released:
                    if timer_frozen and frozen_time_left is not None:
                        time_left = frozen_time_left
                    else:
                        time_left = round_time - ((pygame.time.get_ticks() - timer_start) // 1000)
                    # --- Mise en page améliorée du panneau d'informations ---
                    # Paramètres du panneau
                    padding_x, padding_y = 24, 14
                    section_width = 120
                    icon_text_gap = 10
                    panel_height = 48 + 2*padding_y
                    panel_width = 4*section_width + 2*padding_x
                    panel_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
                    # Ombre (arrondie, forme du panneau)
                    shadow = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
                    pygame.draw.rect(shadow, (0,0,0,40), (0,0,panel_width,panel_height), border_radius=24)
                    screen.blit(shadow, (12, 20))  # Légèrement décalé pour un effet d'ombre douce
                    # Fond du panneau (plus clair, plus lisible)
                    # Dessine uniquement un rectangle arrondi pour le fond et la bordure
                    # Dessine un fond et une bordure arrondis pour un contour parfait
                    pygame.draw.rect(panel_surf, (245, 248, 255, 230), (0,0,panel_width,panel_height), border_radius=24)
                    pygame.draw.rect(panel_surf, (200,200,220,180), (0,0,panel_width,panel_height), 2, border_radius=24)
                    # Polices
                    label_font = pygame.font.SysFont('arial', 26, bold=True)
                    stat_font = pygame.font.SysFont('arial', 28, bold=True)
                    emoji_font = pygame.font.SysFont('Segoe UI Emoji', 28, bold=True)
                    # --- Amélioré : espacement dynamique et uniforme pour le contenu du panneau ---
                    center_y = panel_height // 2
                    # Affiche le panneau avec du padding pour que les coins arrondis soient visibles
                    # ...code existant...
                    # Prépare tous les éléments rendus et leurs largeurs
                    niveau_label = f"Niveau : {label}"
                    niveau_text = label_font.render(niveau_label, True, (0,0,0))
                    magpie_size = stat_font.get_height()
                    magpie_img = pygame.transform.smoothscale(BIRD_IMG, (magpie_size, magpie_size))
                    magpie_text = stat_font.render(f"{score}/{goal}", True, (30,30,30))
                    ammo_size = stat_font.get_height()
                    ammo_img = pygame.transform.smoothscale(AMMO_IMG, (ammo_size, ammo_size))
                    ammo_text = stat_font.render(f"{ammo}", True, (30,30,30))
                    timer_size = stat_font.get_height()
                    timer_img = pygame.transform.smoothscale(TIMER_IMG, (timer_size, timer_size))
                    timer_text = stat_font.render(f"{time_left}s", True, (30,30,30))
                    icon_text_gap = 10
                    section_gap = 32
                    # Calculate total width needed for each group
                    group1_w = niveau_text.get_width()
                    group2_w = magpie_img.get_width() + icon_text_gap + magpie_text.get_width()
                    group3_w = ammo_img.get_width() + icon_text_gap + ammo_text.get_width()
                    group4_w = timer_img.get_width() + icon_text_gap + timer_text.get_width()
                    total_content_w = group1_w + group2_w + group3_w + group4_w + 3*section_gap
                    # Calculate starting x for first group to center all content
                    start_x = (panel_width - total_content_w) // 2
                    x = start_x
                    # 1. Libellé du niveau
                    niveau_rect = niveau_text.get_rect()
                    niveau_rect.midleft = (x, center_y)
                    panel_surf.blit(niveau_text, niveau_rect)
                    x += group1_w + section_gap
                    # 2. Icône de pie et nombre capturées
                    magpie_rect = magpie_img.get_rect()
                    magpie_rect.midleft = (x, center_y)
                    panel_surf.blit(magpie_img, magpie_rect)
                    magpie_text_rect = magpie_text.get_rect()
                    magpie_text_rect.midleft = (magpie_rect.right + icon_text_gap, center_y)
                    panel_surf.blit(magpie_text, magpie_text_rect)
                    x += group2_w + section_gap
                    # 3. Icône de munitions et nombre
                    ammo_rect = ammo_img.get_rect()
                    ammo_rect.midleft = (x, center_y)
                    panel_surf.blit(ammo_img, ammo_rect)
                    ammo_text_rect = ammo_text.get_rect()
                    ammo_text_rect.midleft = (ammo_rect.right + icon_text_gap, center_y)
                    panel_surf.blit(ammo_text, ammo_text_rect)
                    x += group3_w + section_gap
                    # 4. Icône de minuterie et valeur
                    timer_rect = timer_img.get_rect()
                    timer_rect.midleft = (x, center_y)
                    panel_surf.blit(timer_img, timer_rect)
                    timer_text_rect = timer_text.get_rect()
                    timer_text_rect.midleft = (timer_rect.right + icon_text_gap, center_y)
                    panel_surf.blit(timer_text, timer_text_rect)
                    # Affiche le panneau à l'écran avec plus de padding
                    screen.blit(panel_surf, (10, 10))
                # Conditions de fin de partie
                if magpies_released:
                    if score >= goal:
                        win = True
                        game_over = True
                        if not timer_frozen:
                            frozen_time_left = time_left
                            timer_frozen = True
                    elif ammo <= 0 or (timer_start and time_left <= 0):
                        win = False
                        game_over = True
                        if not timer_frozen:
                            frozen_time_left = time_left
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
                        if not jump_started:
                            # Vérifie si le clic est sur le chien
                            if dog_x <= mx <= dog_x + SHELTIE_IMG.get_width() and dog_y <= my <= dog_y + SHELTIE_IMG.get_height():
                                if barking_sound:
                                    barking_sound.play()
                                    # Joue la musique d'ambiance après l'aboiement
                                    if ambiance_music_exists:
                                        pygame.mixer.music.load(AMBIANCE_MUSIC_PATH)
                                        pygame.mixer.music.play(-1)
                                else:
                                    if ambiance_music_exists:
                                        pygame.mixer.music.load(AMBIANCE_MUSIC_PATH)
                                        pygame.mixer.music.play(-1)
                                jump_started = True
                                dog_jumping = True
                        elif dog_jumping:
                            pass
                        if game_over:
                            # Arrête la musique d'ambiance à la fin de la partie
                            pygame.mixer.music.stop()
                            over_font = pygame.font.SysFont(None, 64, bold=True)
                            msg = "Bravo ! Vous avez gagné !" if win else "Partie terminée !"
                            over_text = over_font.render(msg, True, (0, 0, 0))
                            screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 40))
                            sub_font = pygame.font.SysFont(None, 36)
                            sub_text = sub_font.render("Cliquez pour revenir au menu principal", True, (0, 0, 0))
                            screen.blit(sub_text, (WIDTH//2 - sub_text.get_width()//2, HEIGHT//2 + 30))
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                running_round = False
                                menu = True
                                pygame.mouse.set_visible(True)
                        elif magpies_released:
                            if ammo > 0:
                                for m in magpies:
                                    if not m['flying_away']:
                                        dx = mx - m['pos'][0]
                                        dy = my - m['pos'][1]
                                        if dx * dx + dy * dy <= MAGPIE_BODY_RADIUS * MAGPIE_BODY_RADIUS:
                                            score += 1
                                            m['flying_away'] = True
                                            m['fly_away_timer'] = 30
                                            break
                                ammo -= 1
                pygame.display.flip()
                clock.tick(60)
            continue
        else:
            menu = True
    pygame.quit()
    sys.exit()
if __name__ == '__main__':
    try:
        main()
    except ImportError:
        print('Pygame is required. Install it with: pip install pygame')

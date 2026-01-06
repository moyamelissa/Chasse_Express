# =========================
# Module principal du jeu Chasse Express
# =========================
# Ce module gère l'initialisation, le menu principal, la boucle de jeu, le score et la gestion des ressources.
# Toutes les fonctions et classes externes sont importées au début pour une structure claire et modulaire.

from entities import Magpie, Dog
from utils import ErreurRessourceJeu
from ui import (
    dessiner_texte_avec_contour, dessiner_icone_texte, obtenir_surface_panneau, dessiner_panneau_etat,
    dessiner_fond, dessiner_chien, dessiner_pie, dessiner_viseur, dessiner_bouton
)
from settings import (
    WIDTH, HEIGHT, OUTLINE_W, MAGPIE_BLACK, MAGPIE_WHITE, MAGPIE_BLUE, MAGPIE_BEAK,
    MAGPIE_HIGHLIGHT, RED, MAGPIE_BODY_RADIUS, DIFFICULTY_SETTINGS,
    SHELTIE_IMG_PATH, BARKING_SOUND_PATH, AMBIANCE_MUSIC_PATH, TREE_IMG_PATH,
    BACKGROUND_IMG_PATH, BIRD_IMG_PATH, AMMO_IMG_PATH, TIMER_IMG_PATH
)
from resources import load_image, load_sound, load_font, load_icon

import pygame
import sys

def main():
    """
    Point d'entrée principal du jeu Chasse Express.
    - Initialise Pygame et les ressources audio/visuelles.
    - Affiche le menu principal et gère la sélection de la difficulté.
    - Lance la boucle de jeu principale pour chaque partie.
    - Gère le score, les munitions, le temps et la victoire/défaite.
    """
    # === Initialisation de Pygame ===
    try:
        pygame.init()
        pygame.mixer.init()
    except Exception as e:
        print(f"Erreur lors de l'initialisation de Pygame : {e}")
        sys.exit(1)

    # === Création de la fenêtre principale ===
    try:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chasse Express')
    except pygame.error as e:
        print(f"Erreur lors de la création de la fenêtre : {e}")
        sys.exit(1)

    # === Chargement des ressources graphiques et audio ===
    try:
        sheltie_img = load_image(SHELTIE_IMG_PATH)
        if sheltie_img:
            sheltie_img = pygame.transform.smoothscale(sheltie_img, (200, 170))
        else:
            raise ErreurRessourceJeu(f"Image non trouvée : {SHELTIE_IMG_PATH}")

        tree_img = load_image(TREE_IMG_PATH)
        if tree_img:
            tree_img = pygame.transform.smoothscale(tree_img, (150, 240))
        else:
            raise ErreurRessourceJeu(f"Image non trouvée : {TREE_IMG_PATH}")

        background_img = load_image(BACKGROUND_IMG_PATH)
        if background_img:
            background_img = pygame.transform.smoothscale(background_img, (WIDTH, HEIGHT))

        bird_icon = load_icon(BIRD_IMG_PATH)
        ammo_icon = load_icon(AMMO_IMG_PATH)
        timer_icon = load_icon(TIMER_IMG_PATH)

        barking_sound = load_sound(BARKING_SOUND_PATH)
        ambiance_music_exists = load_sound(AMBIANCE_MUSIC_PATH) is not None

    except ErreurRessourceJeu as e:
        print(f"Erreur critique de ressource : {e}")
        sys.exit(1)

    def dessiner_arbre(surface, x, y):
        """
        Dessine un arbre sur la surface donnée.
        :param surface: Surface pygame
        :param x: Position x
        :param y: Position y
        """
        if surface and tree_img:
            surface.blit(tree_img, (x, y))

    # === Variables de contrôle du jeu ===
    pygame.mouse.set_visible(True)
    clock = pygame.time.Clock()
    title_font = pygame.font.SysFont("Montserrat", 96)
    menu = True
    difficulty = None
    running = True

    # === Boucle principale du jeu ===
    while running:
        # --- Affichage du menu principal ---
        if menu:
            try:
                dessiner_fond(screen, background_img)
                tree_x = 55
                tree_y = HEIGHT - 110 - 240//2 - 10
                dessiner_arbre(screen, tree_x, tree_y)
                tree2_x = WIDTH - 55 - 150
                tree2_y = tree_y
                dessiner_arbre(screen, tree2_x, tree2_y)
                dog_x = tree_x + 150 + 18
                dog_y = HEIGHT - 170
                screen.blit(sheltie_img, (dog_x, dog_y))
                title_text = "Chasse Express"
                # --- Génération du titre avec dégradé ---
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
                    dessiner_texte_avec_contour(screen, ch, title_font, (x, title_y), color_steps[i])
                    x += title_font.size(ch)[0]
                # --- Boutons de sélection de difficulté ---
                btn_font = pygame.font.SysFont("Montserrat", 44)
                btns = [
                    (pygame.Rect(WIDTH//2-120, 200, 240, 60), "Facile", (120, 220, 120)),
                    (pygame.Rect(WIDTH//2-120, 280, 240, 60), "Moyen", (220, 200, 80)),
                    (pygame.Rect(WIDTH//2-120, 360, 240, 60), "Difficile", (220, 80, 80)),
                ]
                mx, my = pygame.mouse.get_pos()
                hover_idx = -1
                for i, (rect, text, color) in enumerate(btns):
                    hover = rect.collidepoint(mx, my)
                    dessiner_bouton(screen, rect, text, btn_font, color, hover)
                    if hover:
                        hover_idx = i
                # --- Gestion des événements du menu ---
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

        # --- Vérification de la difficulté sélectionnée ---
        if not menu and (not difficulty or difficulty not in DIFFICULTY_SETTINGS):
            menu = True
            difficulty = None
            continue

        if menu:
            continue

        # --- Boucle de la partie (manche) ---
        try:
            settings = DIFFICULTY_SETTINGS[difficulty]
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
            magpies = []
            magpies_released = False
            timer_start = None
            running_round = True
            game_over = False
            win = False
            timer_frozen = False
            frozen_time_left = None

            while running_round:
                try:
                    dessiner_fond(screen, background_img)
                    dessiner_arbre(screen, tree_x, tree_y)
                    dessiner_arbre(screen, WIDTH - 55 - 150, tree_y)
                    # --- Affichage du chien et gestion du saut ---
                    if not dog.jump_started:
                        screen.blit(sheltie_img, (dog.x, dog.y))
                        instruct_font = pygame.font.SysFont(None, 36)
                        instruct = instruct_font.render("Cliquez sur le chien pour commencer !", True, (255,255,255))
                        screen.blit(instruct, (WIDTH//2 - instruct.get_width()//2, HEIGHT//2))
                    elif dog.jumping:
                        jump_finished = dog.update_jump()
                        screen.blit(sheltie_img, (dog.x, dog.get_jump_y()))
                        if jump_finished:
                            magpies_released = True
                            timer_start = pygame.time.get_ticks()
                    else:
                        screen.blit(sheltie_img, (dog.x, dog.y))
                    # --- Gestion des pies (oiseaux) ---
                    if magpies_released:
                        if not magpies:
                            magpies = [Magpie.create_random(speed, HEIGHT, MAGPIE_BODY_RADIUS) for _ in range(magpie_count)]
                        for m in magpies:
                            m.update(speed, WIDTH, HEIGHT, MAGPIE_BODY_RADIUS)
                            if not m.flying_away:
                                dessiner_pie(screen, m.get_position())
                    # --- Affichage du viseur ---
                    mx, my = pygame.mouse.get_pos()
                    dessiner_viseur(screen, (mx, my))
                    # --- Affichage du panneau d'état ---
                    if magpies_released:
                        if timer_frozen and frozen_time_left is not None:
                            time_left = frozen_time_left
                        else:
                            elapsed = (pygame.time.get_ticks() - timer_start) // 1000 if timer_start else 0
                            time_left = max(0, round_time - elapsed)
                        stat_font = pygame.font.SysFont("Consolas", 28)
                        label_font = pygame.font.SysFont("Montserrat", 28)
                        dessiner_panneau_etat(
                            screen, 10, 10, label, score, goal, ammo, time_left,
                            bird_icon, ammo_icon, timer_icon,
                            stat_font, label_font, obtenir_surface_panneau
                        )
                    # --- Gestion de la victoire/défaite ---
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
                    # --- Affichage du message de fin de partie ---
                    if game_over:
                        over_font = pygame.font.SysFont(None, 64, bold=True)
                        msg = "Bravo ! Vous avez gagné !" if win else "Partie terminée !"
                        over_text = over_font.render(msg, True, (255, 255, 255))
                        screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 40))
                        sub_font = pygame.font.SysFont(None, 36)
                        sub_text = sub_font.render("Cliquez pour revenir au menu principal", True, (255, 255, 255))
                        screen.blit(sub_text, (WIDTH//2 - sub_text.get_width()//2, HEIGHT//2 + 30))
                    # --- Gestion des événements de la partie ---
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            running_round = False
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            mx, my = pygame.mouse.get_pos()
                            if not dog.jump_started:
                                if dog.is_clicked(mx, my, sheltie_img.get_width(), sheltie_img.get_height()):
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
    # === Fin du jeu ===
    pygame.quit()
    sys.exit()



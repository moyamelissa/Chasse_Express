import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# === Imports pour les tests ===
from ui import (
    obtenir_surface_panneau, dessiner_icone_texte, dessiner_texte_avec_contour,
    dessiner_panneau_etat, dessiner_fond
)
from resources import load_font, load_icon
from settings import DIFFICULTY_SETTINGS
from entities import Magpie, Dog
from chasse_express import (
    calcule_score, consomme_munition, verifie_victoire, verifie_defaite
)

import unittest

# === Tests settings.py ===
class TestGetDifficultySettings(unittest.TestCase):
    def test_facile(self):
        # Vérifie les paramètres retournés pour "Facile"
        params = DIFFICULTY_SETTINGS.get("Facile")
        self.assertIsInstance(params, dict)
        self.assertEqual(params["magpie_count"], 1)
        self.assertEqual(params["label"], "Facile")

    def test_moyen(self):
        # Vérifie les paramètres retournés pour "Moyen"
        params = DIFFICULTY_SETTINGS.get("Moyen")
        self.assertIsInstance(params, dict)
        self.assertEqual(params["magpie_count"], 2)
        self.assertEqual(params["label"], "Moyen")

    def test_difficile(self):
        # Vérifie les paramètres retournés pour "Difficile"
        params = DIFFICULTY_SETTINGS.get("Difficile")
        self.assertIsInstance(params, dict)
        self.assertEqual(params["magpie_count"], 4)
        self.assertEqual(params["label"], "Difficile")

    def test_invalide(self):
        # Vérifie qu'une difficulté inconnue retourne None
        params = DIFFICULTY_SETTINGS.get("Impossible")
        self.assertIsNone(params)

# === Tests entities.py ===
class TestMagpie(unittest.TestCase):
    def test_create_random(self):
        # Vérifie la création aléatoire d'une pie
        magpie = Magpie.create_random(3, 600, 32)
        self.assertIsInstance(magpie, Magpie)
        self.assertEqual(len(magpie.pos), 2)
        self.assertEqual(len(magpie.vel), 2)

    def test_check_hit(self):
        # Vérifie que check_hit détecte un clic sur la pie
        magpie = Magpie(pos=[100, 100], vel=[0, 0])
        hit = magpie.check_hit(100, 100, 32)
        self.assertTrue(hit)
        self.assertTrue(magpie.flying_away)

    def test_update_and_respawn(self):
        # Vérifie le respawn après avoir été touchée
        magpie = Magpie(pos=[100, 100], vel=[0, 0], flying_away=True, fly_away_timer=1)
        magpie.update(3, 800, 600, 32)
        self.assertFalse(magpie.flying_away)

    def test_check_hit_outside(self):
        # Vérifie que check_hit retourne False hors de la pie
        magpie = Magpie(pos=[100, 100], vel=[0, 0])
        hit = magpie.check_hit(200, 200, 32)
        self.assertFalse(hit)
        self.assertFalse(magpie.flying_away)

    def test_update_bounce(self):
        # Vérifie le rebond sur les bords
        magpie = Magpie(pos=[10, 10], vel=[-5, -5])
        magpie.update(3, 800, 600, 32)
        self.assertTrue(magpie.vel[0] > 0 or magpie.vel[1] > 0)

    def test_respawn_random(self):
        # Vérifie que _respawn place la pie dans les bornes
        magpie = Magpie()
        magpie._respawn(3, 800, 600)
        self.assertTrue(100 <= magpie.pos[0] <= 700)
        self.assertTrue(200 <= magpie.pos[1] <= 400)

    def test_update_no_bounce(self):
        # Vérifie update sans rebond ni fly_away
        magpie = Magpie(pos=[400, 300], vel=[1, 1])
        magpie.update(3, 800, 600, 32)
        self.assertFalse(magpie.flying_away)

    def test_update_flying_away(self):
        # Vérifie update avec flying_away True et fly_away_timer > 1
        magpie = Magpie(pos=[100, 100], vel=[0, 0], flying_away=True, fly_away_timer=5)
        magpie.update(3, 800, 600, 32)
        self.assertTrue(magpie.flying_away)
        self.assertEqual(magpie.fly_away_timer, 4)

    def test_check_hit_already_flying(self):
        # Vérifie check_hit quand la pie est déjà flying_away
        magpie = Magpie(pos=[100, 100], vel=[0, 0], flying_away=True)
        hit = magpie.check_hit(100, 100, 32)
        self.assertFalse(hit)

class TestDog(unittest.TestCase):
    def test_start_jump_and_update(self):
        # Vérifie que le saut démarre et se termine correctement
        dog = Dog(x=0, y=100)
        dog.start_jump()
        self.assertTrue(dog.jumping)
        finished = False
        for _ in range(100):
            finished = dog.update_jump()
            if finished:
                break
        self.assertTrue(finished)
        self.assertFalse(dog.jumping)

    def test_get_jump_y(self):
        # Vérifie que la position Y change pendant le saut
        dog = Dog(x=0, y=100)
        dog.start_jump()
        y1 = dog.get_jump_y()
        dog.update_jump()
        y2 = dog.get_jump_y()
        self.assertNotEqual(y1, y2)

    def test_is_clicked(self):
        # Vérifie la détection de clic sur le chien
        dog = Dog(x=10, y=20)
        self.assertTrue(dog.is_clicked(50, 50, 200, 170))
        self.assertFalse(dog.is_clicked(500, 500, 200, 170))

    def test_jump_not_started(self):
        # Vérifie get_jump_y si le saut n'a pas commencé
        dog = Dog(x=0, y=100)
        self.assertEqual(dog.get_jump_y(), 100)

    def test_is_clicked_outside(self):
        # Vérifie is_clicked hors de l'image
        dog = Dog(x=10, y=20)
        self.assertFalse(dog.is_clicked(0, 0, 200, 170))

    def test_update_jump_not_jumping(self):
        # Vérifie update_jump quand le chien ne saute pas
        dog = Dog(x=0, y=100)
        self.assertFalse(dog.update_jump())

    def test_get_jump_y_not_jumping(self):
        # Vérifie get_jump_y quand le chien ne saute pas
        dog = Dog(x=0, y=100)
        self.assertEqual(dog.get_jump_y(), 100)

# === Tests ui.py ===
class TestUIFunctions(unittest.TestCase):
    def test_draw_icon_text(self):
        import pygame
        pygame.init()
        surf = pygame.Surface((100, 40))
        font = load_font("Consolas", 20)
        dessiner_icone_texte(surf, None, "Test", font, (0,0), 24)

    def test_draw_text_with_outline(self):
        import pygame
        pygame.init()
        surf = pygame.Surface((100, 40))
        font = load_font("Consolas", 20)
        dessiner_texte_avec_contour(surf, "Test", font, (0,0), (255,255,255))

    def test_get_panel_surface(self):
        surf, shadow = obtenir_surface_panneau(100, 40)
        self.assertIsNotNone(surf)
        self.assertIsNotNone(shadow)

    def test_draw_status_panel(self):
        import pygame
        pygame.init()
        surf = pygame.Surface((400, 80))
        font = load_font("Consolas", 20)
        stat_font = load_font("Consolas", 20)
        dessiner_panneau_etat(
            surf, 0, 0, "Test", 1, 2, 3, 4,
            None, None, None,
            stat_font, font, obtenir_surface_panneau
        )

    def test_draw_landfill_background(self):
        import pygame
        pygame.init()
        surf = pygame.Surface((100, 40))
        dessiner_fond(surf, None)

# === Tests resources.py ===
class TestResourcesFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import pygame
        pygame.init()

    def test_get_best_font(self):
        font = load_font("Consolas", 20)
        self.assertIsNotNone(font)

    def test_get_panel_font(self):
        font = load_font("Consolas", 20)
        self.assertIsNotNone(font)

    def test_load_icon_fallback(self):
        icon = load_icon("notfoundicon.png")
        self.assertIsNotNone(icon)

    def test_load_font_fallback(self):
        font = load_font("notfoundfont", 20)
        self.assertIsNotNone(font)

# === Tests utils.py (logique métier) ===
class TestGameLogic(unittest.TestCase):
    def test_calcule_score(self):
        self.assertEqual(calcule_score(5), 6)
        self.assertEqual(calcule_score(0, 2), 2)

    def test_consomme_munition(self):
        self.assertEqual(consomme_munition(5), 4)
        self.assertEqual(consomme_munition(1), 0)
        self.assertEqual(consomme_munition(0), 0)

    def test_verifie_victoire(self):
        self.assertTrue(verifie_victoire(5, 5))
        self.assertTrue(verifie_victoire(6, 5))
        self.assertFalse(verifie_victoire(4, 5))

    def test_verifie_defaite(self):
        self.assertTrue(verifie_defaite(0, 10))
        self.assertTrue(verifie_defaite(5, 0))
        self.assertTrue(verifie_defaite(0, 0))
        self.assertFalse(verifie_defaite(5, 10))

if __name__ == '__main__':
    unittest.main()

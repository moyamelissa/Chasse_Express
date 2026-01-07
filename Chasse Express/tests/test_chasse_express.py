import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import ui
import resources
import entities
import settings
import unittest

# === Tests pour la fonction get_difficulty_settings ===
class TestGetDifficultySettings(unittest.TestCase):
    def test_facile(self):
        params = settings.DIFFICULTY_SETTINGS.get("Facile")
        self.assertIsInstance(params, dict)
        self.assertEqual(params["magpie_count"], 1)
        self.assertEqual(params["label"], "Facile")

    def test_moyen(self):
        params = settings.DIFFICULTY_SETTINGS.get("Moyen")
        self.assertIsInstance(params, dict)
        self.assertEqual(params["magpie_count"], 2)
        self.assertEqual(params["label"], "Moyen")

    def test_difficile(self):
        params = settings.DIFFICULTY_SETTINGS.get("Difficile")
        self.assertIsInstance(params, dict)
        self.assertEqual(params["magpie_count"], 4)
        self.assertEqual(params["label"], "Difficile")

    def test_invalide(self):
        params = settings.DIFFICULTY_SETTINGS.get("Impossible")
        self.assertIsNone(params)

# === Tests pour la classe Magpie ===
class TestMagpie(unittest.TestCase):
    def test_create_random(self):
        magpie = entities.Magpie.create_random(3, 600, 32)
        self.assertIsInstance(magpie, entities.Magpie)
        self.assertEqual(len(magpie.pos), 2)
        self.assertEqual(len(magpie.vel), 2)

    def test_check_hit(self):
        magpie = entities.Magpie(pos=[100, 100], vel=[0, 0])
        hit = magpie.check_hit(100, 100, 32)
        self.assertTrue(hit)
        self.assertTrue(magpie.flying_away)

    def test_update_and_respawn(self):
        magpie = entities.Magpie(pos=[100, 100], vel=[0, 0], flying_away=True, fly_away_timer=1)
        magpie.update(3, 800, 600, 32)
        self.assertFalse(magpie.flying_away)

    def test_check_hit_outside(self):
        magpie = entities.Magpie(pos=[100, 100], vel=[0, 0])
        hit = magpie.check_hit(200, 200, 32)
        self.assertFalse(hit)
        self.assertFalse(magpie.flying_away)

    def test_update_bounce(self):
        magpie = entities.Magpie(pos=[10, 10], vel=[-5, -5])
        magpie.update(3, 800, 600, 32)
        self.assertTrue(magpie.vel[0] > 0 or magpie.vel[1] > 0)

    def test_respawn_random(self):
        magpie = entities.Magpie()
        magpie._respawn(3, 800, 600)
        self.assertTrue(100 <= magpie.pos[0] <= 700)
        self.assertTrue(200 <= magpie.pos[1] <= 400)

    def test_update_no_bounce(self):
        magpie = entities.Magpie(pos=[400, 300], vel=[1, 1])
        magpie.update(3, 800, 600, 32)
        self.assertFalse(magpie.flying_away)


    def test_update_flying_away(self):
        # Vérifie update avec flying_away True et fly_away_timer > 1
        magpie = entities.Magpie(pos=[100, 100], vel=[0, 0], flying_away=True, fly_away_timer=5)
        magpie.update(3, 800, 600, 32)
        self.assertTrue(magpie.flying_away)
        self.assertEqual(magpie.fly_away_timer, 4)

    def test_check_hit_already_flying(self):
        # Vérifie check_hit quand la pie est déjà flying_away
        magpie = entities.Magpie(pos=[100, 100], vel=[0, 0], flying_away=True)
        hit = magpie.check_hit(100, 100, 32)
        self.assertFalse(hit)

# === Tests pour la classe Dog ===
class TestDog(unittest.TestCase):
    def test_start_jump_and_update(self):
        dog = entities.Dog(x=0, y=100)
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
        dog = entities.Dog(x=0, y=100)
        dog.start_jump()
        y1 = dog.get_jump_y()
        dog.update_jump()
        y2 = dog.get_jump_y()
        self.assertNotEqual(y1, y2)

    def test_is_clicked(self):
        dog = entities.Dog(x=10, y=20)
        self.assertTrue(dog.is_clicked(50, 50, 200, 170))
        self.assertFalse(dog.is_clicked(500, 500, 200, 170))

    def test_jump_not_started(self):
        dog = entities.Dog(x=0, y=100)
        self.assertEqual(dog.get_jump_y(), 100)

    def test_is_clicked_outside(self):
        dog = entities.Dog(x=10, y=20)
        self.assertFalse(dog.is_clicked(0, 0, 200, 170))

    def test_update_jump_not_jumping(self):
        dog = entities.Dog(x=0, y=100)
        self.assertFalse(dog.update_jump())

    def test_get_jump_y_not_jumping(self):
        dog = entities.Dog(x=0, y=100)
        self.assertEqual(dog.get_jump_y(), 100)

# === Tests pour les fonctions utilitaires ===
class TestUtilityFunctions(unittest.TestCase):
    def test_load_icon_fallback(self):
        icon = resources.load_icon("notfoundicon.png")
        self.assertIsNotNone(icon)

    def test_load_font_fallback(self):
        font = resources.load_font(["notfoundfont"], 20)
        self.assertIsNotNone(font)

    def test_draw_icon_text(self):
        import pygame
        pygame.init()
        surf = pygame.Surface((100, 40))
        font = resources.load_font(["Arial"], 20)
        ui.dessiner_icone_texte(surf, None, "Test", font, (0,0), 24)

    def test_draw_text_with_outline(self):
        import pygame
        pygame.init()
        surf = pygame.Surface((100, 40))
        font = resources.load_font(["Arial"], 20)
        ui.dessiner_texte_avec_contour(surf, "Test", font, (0,0), (255,255,255))

    def test_get_panel_surface(self):
        surf, shadow = ui.obtenir_surface_panneau(100, 40)
        self.assertIsNotNone(surf)
        self.assertIsNotNone(shadow)

    def test_draw_status_panel(self):
        import pygame
        pygame.init()
        surf = pygame.Surface((400, 80))
        font = resources.load_font(["Arial"], 20)
        stat_font = resources.load_font(["Arial"], 20)
        ui.dessiner_panneau_etat(
            surf, 0, 0, "Test", 1, 2, 3, 4,
            None, None, None,
            stat_font, font, ui.obtenir_surface_panneau
        )

    def test_draw_landfill_background(self):
        import pygame
        pygame.init()
        surf = pygame.Surface((100, 40))
        ui.dessiner_fond(surf, None)

if __name__ == '__main__':
    unittest.main()



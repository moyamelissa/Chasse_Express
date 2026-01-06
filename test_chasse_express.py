import unittest
import chasse_express

# === Tests pour la fonction get_difficulty_settings ===
class TestGetDifficultySettings(unittest.TestCase):
    def test_facile(self):
        # Vérifie les paramètres retournés pour "Facile"
        params = chasse_express.get_difficulty_settings("Facile")
        self.assertIsInstance(params, dict)
        self.assertEqual(params["magpie_count"], 1)
        self.assertEqual(params["label"], "Facile")

    def test_moyen(self):
        # Vérifie les paramètres retournés pour "Moyen"
        params = chasse_express.get_difficulty_settings("Moyen")
        self.assertIsInstance(params, dict)
        self.assertEqual(params["magpie_count"], 2)
        self.assertEqual(params["label"], "Moyen")

    def test_difficile(self):
        # Vérifie les paramètres retournés pour "Difficile"
        params = chasse_express.get_difficulty_settings("Difficile")
        self.assertIsInstance(params, dict)
        self.assertEqual(params["magpie_count"], 4)
        self.assertEqual(params["label"], "Difficile")

    def test_invalide(self):
        # Vérifie qu'une difficulté inconnue retourne None
        params = chasse_express.get_difficulty_settings("Impossible")
        self.assertIsNone(params)

# === Tests pour la classe Magpie ===
class TestMagpie(unittest.TestCase):
    def test_create_random(self):
        # Vérifie la création aléatoire d'une pie
        magpie = chasse_express.Magpie.create_random(3, 600, 32)
        self.assertIsInstance(magpie, chasse_express.Magpie)
        self.assertEqual(len(magpie.pos), 2)
        self.assertEqual(len(magpie.vel), 2)

    def test_check_hit(self):
        # Vérifie que check_hit détecte un clic sur la pie
        magpie = chasse_express.Magpie(pos=[100, 100], vel=[0, 0])
        hit = magpie.check_hit(100, 100, 32)
        self.assertTrue(hit)
        self.assertTrue(magpie.flying_away)

    def test_update_and_respawn(self):
        # Vérifie le respawn après avoir été touchée
        magpie = chasse_express.Magpie(pos=[100, 100], vel=[0, 0], flying_away=True, fly_away_timer=1)
        magpie.update(3, 800, 600, 32)
        self.assertFalse(magpie.flying_away)

    def test_check_hit_outside(self):
        # Vérifie que check_hit retourne False hors de la pie
        magpie = chasse_express.Magpie(pos=[100, 100], vel=[0, 0])
        hit = magpie.check_hit(200, 200, 32)
        self.assertFalse(hit)
        self.assertFalse(magpie.flying_away)

    def test_update_bounce(self):
        # Vérifie le rebond sur les bords
        magpie = chasse_express.Magpie(pos=[10, 10], vel=[-5, -5])
        magpie.update(3, 800, 600, 32)
        self.assertTrue(magpie.vel[0] > 0 or magpie.vel[1] > 0)

    def test_respawn_random(self):
        # Vérifie que _respawn place la pie dans les bornes
        magpie = chasse_express.Magpie()
        magpie._respawn(3, 800, 600)
        self.assertTrue(100 <= magpie.pos[0] <= 700)
        self.assertTrue(200 <= magpie.pos[1] <= 400)

    def test_update_no_bounce(self):
        # Vérifie update sans rebond ni fly_away
        magpie = chasse_express.Magpie(pos=[400, 300], vel=[1, 1])
        magpie.update(3, 800, 600, 32)
        self.assertFalse(magpie.flying_away)

    def test_update_flying_away(self):
        # Vérifie update avec flying_away True et fly_away_timer > 1
        magpie = chasse_express.Magpie(pos=[100, 100], vel=[0, 0], flying_away=True, fly_away_timer=5)
        magpie.update(3, 800, 600, 32)
        self.assertTrue(magpie.flying_away)
        self.assertEqual(magpie.fly_away_timer, 4)

    def test_check_hit_already_flying(self):
        # Vérifie check_hit quand la pie est déjà flying_away
        magpie = chasse_express.Magpie(pos=[100, 100], vel=[0, 0], flying_away=True)
        hit = magpie.check_hit(100, 100, 32)
        self.assertFalse(hit)

# === Tests pour la classe Dog ===
class TestDog(unittest.TestCase):
    def test_start_jump_and_update(self):
        # Vérifie que le saut démarre et se termine correctement
        dog = chasse_express.Dog(x=0, y=100)
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
        dog = chasse_express.Dog(x=0, y=100)
        dog.start_jump()
        y1 = dog.get_jump_y()
        dog.update_jump()
        y2 = dog.get_jump_y()
        self.assertNotEqual(y1, y2)

    def test_is_clicked(self):
        # Vérifie la détection de clic sur le chien
        dog = chasse_express.Dog(x=10, y=20)
        self.assertTrue(dog.is_clicked(50, 50, 200, 170))
        self.assertFalse(dog.is_clicked(500, 500, 200, 170))

    def test_jump_not_started(self):
        # Vérifie get_jump_y si le saut n'a pas commencé
        dog = chasse_express.Dog(x=0, y=100)
        self.assertEqual(dog.get_jump_y(), 100)

    def test_is_clicked_outside(self):
        # Vérifie is_clicked hors de l'image
        dog = chasse_express.Dog(x=10, y=20)
        self.assertFalse(dog.is_clicked(0, 0, 200, 170))

    def test_update_jump_not_jumping(self):
        # Vérifie update_jump quand le chien ne saute pas
        dog = chasse_express.Dog(x=0, y=100)
        self.assertFalse(dog.update_jump())

    def test_get_jump_y_not_jumping(self):
        # Vérifie get_jump_y quand le chien ne saute pas
        dog = chasse_express.Dog(x=0, y=100)
        self.assertEqual(dog.get_jump_y(), 100)

# === Tests pour les fonctions utilitaires ===
class TestUtilityFunctions(unittest.TestCase):
    def test_get_best_font(self):
        # Vérifie que get_best_font retourne une police
        font = chasse_express.get_best_font(20)
        self.assertIsNotNone(font)

    def test_get_panel_font(self):
        # Vérifie que get_panel_font retourne une police
        font = chasse_express.get_panel_font(20)
        self.assertIsNotNone(font)

    def test_load_icon_fallback(self):
        # Vérifie le fallback si l'icône n'existe pas
        icon = chasse_express.load_icon("notfoundicon.png")
        self.assertIsNotNone(icon)

    def test_load_font_fallback(self):
        # Vérifie le fallback si la police n'existe pas
        font = chasse_express.load_font("notfoundfont", 20)
        self.assertIsNotNone(font)

    def test_draw_icon_text(self):
        # Vérifie que draw_icon_text ne plante pas (surface factice)
        import pygame
        pygame.init()
        surf = pygame.Surface((100, 40))
        font = chasse_express.get_best_font(20)
        chasse_express.draw_icon_text(surf, None, "Test", font, (0,0), 24)

    def test_draw_text_with_outline(self):
        # Vérifie que draw_text_with_outline ne plante pas (surface factice)
        import pygame
        pygame.init()
        surf = pygame.Surface((100, 40))
        font = chasse_express.get_best_font(20)
        chasse_express.draw_text_with_outline(surf, "Test", font, (0,0), (255,255,255))

    def test_get_panel_surface(self):
        # Vérifie que get_panel_surface retourne deux surfaces
        surf, shadow = chasse_express.get_panel_surface(100, 40)
        self.assertIsNotNone(surf)
        self.assertIsNotNone(shadow)

    def test_draw_status_panel(self):
        # Vérifie que draw_status_panel ne plante pas (surface factice)
        import pygame
        pygame.init()
        surf = pygame.Surface((400, 80))
        font = chasse_express.get_best_font(20)
        stat_font = chasse_express.get_panel_font(20)
        chasse_express.draw_status_panel(
            surf, 0, 0, "Test", 1, 2, 3, 4,
            None, None, None,
            stat_font, font, chasse_express.get_panel_surface
        )

    def test_draw_landfill_background(self):
        # Vérifie que draw_landfill_background ne plante pas (surface factice)
        import pygame
        pygame.init()
        surf = pygame.Surface((100, 40))
        chasse_express.draw_landfill_background(surf, None)

if __name__ == '__main__':
    unittest.main()



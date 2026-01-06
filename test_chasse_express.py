import unittest
import time
import chasse_express

class TestAddition(unittest.TestCase):
    """Tests pour la fonction addition."""

    def test_addition(self):
        # Vérifie que l'addition de deux entiers retourne le bon résultat (2 + 3 = 5)
        result = chasse_express.addition(2, 3)
        self.assertEqual(result, 5)

    def test_addition_float(self):
        # Vérifie que l'addition de deux flottants retourne le bon résultat (2.5 + 3.5 = 6.0)
        result = chasse_express.addition(2.5, 3.5)
        self.assertEqual(result, 6.0)

    def test_addition_negative(self):
        # Vérifie que l'addition de deux nombres négatifs retourne le bon résultat (-2 + -3 = -5)
        result = chasse_express.addition(-2, -3)
        self.assertEqual(result, -5)

    def test_addition_zero(self):
        # Vérifie que l'addition avec zéro retourne le bon résultat (0 + 5 = 5)
        result = chasse_express.addition(0, 5)
        self.assertEqual(result, 5)

    def test_addition_type_error(self):
        # Vérifie que la fonction lève une exception TypeError si un argument n'est pas un nombre
        with self.assertRaises(TypeError):
            chasse_express.addition(2, "a")
        with self.assertRaises(TypeError):
            chasse_express.addition("b", 3)
        with self.assertRaises(TypeError):
            chasse_express.addition(None, 3)

class TestPerformanceAddition(unittest.TestCase):
    """Test de performance pour la fonction addition."""

    def test_addition_performance(self):
        # Vérifie que l'addition est rapide même pour 100 000 appels successifs
        start = time.time()
        for _ in range(100000):
            chasse_express.addition(1, 2)
        duration = time.time() - start
        self.assertLess(duration, 1, "Addition trop lente")

class TestGetDifficultySettings(unittest.TestCase):
    """Tests pour la fonction get_difficulty_settings."""

    def test_facile(self):
        # Vérifie que les paramètres retournés pour "Facile" sont corrects
        params = chasse_express.get_difficulty_settings("Facile")
        self.assertIsInstance(params, dict)
        self.assertEqual(params["magpie_count"], 1)
        self.assertEqual(params["label"], "Facile")

    def test_moyen(self):
        # Vérifie que les paramètres retournés pour "Moyen" sont corrects
        params = chasse_express.get_difficulty_settings("Moyen")
        self.assertIsInstance(params, dict)
        self.assertEqual(params["magpie_count"], 2)
        self.assertEqual(params["label"], "Moyen")

    def test_difficile(self):
        # Vérifie que les paramètres retournés pour "Difficile" sont corrects
        params = chasse_express.get_difficulty_settings("Difficile")
        self.assertIsInstance(params, dict)
        self.assertEqual(params["magpie_count"], 4)
        self.assertEqual(params["label"], "Difficile")

    def test_invalide(self):
        # Vérifie qu'une difficulté inconnue retourne None
        params = chasse_express.get_difficulty_settings("Impossible")
        self.assertIsNone(params)

class TestMagpie(unittest.TestCase):
    """Tests pour la classe Magpie."""

    def test_create_random(self):
        # Vérifie que la création aléatoire d'une pie retourne bien un objet Magpie
        magpie = chasse_express.Magpie.create_random(3, 600, 32)
        self.assertIsInstance(magpie, chasse_express.Magpie)
        self.assertEqual(len(magpie.pos), 2)
        self.assertEqual(len(magpie.vel), 2)

    def test_check_hit(self):
        # Vérifie que check_hit détecte un clic sur la pie et modifie son état
        magpie = chasse_express.Magpie(pos=[100, 100], vel=[0, 0])
        hit = magpie.check_hit(100, 100, 32)
        self.assertTrue(hit)
        self.assertTrue(magpie.flying_away)

    def test_update_and_respawn(self):
        # Vérifie que la pie respawn correctement après avoir été touchée
        magpie = chasse_express.Magpie(pos=[100, 100], vel=[0, 0], flying_away=True, fly_away_timer=1)
        magpie.update(3, 800, 600, 32)
        self.assertFalse(magpie.flying_away)  # Doit respawn et ne plus être flying_away

class TestDog(unittest.TestCase):
    """Tests pour la classe Dog."""

    def test_start_jump_and_update(self):
        # Vérifie que le saut démarre et se termine correctement
        dog = chasse_express.Dog(x=0, y=100)
        dog.start_jump()
        self.assertTrue(dog.jumping)
        finished = False
        # Simule le saut complet
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
        # Vérifie que le chien détecte correctement un clic à l'intérieur ou à l'extérieur de son image
        dog = chasse_express.Dog(x=10, y=20)
        # Suppose une image de 200x170
        self.assertTrue(dog.is_clicked(50, 50, 200, 170))
        self.assertFalse(dog.is_clicked(500, 500, 200, 170))

if __name__ == '__main__':
    unittest.main()

# Comment exécuter les tests

Ce dossier contient les tests unitaires automatisés pour le jeu Chasse Express.

## Exécution des tests

1. Ouvrez un terminal dans le dossier `Chasse Express/Chasse Express`.
2. Activez votre environnement virtuel si besoin :
   ```
   .venv\Scripts\activate
   ```
3. Lancez tous les tests avec :
   ```
   python -m unittest discover tests
   ```
   ou, si vous utilisez pytest :
   ```
   pytest
   ```

## Ce que font les tests

- Les tests vérifient la logique principale du jeu, notamment :
  - Les paramètres de difficulté
  - Les comportements des classes Magpie et Dog
  - Les fonctions utilitaires (polices, icônes, dessin)
- Chaque test s'assure que les fonctions et classes fonctionnent comme prévu et que les cas limites sont bien gérés.

## Ce que signifient les résultats

- **Tous les tests passent :** Votre code fonctionne comme attendu.
- **Certains tests échouent :** Il y a un bug ou un comportement inattendu dans votre code. Lisez le message d'erreur pour savoir quel test a échoué et pourquoi.
- **Couverture :** Vous pouvez utiliser `coverage` pour mesurer la part de code testée :
  ```
  coverage run -m unittest discover tests
  coverage report
  ```

## Bonnes pratiques

- Exécutez les tests après chaque modification du code.
- Ajoutez de nouveaux tests lors de l'ajout de fonctionnalités ou de la correction de bugs.
- Les tests garantissent la stabilité et la maintenabilité du jeu.


# Comment exécuter les tests

Ce dossier contient les tests unitaires automatisés pour le jeu Chasse Express.

## Exécution des tests

1. Ouvrez un terminal dans le dossier `Chasse Express/Chasse Express`.
2. Activez votre environnement virtuel si besoin :
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```
3. Lancez tous les tests avec :
   ```bash
   python -m unittest discover tests
   ```
   ou, si vous utilisez pytest :
   ```bash
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
- **Couverture :** Vous pouvez utiliser `coverage` pour mesurer la part de code testée (voir section ci-dessous).

## Bonnes pratiques

- Exécutez les tests après chaque modification du code.
- Ajoutez de nouveaux tests lors de l'ajout de fonctionnalités ou de la correction de bugs.
- Les tests garantissent la stabilité et la maintenabilité du jeu.

---

## Comment générer un rapport de couverture des tests

Pour mesurer la couverture de vos tests unitaires avec le module `coverage`, suivez ces étapes :

### 1. Installez coverage (si ce n'est pas déjà fait)
```bash
python -m pip install coverage
```

### 2. Lancez les tests avec coverage
```bash
python -m coverage run -m unittest discover tests
```
(Remplacez `unittest` par `pytest` si vous utilisez pytest.)

### 3. Affichez le rapport de couverture

**Dans le terminal :**
```bash
python -m coverage report
```

**En HTML (plus lisible) :**
```bash
python -m coverage html
```
Puis ouvrez le fichier `htmlcov/index.html` dans votre navigateur. 

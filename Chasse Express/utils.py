# ==========================================
# Fonctions utilitaires pour Chasse Express
# ==========================================

from resources import load_font, load_icon

# ========================================
# Fonctions utilitaires mathématiques
# ========================================

def clamp(valeur, minimum, maximum):
    """
    Contraint une valeur entre un minimum et un maximum.
    """
    return max(minimum, min(valeur, maximum))

# ===============================================
# Fonctions de gestion du score et des munitions
# ===============================================

def calcule_score(score, increment=1):
    """Retourne le score après avoir touché une pie."""
    return score + increment

def consomme_munition(ammo, amount=1):
    """Retourne le nombre de munitions après un tir."""
    return max(0, ammo - amount)

# ==============================================
# Fonctions de vérification de victoire/défaite
# ==============================================

def verifie_victoire(score, goal):
    """Retourne True si le score atteint l'objectif."""
    return score >= goal

def verifie_defaite(ammo, time_left):
    """Retourne True si le joueur n'a plus de munitions ou de temps."""
    return ammo <= 0 or time_left <= 0

# ================================================
# Fonctions de gestion du temps et de progression
# ================================================

def temps_ecoule(timer_start):
    """Retourne le temps écoulé en secondes depuis le début du round."""
    import pygame
    if timer_start is None:
        return 0
    return (pygame.time.get_ticks() - timer_start) // 1000

def pourcentage_objectif(score, goal):
    """Retourne le pourcentage d'objectif atteint (entre 0 et 100)."""
    if goal == 0:
        return 100
    return min(100, int((score / goal) * 100))

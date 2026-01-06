# =========================
# Fonctions d'affichage et d'interface graphique pour Chasse Express
# =========================
import pygame
from typing import Optional
from settings import OUTLINE_W, MAGPIE_BLACK, MAGPIE_WHITE, MAGPIE_BLUE, MAGPIE_BEAK

def dessiner_texte_avec_contour(
    surface: "pygame.Surface",
    texte: str,
    police: "pygame.font.Font",
    position: tuple,
    couleur_principale: tuple,
    couleur_contour: tuple = (255,255,255),
    couleur_ombre: tuple = (0,0,0),
    decalage_contour: int = 2,
    decalage_ombre: int = 4
) -> None:
    """
    Dessine un texte avec contour et ombre sur la surface.
    """
    x, y = position
    ombre = police.render(texte, True, couleur_ombre)
    surface.blit(ombre, (x+decalage_ombre, y+decalage_ombre))
    for dx in [-decalage_contour, 0, decalage_contour]:
        for dy in [-decalage_contour, 0, decalage_contour]:
            if dx != 0 or dy != 0:
                contour = police.render(texte, True, couleur_contour)
                surface.blit(contour, (x+dx, y+dy))
    principal = police.render(texte, True, couleur_principale)
    surface.blit(principal, (x, y))

def dessiner_icone_texte(
    surface: "pygame.Surface",
    icone: Optional["pygame.Surface"],
    texte: str,
    police: "pygame.font.Font",
    position: tuple,
    taille_icone: int,
    espace: int = 10
) -> None:
    """
    Dessine une icône suivie d'un texte sur la surface.
    """
    x, y = position
    if icone:
        icone_img = pygame.transform.smoothscale(icone, (taille_icone, taille_icone))
        surface.blit(icone_img, (x, y))
        x += taille_icone + espace
    etiquette = police.render(texte, True, (30,30,30))
    surface.blit(etiquette, (x, y + (taille_icone - etiquette.get_height()) // 2))

def obtenir_surface_panneau(largeur: int, hauteur: int, rayon_bord: int = 24) -> tuple:
    """
    Crée une surface de panneau avec ombre et bord arrondi.
    """
    panneau = pygame.Surface((largeur, hauteur), pygame.SRCALPHA)
    ombre = pygame.Surface((largeur, hauteur), pygame.SRCALPHA)
    pygame.draw.rect(ombre, (0,0,0,40), (0,0,largeur,hauteur), border_radius=rayon_bord)
    pygame.draw.rect(panneau, (245, 248, 255, 230), (0,0,largeur,hauteur), border_radius=rayon_bord)
    pygame.draw.rect(panneau, (200,200,220,180), (0,0,largeur,hauteur), 2, border_radius=rayon_bord)
    return panneau, ombre

def dessiner_panneau_etat(
    surface: "pygame.Surface",
    x: int, y: int, niveau: str, score: int, objectif: int, munitions: int, temps_restant: int,
    icone_oiseau: Optional["pygame.Surface"], icone_munition: Optional["pygame.Surface"], icone_timer: Optional["pygame.Surface"],
    police_stat: "pygame.font.Font", police_niveau: "pygame.font.Font", obtenir_surface_panneau_func,
    marge_x: int = 24, marge_y: int = 14, espace_section: int = 32, espace_icone_texte: int = 10
) -> None:
    """
    Dessine le panneau d'état du jeu (score, niveau, munitions, temps).
    """
    taille_icone = police_stat.get_height()
    hauteur_panneau = taille_icone + 2 * marge_y
    groupes = []
    texte_niveau = police_niveau.render(f"Niveau : {niveau}", True, (0,0,0))
    groupes.append({'icone': None, 'texte_surf': texte_niveau})
    texte_oiseau = police_stat.render(f"{score}/{objectif}", True, (30,30,30))
    icone_oiseau = pygame.transform.smoothscale(icone_oiseau, (taille_icone, taille_icone)) if icone_oiseau else None
    groupes.append({'icone': icone_oiseau, 'texte_surf': texte_oiseau})
    texte_munition = police_stat.render(f"{munitions}", True, (30,30,30))
    icone_munition = pygame.transform.smoothscale(icone_munition, (taille_icone, taille_icone)) if icone_munition else None
    groupes.append({'icone': icone_munition, 'texte_surf': texte_munition})
    texte_timer = police_stat.render(f"{temps_restant}s", True, (30,30,30))
    icone_timer = pygame.transform.smoothscale(icone_timer, (taille_icone, taille_icone)) if icone_timer else None
    groupes.append({'icone': icone_timer, 'texte_surf': texte_timer})
    largeurs_groupes = []
    for g in groupes:
        w = 0
        if g['icone']:
            w += taille_icone + espace_icone_texte
        w += g['texte_surf'].get_width()
        largeurs_groupes.append(w)
    largeur_panneau = sum(largeurs_groupes) + espace_section * (len(groupes)-1) + 2 * marge_x
    panneau, ombre = obtenir_surface_panneau_func(largeur_panneau, hauteur_panneau)
    surface.blit(ombre, (x+2, y+10))
    dessiner_x = marge_x
    centre_y = hauteur_panneau // 2
    for idx, g in enumerate(groupes):
        icone_y = centre_y - taille_icone // 2
        if g['icone']:
            panneau.blit(g['icone'], (dessiner_x, icone_y))
            dessiner_x += taille_icone + espace_icone_texte
        texte_y = centre_y - g['texte_surf'].get_height() // 2
        panneau.blit(g['texte_surf'], (dessiner_x, texte_y))
        dessiner_x += g['texte_surf'].get_width()
        if idx < len(groupes) - 1:
            dessiner_x += espace_section
    surface.blit(panneau, (x, y))

def dessiner_fond(surface: "pygame.Surface", image_fond: Optional["pygame.Surface"] = None) -> None:
    """
    Dessine le fond du jeu (image ou couleur).
    """
    if image_fond:
        surface.blit(image_fond, (0, 0))
    else:
        surface.fill((100, 180, 255))

def dessiner_chien(surface: "pygame.Surface", x: int, y: int, phase_saut: float, image_sheltie: "pygame.Surface") -> None:
    """
    Dessine le chien (sheltie) à la position donnée.
    """
    surface.blit(image_sheltie, (x, y))

def dessiner_pie(surface: "pygame.Surface", pos: tuple) -> None:
    """
    Dessine une pie sur la surface.
    """
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

def dessiner_viseur(surface: "pygame.Surface", pos: tuple) -> None:
    """
    Dessine le viseur (croix rouge) à la position donnée.
    """
    x, y = pos
    viseur = pygame.Surface((44, 44), pygame.SRCALPHA)
    centre = 22
    rouge = (255, 0, 0, 140)
    pygame.draw.circle(viseur, rouge, (centre, centre), 20, 5)
    pygame.draw.line(viseur, rouge, (centre - 22, centre), (centre + 22, centre), 5)
    pygame.draw.line(viseur, rouge, (centre, centre - 22), (centre, centre + 22), 5)
    pygame.draw.circle(viseur, rouge, (centre, centre), 5, 2)
    surface.blit(viseur, (x - centre, y - centre))

def dessiner_bouton(
    surface: "pygame.Surface",
    rect: "pygame.Rect",
    texte: str,
    police: "pygame.font.Font",
    couleur: tuple,
    survol: bool = False
) -> None:
    """
    Dessine un bouton avec texte et effet de survol.
    """
    bouton = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(bouton, (*couleur, 170), (0,0,rect.width,rect.height), border_radius=22)
    pygame.draw.rect(bouton, (200,200,220,120), (0,0,rect.width,rect.height), 3, border_radius=22)
    if survol:
        pygame.draw.rect(bouton, (255,255,255,180), (0,0,rect.width,rect.height), 4, border_radius=22)
    etiquette = police.render(texte, True, (255,255,255))
    bouton.blit(etiquette, ((rect.width-etiquette.get_width())//2, (rect.height-etiquette.get_height())//2))
    surface.blit(bouton, (rect.x, rect.y))

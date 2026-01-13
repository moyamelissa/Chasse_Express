# ========================================
# Module des entités du jeu (Magpie, Dog)
# ========================================

# ----- Imports -----
from dataclasses import dataclass, field
from typing import List, Tuple
import math
import random

# ==============================
# Classe Magpie (entité oiseau)
# ==============================
@dataclass
class Magpie:
    """
    Représente une pie (oiseau) dans le jeu.
    """
    pos: List[float] = field(default_factory=lambda: [0.0, 0.0])
    vel: List[float] = field(default_factory=lambda: [0.0, 0.0])
    flying_away: bool = False
    fly_away_timer: int = 0

    @classmethod
    def create_random(cls, speed: float, screen_height: int, body_radius: int) -> "Magpie":
        """
        Crée une pie avec une position et une vitesse aléatoires.
        """
        start_x = body_radius
        start_y = random.randint(body_radius, screen_height - 150 - body_radius)
        vx = speed * random.uniform(0.9, 1.2)
        vy = random.uniform(-2, 2)
        return cls(pos=[start_x, start_y], vel=[vx, vy])

    def update(self, speed: float, width: int, height: int, body_radius: int) -> None:
        """
        Met à jour la position et l'état de la pie.
        """
        if self.flying_away:
            self.pos[1] -= 12
            self.fly_away_timer -= 1
            if self.pos[1] < -body_radius or self.fly_away_timer <= 0:
                self._respawn(speed, width, height)
        else:
            self._move_and_bounce(speed, width, height, body_radius)

    def _respawn(self, speed: float, width: int, height: int) -> None:
        """
        Replace la pie à une nouvelle position aléatoire.
        """
        self.pos[0] = random.randint(100, width - 100)
        self.pos[1] = random.randint(200, height - 200)
        direction_x = 1 if random.random() < 0.5 else -1
        direction_y = 1 if random.random() < 0.5 else -1
        self.vel[0] = speed * direction_x
        self.vel[1] = speed * direction_y
        self.flying_away = False

    def _move_and_bounce(self, speed: float, width: int, height: int, body_radius: int) -> None:
        """
        Déplace la pie et gère les rebonds sur les bords.
        """
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        bounced = False
        if self.pos[0] < body_radius or self.pos[0] > width - body_radius:
            self.vel[0] *= -1
            bounced = True
        if self.pos[1] < body_radius or self.pos[1] > height - 150 - body_radius:
            self.vel[1] *= -1
            bounced = True
        if bounced and self.vel[0] == 0:
            self.vel[0] = speed * (1 if random.random() < 0.5 else -1)
        if bounced and self.vel[1] == 0:
            self.vel[1] = speed * (1 if random.random() < 0.5 else -1)

    def check_hit(self, mx: int, my: int, body_radius: int) -> bool:
        """
        Vérifie si la pie a été touchée par un clic.
        """
        if not self.flying_away:
            dx = mx - self.pos[0]
            dy = my - self.pos[1]
            if dx * dx + dy * dy <= body_radius * body_radius:
                self.flying_away = True
                self.fly_away_timer = 30
                return True
        return False

    def get_position(self) -> Tuple[int, int]:
        """
        Retourne la position entière de la pie.
        """
        return (int(self.pos[0]), int(self.pos[1]))

# ===========================
# Classe Dog (entité chien)
# ===========================
@dataclass
class Dog:
    """
    Représente le chien dans le jeu.
    """
    x: int
    y: int
    jump_phase: float = 0.0
    jumping: bool = False
    jump_total: float = field(default_factory=lambda: math.pi)
    jump_started: bool = False

    def start_jump(self) -> None:
        """
        Démarre le saut du chien.
        """
        self.jump_started = True
        self.jumping = True
        self.jump_phase = 0.0

    def update_jump(self) -> bool:
        """
        Met à jour le saut du chien.
        """
        if self.jumping:
            self.jump_phase += 0.07
            if self.jump_phase >= self.jump_total:
                self.jumping = False
                return True
        return False

    def get_jump_y(self) -> int:
        """
        Retourne la position Y du chien pendant le saut.
        """
        if self.jumping:
            return self.y - int(30 * abs(math.sin(self.jump_phase)))
        return self.y

    def is_clicked(self, mx: int, my: int, img_width: int, img_height: int) -> bool:
        """
        Vérifie si le chien a été cliqué.
        """
        return (self.x <= mx <= self.x + img_width and 
                self.y <= my <= self.y + img_height)

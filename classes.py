# -*- coding: utf-8 -*-

import pygame
from config import BRICK_PROPERTIES, POWER_UP_PROPERTIES, hud_font
from drawing_utils import draw_text

class Brick:
    def __init__(self, x, y, brick_type):
        self.rect = pygame.Rect(x, y, 50, 20)
        self.type = brick_type
        properties = BRICK_PROPERTIES.get(brick_type, BRICK_PROPERTIES['G'])
        self.hp = properties["hp"]
        self.max_hp = properties["hp"]
        self.base_color = properties["color"]
        self.score_value = properties["score"]
        self.power_up_type = properties["power_up"]
        self.is_invisible = properties.get("is_invisible", False)
        self.was_hit = False

    def hit(self):
        if self.is_invisible and not self.was_hit:
            self.was_hit = True
            return False
        if self.hp < float('inf'):
            self.hp -= 1
        return self.hp <= 0

    def draw(self, surface):
        if self.hp > 0 and not (self.is_invisible and not self.was_hit):
            color_multiplier = 1
            if self.max_hp > 1 and self.hp < float('inf'):
                color_multiplier = 0.4 + 0.6 * (self.hp / self.max_hp)
            color = tuple(int(c * color_multiplier) for c in self.base_color)
            pygame.draw.rect(surface, color, self.rect, border_radius=4)
            if self.type == 'I':
                pygame.draw.rect(surface, (200, 200, 200), self.rect, 2, border_radius=4)

class PowerUp:
    def __init__(self, center_x, center_y, power_up_type):
        self.type = power_up_type
        self.rect = pygame.Rect(center_x - 10, center_y, 20, 20)
        self.color = POWER_UP_PROPERTIES[self.type]["color"]
        self.speed = 3

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=5)
        icon = POWER_UP_PROPERTIES[self.type]["icon"]
        draw_text(icon[0], hud_font, (0,0,0), self.rect.centerx, self.rect.centery)

class Ball:
    def __init__(self, x, y, speed_x, speed_y):
        self.rect = pygame.Rect(x, y, 12, 12)
        self.speed = [speed_x, speed_y]
        self.true_pos = [float(x), float(y)]

    def update(self, speed_multiplier):
        self.true_pos[0] += self.speed[0] * speed_multiplier
        self.true_pos[1] += self.speed[1] * speed_multiplier
        self.rect.center = (round(self.true_pos[0]), round(self.true_pos[1]))

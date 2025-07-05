# -*- coding: utf-8 -*-

import pygame

# --- Constants ---
WIDTH, HEIGHT = 600, 600
TOP_PANEL_HEIGHT = 50
GAME_AREA_Y_START = TOP_PANEL_HEIGHT
SCORE_FILE = "breakout_scores.json"

# --- Color Theme ---
BG_COLOR = (10, 10, 42)
HUD_BG_COLOR = (26, 26, 58)
TEXT_COLOR = (224, 224, 224)
HIGHLIGHT_COLOR = (97, 255, 216)
PADDLE_COLOR = (0, 191, 255)
BALL_COLOR = (255, 0, 255)
RED = (255, 85, 85)

# --- Fonts ---
pygame.font.init()
title_font = pygame.font.SysFont("Consolas", 50, bold=True)
menu_font = pygame.font.SysFont("Consolas", 28, bold=True)
hud_font = pygame.font.SysFont("Arial", 20)
info_font = pygame.font.SysFont("Arial", 20)
message_font = pygame.font.SysFont("Arial", 22, italic=True)

# --- Brick & Power-up Config ---
BRICK_PROPERTIES = {
    'G': {"name": "Classic", "hp": 1, "color": (0, 200, 100), "score": 10, "power_up": None},
    'K': {"name": "Tough", "hp": 3, "color": (60, 60, 60), "score": 50, "power_up": None},
    'R': {"name": "Speed Up", "hp": 1, "color": (255, 0, 0), "score": 25, "power_up": 'speed_up'},
    'P': {"name": "Multi-ball", "hp": 1, "color": (128, 0, 128), "score": 25, "power_up": 'multi_ball'},
    'W': {"name": "Slow Down", "hp": 1, "color": (255, 255, 255), "score": 25, "power_up": 'slow_down'},
    'Y': {"name": "Shrink", "hp": 1, "color": (128, 128, 128), "score": 25, "power_up": 'shrink_paddle'},
    'B': {"name": "Bonus", "hp": 1, "color": (255, 255, 0), "score": 25, "power_up": 'bonus'},
    'L': {"name": "Grow", "hp": 1, "color": (0, 191, 255), "score": 25, "power_up": 'grow_paddle'},
    'O': {"name": "Reverse", "hp": 1, "color": (255, 165, 0), "score": 25, "power_up": 'reverse_controls'},
    'N': {"name": "Invisible", "hp": 1, "color": (139, 69, 19), "score": 100, "power_up": None, "is_invisible": True},
    'I': {"name": "Indestructible", "hp": float('inf'), "color": (100, 100, 100), "score": 0, "power_up": None},
}

POWER_UP_PROPERTIES = {
    'speed_up': {"color": (255, 0, 0), "duration": 5, "icon": "SPD+"},
    'multi_ball': {"color": (128, 0, 128), "duration": 10, "icon": "x3"},
    'slow_down': {"color": (255, 255, 255), "duration": 5, "icon": "SPD-"},
    'shrink_paddle': {"color": (128, 128, 128), "duration": 10, "icon": "SHR"},
    'bonus': {"color": (255, 255, 0), "duration": 0, "icon": "?"},
    'grow_paddle': {"color": (0, 191, 255), "duration": 10, "icon": "GRW"},
    'reverse_controls': {"color": (255, 165, 0), "duration": 5, "icon": "REV"},
}

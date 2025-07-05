# -*- coding: utf-8 -*-

import pygame

def draw_text(text, font, color, x, y, center=True, surface=None):
    if surface is None:
        surface = pygame.display.get_surface()
    txt_surface = font.render(text, True, color)
    rect = txt_surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(txt_surface, rect)

def draw_multiline_text(text, font, color, x, y, max_width, surface=None):
    if surface is None:
        surface = pygame.display.get_surface()
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] < max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    total_height = len(lines) * font.get_height()
    start_y = y - total_height // 2
    for i, line in enumerate(lines):
        draw_text(line.strip(), font, color, x, start_y + i * font.get_height(), center=True, surface=surface)

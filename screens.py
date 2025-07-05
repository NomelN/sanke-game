# -*- coding: utf-8 -*-

import pygame
from config import *
from drawing_utils import draw_text, draw_multiline_text
from utils import load_scores

def main_menu(win, start_game_func):
    selected_option = 0
    menu_options = ["Start Game", "High Scores", "Quit"]
    if pygame.mixer.get_init():
        try:
            pygame.mixer.music.load('média/8bit-music-for-game-68698.mp3')
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Error playing menu music: {e}")

    while True:
        win.fill(BG_COLOR)
        draw_text("BREAKOUT EVOLVED", title_font, HIGHLIGHT_COLOR, WIDTH // 2, 120, surface=win)
        for i, option in enumerate(menu_options):
            color = HIGHLIGHT_COLOR if i == selected_option else TEXT_COLOR
            text = f"> {option} <" if i == selected_option else option
            draw_text(text, menu_font, color, WIDTH // 2, 250 + i * 60, surface=win)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN: selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        player_name = name_input_screen(win)
                        if player_name:
                            start_game_func(player_name)
                            if pygame.mixer.get_init() and not pygame.mixer.music.get_busy():
                                try:
                                    pygame.mixer.music.load('média/8bit-music-for-game-68698.mp3')
                                    pygame.mixer.music.play(-1)
                                except pygame.error as e:
                                    print(f"Error playing menu music: {e}")
                    elif selected_option == 1: show_history(win)
                    elif selected_option == 2: pygame.quit(); exit()

def name_input_screen(win):
    current_player = ""
    cursor_visible = True
    cursor_timer = 0
    clock = pygame.time.Clock()
    while True:
        win.fill(BG_COLOR)
        draw_text("ENTER YOUR NAME", title_font, HIGHLIGHT_COLOR, WIDTH // 2, 150, surface=win)
        cursor_timer += clock.get_rawtime()
        if cursor_timer > 500:
            cursor_timer = 0
            cursor_visible = not cursor_visible
        display_text = current_player + ("_" if cursor_visible else "")
        draw_text(display_text, menu_font, TEXT_COLOR, WIDTH // 2, 250, surface=win)
        draw_text("Max 10 chars. Enter to start.", info_font, TEXT_COLOR, WIDTH // 2, 320, surface=win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and current_player: return current_player
                elif event.key == pygame.K_BACKSPACE: current_player = current_player[:-1]
                elif len(current_player) < 10 and event.unicode.isalnum():
                    current_player += event.unicode.upper()
        clock.tick(60)

def show_history(win):
    win.fill(BG_COLOR)
    draw_text("HIGH SCORES", title_font, HIGHLIGHT_COLOR, WIDTH // 2, 80, surface=win)
    scores = load_scores()
    if not scores:
        draw_text("No scores yet!", info_font, TEXT_COLOR, WIDTH // 2, HEIGHT // 2, surface=win)
    else:
        for i, entry in enumerate(scores):
            name = entry.get('name', 'N/A')
            score = entry.get('score', 0)
            draw_text(f"{i+1: >2}. {name: <10} {score: >6}", menu_font, TEXT_COLOR, WIDTH // 2, 180 + i * 40, surface=win)
    draw_text("Press Enter to return", info_font, RED, WIDTH // 2, HEIGHT - 50, surface=win)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: waiting = False

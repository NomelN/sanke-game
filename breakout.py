import pygame
import random
import os
import json

pygame.init()
pygame.mixer.init()

# --- Constantes ---
WIDTH, HEIGHT = 600, 550
TOP_PANEL_HEIGHT = 50
GAME_AREA_Y_START = TOP_PANEL_HEIGHT
SCORE_FILE = "breakout_scores.json"

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Futura")

# --- Thème de couleurs ---
BG_COLOR = (10, 10, 42)
HUD_BG_COLOR = (26, 26, 58)
TEXT_COLOR = (224, 224, 224)
HIGHLIGHT_COLOR = (97, 255, 216)
PADDLE_COLOR = (0, 191, 255)
BALL_COLOR = (255, 0, 255)
BRICK_COLORS = [(0, 200, 100), (255, 105, 180), (255, 255, 0)]
RED = (255, 85, 85)

# --- Polices ---
title_font = pygame.font.SysFont("Consolas", 50, bold=True)
menu_font = pygame.font.SysFont("Consolas", 28, bold=True)
hud_font = pygame.font.SysFont("Arial", 24)
info_font = pygame.font.SysFont("Arial", 20)

clock = pygame.time.Clock()

# ----------------------
# 🎵 Chargement des sons
# ----------------------
try:
    pygame.mixer.music.load('média/8bit-music-for-game-68698.mp3')
    brick_hit_sound = pygame.mixer.Sound('média/explosion-312361.mp3')
    game_over_sound = pygame.mixer.Sound('média/game-over-38511.mp3')
    pygame.mixer.music.set_volume(0.3)
    brick_hit_sound.set_volume(0.4)
except pygame.error as e:
    print(f"Warning: Un son n'a pas pu être chargé : {e}")
    brick_hit_sound = None
    game_over_sound = None

# ----------------------
# 🎯 Fonctions utilitaires
# ----------------------

def draw_text(text, font, color, x, y, center=True):
    txt_surface = font.render(text, True, color)
    rect = txt_surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    win.blit(txt_surface, rect)

def load_scores():
    if not os.path.exists(SCORE_FILE):
        return []
    try:
        with open(SCORE_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_score(player_name, score):
    scores = load_scores()
    scores.append({"name": player_name, "score": score})
    scores.sort(key=lambda s: s.get('score', 0), reverse=True)
    scores = scores[:10] # Garder les 10 meilleurs
    with open(SCORE_FILE, 'w') as f:
        json.dump(scores, f, indent=4)

def show_history():
    pygame.mixer.music.pause()
    win.fill(BG_COLOR)
    draw_text("MEILLEURS SCORES", title_font, HIGHLIGHT_COLOR, WIDTH // 2, 80)
    
    scores = load_scores()
    if not scores:
        draw_text("Aucun score trouvé.", info_font, TEXT_COLOR, WIDTH // 2, HEIGHT // 2)
    else:
        for i, entry in enumerate(scores):
            name = entry.get('name', 'N/A')
            score = entry.get('score', 0)
            draw_text(f"{i+1: >2}. {name: <10} {score: >6}", menu_font, TEXT_COLOR, WIDTH // 2, 180 + i * 40)

    draw_text("Appuyez sur Entrée pour revenir", info_font, RED, WIDTH // 2, HEIGHT - 50)
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False
    pygame.mixer.music.unpause()

def name_input_screen():
    current_player = ""
    cursor_visible = True
    cursor_timer = 0

    while True:
        win.fill(BG_COLOR)
        draw_text("ENTREZ VOTRE NOM", title_font, HIGHLIGHT_COLOR, WIDTH // 2, 150)

        # Affichage du nom avec curseur clignotant
        cursor_timer += clock.get_rawtime()
        if cursor_timer > 500:
            cursor_timer = 0
            cursor_visible = not cursor_visible
        
        display_text = current_player
        if cursor_visible:
            display_text += "_"
            
        draw_text(display_text, menu_font, TEXT_COLOR, WIDTH // 2, 250)
        draw_text("Max 10 caractères. Entrée pour valider.", info_font, TEXT_COLOR, WIDTH // 2, 320)
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if current_player:
                        return current_player
                elif event.key == pygame.K_BACKSPACE:
                    current_player = current_player[:-1]
                elif len(current_player) < 10:
                    current_player += event.unicode.upper()
        
        clock.tick(60)


def create_bricks(level):
    rows = min(4 + level, 7)
    bricks = []
    for y in range(rows):
        for x in range(9):
            brick_x = x * 65 + 12
            brick_y = y * 30 + GAME_AREA_Y_START + 20
            color = random.choice(BRICK_COLORS)
            bricks.append(pygame.Rect(brick_x, brick_y, 60, 20))
    return bricks

# ----------------------
# 🧱 Jeu principal
# ----------------------

def start_game(player_name):
    if pygame.mixer.get_init():
        pygame.mixer.music.play(-1)

    paddle = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 40, 100, 12)
    ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, 12, 12)
    
    level = 1
    ball_speed_initial = 4
    ball_speed = [random.choice([-ball_speed_initial, ball_speed_initial]), -ball_speed_initial]
    
    bricks = create_bricks(level)
    score = 0
    lives = 3
    running = True
    paused = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                    if paused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

        if not paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and paddle.left > 0:
                paddle.move_ip(-8, 0)
            if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
                paddle.move_ip(8, 0)

            ball.move_ip(*ball_speed)

            # --- Collisions ---
            if ball.left <= 0 or ball.right >= WIDTH:
                ball_speed[0] = -ball_speed[0]
            if ball.top <= GAME_AREA_Y_START:
                ball_speed[1] = -ball_speed[1]
            if ball.colliderect(paddle):
                ball_speed[1] = -abs(ball_speed[1])

            hit_brick = ball.collidelist(bricks)
            if hit_brick != -1:
                bricks.pop(hit_brick)
                ball_speed[1] = -ball_speed[1]
                score += 10
                if brick_hit_sound:
                    brick_hit_sound.play()
            
            # --- Logique de jeu ---
            if not bricks:
                level += 1
                draw_text(f"NIVEAU {level}", title_font, HIGHLIGHT_COLOR, WIDTH // 2, HEIGHT // 2)
                pygame.display.update()
                pygame.time.wait(1500)
                bricks = create_bricks(level)
                ball_speed_val = ball_speed_initial + (level - 1) * 0.5
                ball_speed = [random.choice([-ball_speed_val, ball_speed_val]), -ball_speed_val]
                ball.center = (WIDTH // 2, HEIGHT // 2)

            if ball.bottom > HEIGHT:
                lives -= 1
                if lives > 0:
                    ball.center = (WIDTH // 2, HEIGHT // 2)
                    pygame.time.wait(500)
                else:
                    if pygame.mixer.get_init():
                        pygame.mixer.music.stop()
                        if game_over_sound: game_over_sound.play()
                    
                    save_score(player_name, score)
                    win.fill(BG_COLOR)
                    draw_text("GAME OVER", title_font, RED, WIDTH // 2, HEIGHT // 2 - 50)
                    draw_text(f"Final Score: {score}", menu_font, TEXT_COLOR, WIDTH // 2, HEIGHT // 2 + 20)
                    draw_text("Appuyez sur Entrée", info_font, TEXT_COLOR, WIDTH // 2, HEIGHT // 2 + 80)
                    pygame.display.update()
                    
                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT: pygame.quit(); exit()
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                                waiting = False
                    return

        # --- Affichage ---
        win.fill(BG_COLOR)
        # Panneau HUD
        pygame.draw.rect(win, HUD_BG_COLOR, (0, 0, WIDTH, TOP_PANEL_HEIGHT))
        y_pos = 13 
        draw_text(f"{player_name}", hud_font, HIGHLIGHT_COLOR, 10, y_pos, center=False)
        draw_text(f"Score: {score}", hud_font, TEXT_COLOR, 160, y_pos, center=False)
        draw_text(f"Niveau: {level}", hud_font, TEXT_COLOR, 330, y_pos, center=False)
        draw_text(f"Vies: {lives}", hud_font, TEXT_COLOR, 510, y_pos, center=False)
        
        # Aire de jeu
        pygame.draw.rect(win, PADDLE_COLOR, paddle, border_radius=4)
        pygame.draw.ellipse(win, BALL_COLOR, ball)
        for i, brick in enumerate(bricks):
            pygame.draw.rect(win, BRICK_COLORS[i % len(BRICK_COLORS)], brick, border_radius=4)

        if paused:
            overlay = pygame.Surface((WIDTH, HEIGHT - TOP_PANEL_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            win.blit(overlay, (0, TOP_PANEL_HEIGHT))
            draw_text("PAUSE", title_font, HIGHLIGHT_COLOR, WIDTH // 2, HEIGHT // 2)
            draw_text("Appuyez sur Espace pour reprendre", info_font, TEXT_COLOR, WIDTH // 2, HEIGHT // 2 + 60)

        pygame.display.update()
        clock.tick(60)

# ----------------------
# 📜 Menu principal
# ----------------------

def main_menu():
    selected_option = 0
    menu_options = ["Démarrer", "Scores", "Quitter"]

    if pygame.mixer.get_init() and not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1)

    while True:
        win.fill(BG_COLOR)
        draw_text("BREAKOUT", title_font, HIGHLIGHT_COLOR, WIDTH // 2, 120)

        for i, option in enumerate(menu_options):
            color = HIGHLIGHT_COLOR if i == selected_option else TEXT_COLOR
            text = f"> {option} <" if i == selected_option else option
            draw_text(text, menu_font, color, WIDTH // 2, 250 + i * 60)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0: # Démarrer
                        player_name = name_input_screen()
                        start_game(player_name)
                        if pygame.mixer.get_init(): pygame.mixer.music.play(-1)
                    elif selected_option == 1: # Scores
                        show_history()
                    elif selected_option == 2: # Quitter
                        pygame.quit()
                        exit()

# ----------------------
# 🚀 Lancement
# ----------------------
main_menu()


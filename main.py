# -*- coding: utf-8 -*-

import pygame
import random
import time
from config import *
from classes import Ball, PowerUp, Brick
from drawing_utils import draw_text, draw_multiline_text
from utils import create_level, save_score
from screens import main_menu
from level_config import LEVELS

pygame.init()
pygame.mixer.init()

# --- Sound Loading ---
try:
    pygame.mixer.music.load('média/8bit-music-for-game-68698.mp3')
    brick_hit_sound = pygame.mixer.Sound('média/explosion-312361.mp3')
    game_over_sound = pygame.mixer.Sound('média/game-over-38511.mp3')
    pygame.mixer.music.set_volume(0.3)
    brick_hit_sound.set_volume(0.4)
except pygame.error as e:
    print(f"Warning: Could not load sound files: {e}")
    brick_hit_sound = None
    game_over_sound = None

def activate_power_up(p_type, effects, balls, score_ref, lives_ref, speed):
    duration = POWER_UP_PROPERTIES[p_type]["duration"]
    if duration > 0:
        effects[p_type] = time.time() + duration
    if p_type == 'bonus':
        if random.choice([True, False]):
            lives_ref[0] += 1
        else:
            score_ref[0] += 500
    elif p_type == 'multi_ball':
        new_balls = []
        for _ in range(2):
            if balls:
                original_ball = random.choice(balls)
                new_balls.append(Ball(original_ball.rect.x, original_ball.rect.y, -original_ball.speed[0], original_ball.speed[1]))
        balls.extend(new_balls)

def draw_active_effects(surface, effects):
    x_offset = 200
    for effect, end_time in effects.items():
        props = POWER_UP_PROPERTIES[effect]
        icon = props["icon"]
        color = props["color"]
        remaining_time = end_time - time.time()
        duration = props["duration"]
        pygame.draw.rect(surface, color, (x_offset, 10, 40, 30), border_radius=5)
        draw_text(icon, hud_font, (0,0,0), x_offset + 20, 25, surface=surface)
        if duration > 0:
            bar_width = (remaining_time / duration) * 40
            pygame.draw.rect(surface, HIGHLIGHT_COLOR, (x_offset, 42, bar_width, 5))
        x_offset += 50

def start_game(player_name):
    win = pygame.display.get_surface()
    clock = pygame.time.Clock()
    current_level_index = 0
    score = [0]
    lives = [3]
    if pygame.mixer.get_init(): pygame.mixer.music.play(-1)

    while current_level_index < len(LEVELS):
        bricks_data, ball_speed_initial, paddle_width_base, level_message = create_level(current_level_index)
        bricks = [Brick(data['x'], data['y'], data['type']) for data in bricks_data] # Instantiate Brick objects here
        paddle = pygame.Rect(WIDTH // 2 - paddle_width_base // 2, HEIGHT - 40, paddle_width_base, 12)
        balls = [Ball(paddle.centerx, paddle.top - 20, random.choice([-1, 1]) * ball_speed_initial, -ball_speed_initial)]
        power_ups = []
        active_effects = {}

        win.fill(BG_COLOR)
        draw_multiline_text(level_message, message_font, HIGHLIGHT_COLOR, WIDTH // 2, HEIGHT // 2, WIDTH - 40, surface=win)
        pygame.display.update()
        pygame.time.wait(2000)

        level_running = True
        paused = False
        while level_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused
                        if paused: pygame.mixer.music.pause()
                        else: pygame.mixer.music.unpause()

            if not paused:
                speed_multiplier = 1.0
                paddle_width_modifier = 0
                controls_reversed = False
                for effect, end_time in list(active_effects.items()):
                    if time.time() > end_time:
                        del active_effects[effect]
                    else:
                        if effect == 'speed_up': speed_multiplier = 1.5
                        if effect == 'slow_down': speed_multiplier = 0.5
                        if effect == 'grow_paddle': paddle_width_modifier = 50
                        if effect == 'shrink_paddle': paddle_width_modifier = -40
                        if effect == 'reverse_controls': controls_reversed = True
                
                paddle.width = paddle_width_base + paddle_width_modifier

                keys = pygame.key.get_pressed()
                move_speed = 8
                move_direction = 1 if not controls_reversed else -1
                if keys[pygame.K_LEFT] and paddle.left > 0: paddle.move_ip(-move_speed * move_direction, 0)
                if keys[pygame.K_RIGHT] and paddle.right < WIDTH: paddle.move_ip(move_speed * move_direction, 0)

                for ball in balls: ball.update(speed_multiplier)
                for p_up in power_ups: p_up.update()

                for p_up in power_ups[:]:
                    if p_up.rect.top > HEIGHT: power_ups.remove(p_up)
                    elif p_up.rect.colliderect(paddle):
                        activate_power_up(p_up.type, active_effects, balls, score, lives, ball_speed_initial)
                        power_ups.remove(p_up)

                for ball in balls[:]:
                    # Collision with paddle
                    if ball.rect.colliderect(paddle):
                        # Reposition ball to prevent tunneling
                        ball.rect.bottom = paddle.top
                        ball.speed[1] *= -1
                        # Adjust horizontal speed based on hit location on paddle
                        hit_pos = ball.rect.centerx - paddle.centerx
                        ball.speed[0] = hit_pos * 0.15 # Adjust multiplier as needed

                    if ball.rect.left < 0:
                        ball.rect.left = 0
                        ball.speed[0] *= -1
                    if ball.rect.right > WIDTH:
                        ball.rect.right = WIDTH
                        ball.speed[0] *= -1
                    if ball.rect.top < GAME_AREA_Y_START:
                        ball.rect.top = GAME_AREA_Y_START
                        ball.speed[1] *= -1

                    for brick in bricks[:]:
                        if ball.rect.colliderect(brick.rect):
                            ball.speed[1] *= -1
                            if brick_hit_sound: brick_hit_sound.play() # Play sound on hit
                            if brick.hit():
                                score[0] += brick.score_value
                                if brick.power_up_type:
                                    power_ups.append(PowerUp(brick.rect.centerx, brick.rect.centery, brick.power_up_type))
                                bricks.remove(brick)
                            break

                    if not any(b.type != 'I' for b in bricks):
                        level_running = False
                        current_level_index += 1
                    if ball.rect.bottom > HEIGHT:
                        balls.remove(ball)
                
                if not balls:
                    lives[0] -= 1
                    if lives[0] > 0:
                        balls.append(Ball(paddle.centerx, paddle.top - 20, ball_speed_initial, -ball_speed_initial))
                        pygame.time.wait(1000)
                    else:
                        level_running = False
                        current_level_index = float('inf')
                        if game_over_sound: game_over_sound.play()

            win.fill(BG_COLOR)
            pygame.draw.rect(win, HUD_BG_COLOR, (0, 0, WIDTH, TOP_PANEL_HEIGHT))
            draw_text(f"{player_name}", hud_font, HIGHLIGHT_COLOR, 10, 15, center=False, surface=win)
            draw_text(f"Score: {score[0]}", hud_font, TEXT_COLOR, 10, 35, center=False, surface=win)
            draw_text(f"Level: {current_level_index + 1}", hud_font, TEXT_COLOR, 500, 15, center=False, surface=win)
            draw_text(f"Lives: {lives[0]}", hud_font, TEXT_COLOR, 500, 35, center=False, surface=win)
            draw_active_effects(win, active_effects)

            for brick in bricks: brick.draw(win)
            for ball in balls: pygame.draw.ellipse(win, BALL_COLOR, ball.rect)
            pygame.draw.rect(win, PADDLE_COLOR, paddle, border_radius=4)
            for p_up in power_ups: p_up.draw(win)

            if paused:
                overlay = pygame.Surface((WIDTH, HEIGHT - TOP_PANEL_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                win.blit(overlay, (0, TOP_PANEL_HEIGHT))
                draw_text("PAUSED", title_font, HIGHLIGHT_COLOR, WIDTH // 2, HEIGHT // 2, surface=win)

            pygame.display.update()
            clock.tick(60)

    win.fill(BG_COLOR)
    final_score = score[0]
    if lives[0] > 0:
        draw_text("CONGRATULATIONS!", title_font, HIGHLIGHT_COLOR, WIDTH // 2, HEIGHT // 2 - 50, surface=win)
        draw_text(f"Final Score: {final_score}", menu_font, TEXT_COLOR, WIDTH // 2, HEIGHT // 2 + 20, surface=win)
    else:
        draw_text("GAME OVER", title_font, RED, WIDTH // 2, HEIGHT // 2 - 50, surface=win)
        draw_text(f"Final Score: {final_score}", menu_font, TEXT_COLOR, WIDTH // 2, HEIGHT // 2 + 20, surface=win)
    
    save_score(player_name, final_score)
    draw_text("Press Enter to continue", info_font, TEXT_COLOR, WIDTH // 2, HEIGHT - 100, surface=win)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: waiting = False

if __name__ == "__main__":
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    main_menu(win, start_game)

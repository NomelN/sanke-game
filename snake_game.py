import tkinter as tk
import random
import math
import pygame
import json
import os

# --- Constantes ---
WIDTH = 600
HEIGHT = 600
SEGMENT_SIZE = 20
GAME_SPEED = 100  # Millisecondes
SCORE_FILE = "scores.json"

# --- Thème Futuriste ---
BG_COLOR = "#0A0A2A"  # Bleu nuit profond
GRID_COLOR = "#1A1A3A"
SNAKE_HEAD_COLOR = "#61FFD8"  # Cyan vif
SNAKE_BODY_COLOR = "#00BFFF"  # Bleu ciel
FOOD_COLOR_1 = "#FF00FF"  # Magenta
FOOD_COLOR_2 = "#FF69B4"  # Rose vif
TEXT_COLOR = "#E0E0E0"  # Blanc cassé
HIGHLIGHT_COLOR = "#FFFFFF" # Blanc pour la sélection
OBSTACLE_COLOR = "#480048" # Violet foncé
SPECIAL_FOOD_COLOR_1 = "#FFFF00"  # Jaune vif
SPECIAL_FOOD_COLOR_2 = "#FFA500"  # Orange vif
SPECIAL_FOOD_SIZE_MULTIPLIER = 1.5
SPECIAL_FOOD_SPAWN_INTERVAL = 10000  # 10 secondes
SPECIAL_FOOD_LIFESPAN = 5000  # 5 secondes

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Cyber Snake")
        self.master.resizable(False, False)
        self.master.configure(bg=BG_COLOR)

        self.canvas = tk.Canvas(self.master, width=WIDTH, height=HEIGHT, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack()

        self.master.bind("<KeyPress>", self.on_key_press)

        pygame.mixer.init()
        # Check for media directory and files
        if os.path.exists("média/explosion-312361.mp3"):
            self.collision_sound = pygame.mixer.Sound("média/explosion-312361.mp3")
        else:
            self.collision_sound = None
        if os.path.exists("média/food.mp3"):
            self.food_sound = pygame.mixer.Sound("média/food.mp3")
        else:
            self.food_sound = None

        if os.path.exists("média/8bit-music-for-game-68698.mp3"):
            self.menu_music_path = "média/8bit-music-for-game-68698.mp3"
        else:
            self.menu_music_path = None
            print("Warning: Menu background music file not found.")

        if os.path.exists("média/8bit-music-for-game-68698.mp3"):
            self.game_music_path = "média/8bit-music-for-game-68698.mp3"
        else:
            self.game_music_path = None
            print("Warning: Game background music file not found.")

        if os.path.exists("média/game-over-38511.mp3"):
            self.game_over_sound = pygame.mixer.Sound("média/game-over-38511.mp3")
        else:
            self.game_over_sound = None
            print("Warning: Game Over sound file not found.")

        self.state = 'menu'
        self.current_player = ""
        self.selected_menu_option = 0
        self.menu_options = ["[ START ]", "[ HIGH SCORES ]", "[ QUIT ]"]
        self.scores = self.load_scores()
        self.pulse_state = True
        self.special_food = None
        self.special_food_timer = None
        self.special_food_exists = False
        self.draw_menu()

    def draw_grid(self):
        for i in range(0, WIDTH, SEGMENT_SIZE):
            self.canvas.create_line([(i, 0), (i, HEIGHT)], tag='grid_line', fill=GRID_COLOR)
        for i in range(0, HEIGHT, SEGMENT_SIZE):
            self.canvas.create_line([(0, i), (WIDTH, i)], tag='grid_line', fill=GRID_COLOR)

    def draw_menu(self):
        self.canvas.delete("all")
        self.draw_grid()
        if self.menu_music_path and not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(self.menu_music_path)
            pygame.mixer.music.play(-1)
        self.canvas.create_text(
            WIDTH / 2, HEIGHT / 2 - 150,
            text="CYBER SNAKE",
            font=("Consolas", 50, "bold"), fill=SNAKE_HEAD_COLOR, anchor="center"
        )
        for i, option_text in enumerate(self.menu_options):
            color = HIGHLIGHT_COLOR if i == self.selected_menu_option else TEXT_COLOR
            display_text = f"> {option_text} <" if i == self.selected_menu_option else option_text
            self.canvas.create_text(
                WIDTH / 2, HEIGHT / 2 - 20 + (i * 60),
                text=display_text,
                font=("Consolas", 24, "bold"), fill=color, anchor="center", tags="menu_button"
            )

    def draw_name_input_screen(self):
        self.canvas.delete("all")
        self.draw_grid()
        self.canvas.create_text(WIDTH / 2, HEIGHT / 2 - 100,
            text="ENTER YOUR NAME",
            font=("Consolas", 30, "bold"), fill=TEXT_COLOR, anchor="center")

        # Display the name being typed with a cursor
        display_text = self.current_player + "_"
        self.canvas.create_text(WIDTH / 2, HEIGHT / 2,
            text=display_text,
            font=("Consolas", 40, "bold"), fill=HIGHLIGHT_COLOR, anchor="center")

        self.canvas.create_text(WIDTH / 2, HEIGHT - 100,
            text="Max 10 characters. Press Enter to continue.",
            font=("Consolas", 14), fill=TEXT_COLOR, anchor="center")

    def draw_high_scores_screen(self):
        self.canvas.delete("all")
        self.draw_grid()
        self.canvas.create_text(WIDTH / 2, 50,
            text="HIGH SCORES",
            font=("Consolas", 40, "bold"), fill=SNAKE_HEAD_COLOR, anchor="center")

        if not self.scores:
            self.canvas.create_text(WIDTH / 2, HEIGHT / 2,
                text="NO SCORES YET!",
                font=("Consolas", 24), fill=TEXT_COLOR, anchor="center")
        else:
            for i, entry in enumerate(self.scores):
                name = entry.get('name', 'N/A')
                score = entry.get('score', 0)
                self.canvas.create_text(WIDTH / 2, 150 + i * 40,
                    text=f"{i+1: >2}. {name: <10} - {score: >5}",
                    font=("Consolas", 20, "bold"), fill=TEXT_COLOR, anchor="center")

        self.canvas.create_text(WIDTH / 2, HEIGHT - 50,
            text="Press Enter to return to menu",
            font=("Consolas", 14), fill=TEXT_COLOR, anchor="center")

    def load_scores(self):
        if not os.path.exists(SCORE_FILE):
            return []
        try:
            with open(SCORE_FILE, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_scores(self):
        self.scores.append({"name": self.current_player, "score": self.score})
        self.scores.sort(key=lambda s: s.get('score', 0), reverse=True)
        self.scores = self.scores[:10]
        with open(SCORE_FILE, 'w') as f:
            json.dump(self.scores, f, indent=4)

    def start_game(self):
        self.canvas.delete("all")
        self.draw_grid()
        self.snake = []
        self.obstacles = []
        self.direction = "Right"
        self.score = 0

        for i in range(3):
            x = (WIDTH / 2) - (i * SEGMENT_SIZE)
            y = HEIGHT / 2
            color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_BODY_COLOR
            segment = self.canvas.create_rectangle(x, y, x + SEGMENT_SIZE, y + SEGMENT_SIZE, fill=color, outline=SNAKE_HEAD_COLOR, width=1)
            self.snake.append(segment)

        self.create_obstacles()

        self.score_text = self.canvas.create_text(
            10, 10, text=f"Score: {self.score}",
            font=("Consolas", 16, "bold"), fill=TEXT_COLOR, anchor="nw"
        )

        self.create_food()
        self.animate_food()
        self.master.after(SPECIAL_FOOD_SPAWN_INTERVAL, self.create_special_food_timed)

    def create_obstacles(self):
        for _ in range(5):
            length = random.randint(2, 5)
            start_x = random.randint(2, (WIDTH // SEGMENT_SIZE) - 7) * SEGMENT_SIZE
            start_y = random.randint(2, (HEIGHT // SEGMENT_SIZE) - 7) * SEGMENT_SIZE
            for i in range(length):
                if random.choice([True, False]):
                    x = start_x + i * SEGMENT_SIZE
                    y = start_y
                else:
                    x = start_x
                    y = start_y + i * SEGMENT_SIZE
                obstacle = self.canvas.create_rectangle(x, y, x + SEGMENT_SIZE, y + SEGMENT_SIZE, fill=OBSTACLE_COLOR, outline=GRID_COLOR)
                self.obstacles.append(obstacle)

    def create_food(self):
        while True:
            x = random.randint(0, (WIDTH // SEGMENT_SIZE) - 1) * SEGMENT_SIZE
            y = random.randint(0, (HEIGHT // SEGMENT_SIZE) - 1) * SEGMENT_SIZE
            on_snake = any(self.canvas.coords(seg) == [float(x), float(y), float(x + SEGMENT_SIZE), float(y + SEGMENT_SIZE)] for seg in self.snake)
            on_obstacle = any(self.canvas.coords(obs) == [float(x), float(y), float(x + SEGMENT_SIZE), float(y + SEGMENT_SIZE)] for obs in self.obstacles)
            if not on_snake and not on_obstacle:
                break
        self.food = self.canvas.create_polygon(
            x + SEGMENT_SIZE / 2, y,
            x + SEGMENT_SIZE, y + SEGMENT_SIZE / 2,
            x + SEGMENT_SIZE / 2, y + SEGMENT_SIZE,
            x, y + SEGMENT_SIZE / 2,
            fill=FOOD_COLOR_1, outline=TEXT_COLOR
        )

    def create_special_food(self):
        while True:
            x = random.randint(0, (WIDTH // SEGMENT_SIZE) - 1) * SEGMENT_SIZE
            y = random.randint(0, (HEIGHT // SEGMENT_SIZE) - 1) * SEGMENT_SIZE
            on_snake = any(self.canvas.coords(seg) == [float(x), float(y), float(x + SEGMENT_SIZE), float(y + SEGMENT_SIZE)] for seg in self.snake)
            on_obstacle = any(self.canvas.coords(obs) == [float(x), float(y), float(x + SEGMENT_SIZE), float(y + SEGMENT_SIZE)] for obs in self.obstacles)
            if not on_snake and not on_obstacle:
                break
        
        # Calculate larger size for special food
        special_size = SEGMENT_SIZE * SPECIAL_FOOD_SIZE_MULTIPLIER
        offset = (special_size - SEGMENT_SIZE) / 2

        self.special_food = self.canvas.create_oval(
            x - offset, y - offset,
            x + SEGMENT_SIZE + offset, y + SEGMENT_SIZE + offset,
            fill=SPECIAL_FOOD_COLOR_1, outline=SPECIAL_FOOD_COLOR_2, width=2
        )
        self.special_food_exists = True
        self.special_food_timer = self.master.after(SPECIAL_FOOD_LIFESPAN, self.remove_special_food)
        self.animate_special_food()

    def remove_special_food(self):
        if self.special_food:
            self.canvas.delete(self.special_food)
            self.special_food = None
            self.special_food_exists = False
        if self.special_food_timer:
            self.master.after_cancel(self.special_food_timer)
            self.special_food_timer = None

    def animate_special_food(self):
        if self.state != 'game' or not self.special_food_exists:
            return
        current_color = self.canvas.itemcget(self.special_food, "fill")
        next_color = SPECIAL_FOOD_COLOR_1 if current_color == SPECIAL_FOOD_COLOR_2 else SPECIAL_FOOD_COLOR_2
        self.canvas.itemconfig(self.special_food, fill=next_color)
        self.master.after(200, self.animate_special_food)

    def move_snake(self):
        if not self.snake or not self.canvas.coords(self.snake[0]):
            return
        head_x1, head_y1, _, _ = self.canvas.coords(self.snake[0])
        self.canvas.itemconfig(self.snake[0], fill=SNAKE_BODY_COLOR)
        if self.direction == "Left":
            new_head_x = head_x1 - SEGMENT_SIZE
            new_head_y = head_y1
        elif self.direction == "Right":
            new_head_x = head_x1 + SEGMENT_SIZE
            new_head_y = head_y1
        elif self.direction == "Up":
            new_head_x = head_x1
            new_head_y = head_y1 - SEGMENT_SIZE
        elif self.direction == "Down":
            new_head_x = head_x1
            new_head_y = head_y1 + SEGMENT_SIZE
        new_head = self.canvas.create_rectangle(
            new_head_x, new_head_y,
            new_head_x + SEGMENT_SIZE, new_head_y + SEGMENT_SIZE,
            fill=SNAKE_HEAD_COLOR, outline=SNAKE_HEAD_COLOR, width=1
        )
        self.snake.insert(0, new_head)
        food_coords = self.canvas.coords(self.food)
        head_coords = self.canvas.coords(self.snake[0])
        if head_coords[0] < food_coords[2] and head_coords[2] > food_coords[0] and \
           head_coords[1] < food_coords[5] and head_coords[3] > food_coords[1]:
            if self.food_sound: self.food_sound.play()
            self.canvas.delete(self.food)
            self.create_food()
            self.score += 10
            self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
        elif self.special_food_exists:
            special_food_coords = self.canvas.coords(self.special_food)
            if head_coords[0] < special_food_coords[2] and head_coords[2] > special_food_coords[0] and \
               head_coords[1] < special_food_coords[3] and head_coords[3] > special_food_coords[1]:
                if self.food_sound: self.food_sound.play()
                self.remove_special_food()
                self.score += 25
                self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
            else:
                tail = self.snake.pop()
                self.canvas.delete(tail)
        else:
            tail = self.snake.pop()
            self.canvas.delete(tail)

    def check_collisions(self):
        if not self.snake or not self.canvas.coords(self.snake[0]):
            return False
        head_x1, head_y1, head_x2, head_y2 = self.canvas.coords(self.snake[0])
        if head_x1 < 0 or head_x2 > WIDTH or head_y1 < 0 or head_y2 > HEIGHT:
            return True
        for segment in self.snake[1:]:
            if self.canvas.coords(segment) == [head_x1, head_y1, head_x2, head_y2]:
                return True
        for obstacle in self.obstacles:
            if self.canvas.coords(obstacle) == [head_x1, head_y1, head_x2, head_y2]:
                return True
        return False

    def on_key_press(self, e):
        key = e.keysym

        if self.state == 'menu':
            if key == 'Up':
                self.selected_menu_option = (self.selected_menu_option - 1) % len(self.menu_options)
            elif key == 'Down':
                self.selected_menu_option = (self.selected_menu_option + 1) % len(self.menu_options)
            elif key == 'Return':
                if self.selected_menu_option == 0:  # Start
                    self.state = 'name_input'
                    self.draw_name_input_screen()
                    return
                elif self.selected_menu_option == 1:  # High Scores
                    self.state = 'high_scores'
                    self.draw_high_scores_screen()
                    return
                elif self.selected_menu_option == 2:  # Quit
                    self.master.destroy()
                    return
            self.draw_menu()

        elif self.state == 'name_input':
            if key == 'Return':
                if self.current_player:
                    pygame.mixer.music.stop()
                    if self.game_music_path:
                        pygame.mixer.music.load(self.game_music_path)
                        pygame.mixer.music.play(-1)
                    self.state = 'game'
                    self.start_game()
                    self.game_loop()
                    return # Empêche de redessiner l'écran de saisie
            elif key == 'BackSpace':
                self.current_player = self.current_player[:-1]
            elif len(key) == 1 and len(self.current_player) < 10:
                self.current_player += key.upper()
            self.draw_name_input_screen()

        elif self.state == 'high_scores':
            if key == 'Return' or key == 'Escape':
                self.state = 'menu'
                self.draw_menu()
                if self.menu_music_path and not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load(self.menu_music_path)
                    pygame.mixer.music.play(-1)

        elif self.state == 'game_over':
            if key == 'Return':
                pygame.mixer.music.stop()
                self.state = 'menu'
                self.current_player = ""
                self.draw_menu()
                if self.menu_music_path and not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load(self.menu_music_path)
                    pygame.mixer.music.play(-1)

        elif self.state == 'game':
            all_directions = ["Left", "Right", "Up", "Down"]
            opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
            if (key in all_directions) and (key != opposites.get(self.direction)):
                self.direction = key

    def animate_food(self):
        if self.state != 'game':
            return
        # Check if food exists
        if not self.canvas.find_withtag(self.food):
             return
        current_color = self.canvas.itemcget(self.food, "fill")
        next_color = FOOD_COLOR_1 if current_color == FOOD_COLOR_2 else FOOD_COLOR_2
        self.canvas.itemconfig(self.food, fill=next_color)
        self.master.after(400, self.animate_food)

    def create_special_food_timed(self):
        if self.state == 'game' and not self.special_food_exists:
            self.create_special_food()
        self.master.after(SPECIAL_FOOD_SPAWN_INTERVAL, self.create_special_food_timed)

    def dissolve_snake(self, segment_index):
        if segment_index < len(self.snake):
            segment = self.snake[segment_index]
            self.canvas.itemconfig(segment, fill=OBSTACLE_COLOR, outline="")
            self.master.after(50, self.dissolve_snake, segment_index + 1)
        else:
            self.display_final_text()

    def display_game_over(self):
        if self.collision_sound: self.collision_sound.play()
        if self.game_over_sound: self.game_over_sound.play()
        pygame.mixer.music.stop()
        self.state = 'game_over'
        self.dissolve_snake(0)

    def display_final_text(self):
        self.save_scores()
        self.canvas.create_text(
            WIDTH / 2, HEIGHT / 2 - 50,
            text="GAME OVER",
            font=("Consolas", 40, "bold"), fill="#FF5555", anchor="center"
        )
        self.canvas.create_text(
            WIDTH / 2, HEIGHT / 2,
            text=f"Final Score: {self.score}",
            font=("Consolas", 24), fill=TEXT_COLOR, anchor="center"
        )
        self.canvas.create_text(
            WIDTH / 2, HEIGHT / 2 + 60,
            text="Press Enter to return to Menu",
            font=("Consolas", 16), fill=TEXT_COLOR, anchor="center"
        )

    def game_loop(self):
        if self.state != 'game':
            return
        if self.check_collisions():
            self.display_game_over()
            return
        self.move_snake()
        self.master.after(GAME_SPEED, self.game_loop)

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()

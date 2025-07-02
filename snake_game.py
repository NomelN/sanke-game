import tkinter as tk
import random
import math
import pygame

# --- Constantes ---
WIDTH = 600
HEIGHT = 600
SEGMENT_SIZE = 20
GAME_SPEED = 100  # Millisecondes

# --- Thème Futuriste ---
BG_COLOR = "#0A0A2A"  # Bleu nuit profond
GRID_COLOR = "#1A1A3A"
SNAKE_HEAD_COLOR = "#61FFD8"  # Cyan vif
SNAKE_BODY_COLOR = "#00BFFF"  # Bleu ciel
FOOD_COLOR_1 = "#FF00FF"  # Magenta
FOOD_COLOR_2 = "#FF69B4"  # Rose vif
TEXT_COLOR = "#E0E0E0"  # Blanc cassé
OBSTACLE_COLOR = "#480048" # Violet foncé

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
        self.collision_sound = pygame.mixer.Sound("média/explosion-312361.mp3")
        self.food_sound = pygame.mixer.Sound("média/bubblepop-254773.mp3")

        self.pulse_state = True
        self.start_game()

    def draw_grid(self):
        for i in range(0, WIDTH, SEGMENT_SIZE):
            self.canvas.create_line([(i, 0), (i, HEIGHT)], tag='grid_line', fill=GRID_COLOR)
        for i in range(0, HEIGHT, SEGMENT_SIZE):
            self.canvas.create_line([(0, i), (WIDTH, i)], tag='grid_line', fill=GRID_COLOR)

    def start_game(self):
        self.canvas.delete("all")
        self.draw_grid()
        self.snake = []
        self.obstacles = []
        self.direction = "Right"
        self.score = 0
        self.game_over_flag = False

        # Création du serpent initial
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
        self.game_loop()

    def create_obstacles(self):
        for _ in range(5): # Créer 5 blocs d'obstacles
            length = random.randint(2, 5)
            start_x = random.randint(2, (WIDTH // SEGMENT_SIZE) - 7) * SEGMENT_SIZE
            start_y = random.randint(2, (HEIGHT // SEGMENT_SIZE) - 7) * SEGMENT_SIZE
            for i in range(length):
                # Aléatoirement horizontal ou vertical
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

        # Créer une forme de diamant pour la nourriture
        self.food = self.canvas.create_polygon(
            x + SEGMENT_SIZE / 2, y,
            x + SEGMENT_SIZE, y + SEGMENT_SIZE / 2,
            x + SEGMENT_SIZE / 2, y + SEGMENT_SIZE,
            x, y + SEGMENT_SIZE / 2,
            fill=FOOD_COLOR_1, outline=TEXT_COLOR
        )

    def move_snake(self):
        head_x1, head_y1, _, _ = self.canvas.coords(self.snake[0])
        self.canvas.itemconfig(self.snake[0], fill=SNAKE_BODY_COLOR) # L'ancienne tête devient corps

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

        # Simple collision check based on bounding boxes
        if head_coords[0] < food_coords[2] and head_coords[2] > food_coords[0] and \
           head_coords[1] < food_coords[5] and head_coords[3] > food_coords[1]:
            self.food_sound.play()
            self.canvas.delete(self.food)
            self.create_food()
            self.score += 10
            self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
        else:
            tail = self.snake.pop()
            self.canvas.delete(tail)

    def check_collisions(self):
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
        new_direction = e.keysym

        if self.game_over_flag and new_direction == "Return":
            self.start_game()
            return

        all_directions = ["Left", "Right", "Up", "Down"]
        opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}

        if (new_direction in all_directions) and (new_direction != opposites.get(self.direction)):
            self.direction = new_direction

    def animate_food(self):
        if self.game_over_flag:
            return
        current_color = self.canvas.itemcget(self.food, "fill")
        next_color = FOOD_COLOR_1 if current_color == FOOD_COLOR_2 else FOOD_COLOR_2
        self.canvas.itemconfig(self.food, fill=next_color)
        self.master.after(400, self.animate_food)

    def dissolve_snake(self, segment_index):
        if segment_index < len(self.snake):
            segment = self.snake[segment_index]
            self.canvas.itemconfig(segment, fill=OBSTACLE_COLOR, outline="")
            self.master.after(50, self.dissolve_snake, segment_index + 1)
        else:
            self.display_final_text()

    def display_game_over(self):
        self.collision_sound.play()
        self.game_over_flag = True
        self.dissolve_snake(0)


    def display_final_text(self):
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
            text="Press Enter to Restart",
            font=("Consolas", 16), fill=TEXT_COLOR, anchor="center"
        )

    def game_loop(self):
        if self.game_over_flag:
            return

        if self.check_collisions():
            self.display_game_over()
            return

        self.move_snake()
        self.master.after(GAME_SPEED, self.game_loop)

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    # Lancer l'animation de la nourriture une fois
    root.after(400, game.animate_food)
    root.mainloop()
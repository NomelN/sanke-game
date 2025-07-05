# -*- coding: utf-8 -*-

import json
import os
from drawing_utils import draw_text, draw_multiline_text
from config import SCORE_FILE, WIDTH, GAME_AREA_Y_START
from level_config import LEVELS

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
    scores = scores[:10]
    with open(SCORE_FILE, 'w') as f:
        json.dump(scores, f, indent=4)

def create_level(level_index):
    if level_index >= len(LEVELS):
        return None, None, None, None
    level_data = LEVELS[level_index]
    layout = level_data["layout"]
    bricks_data = [] # Store raw data, not objects
    num_cols = len(layout[0])
    brick_width = 50
    brick_height = 20
    gap = 5
    total_layout_width = num_cols * (brick_width + gap) - gap
    start_x = (WIDTH - total_layout_width) // 2
    for row_idx, row in enumerate(layout):
        for col_idx, brick_type in enumerate(row):
            if brick_type != '_':
                x = start_x + col_idx * (brick_width + gap)
                y = GAME_AREA_Y_START + 50 + row_idx * (brick_height + gap)
                bricks_data.append({'x': x, 'y': y, 'type': brick_type})
    return bricks_data, level_data["ball_speed"], level_data["paddle_size"], level_data.get("message", "")

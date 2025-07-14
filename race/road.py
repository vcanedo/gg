import pygame
import math
from settings import (
    SEGMENTS, SEGMENT_LENGTH, GRASS, GRASS_ALT, ROAD, LANE,
    SCREEN_WIDTH, SCREEN_HEIGHT, CAMERA_HEIGHT, PLAYER_Z,
    DRAW_DISTANCE
)
from utils import project

road = []
for i in range(SEGMENTS):
    curve = math.sin(i * 0.1) * 2
    road.append({
        "index": i,
        "z": i * SEGMENT_LENGTH,
        "curve": curve
    })

def draw_road(screen, car_x, car_pos):
    base_index = int(car_pos / SEGMENT_LENGTH) % SEGMENTS
    base_z = car_pos
    camera_x = car_x
    camera_y = CAMERA_HEIGHT
    camera_z = base_z - PLAYER_Z

    x = 0
    dx = 0

    for n in range(DRAW_DISTANCE):
        segment = road[(base_index + n) % SEGMENTS]
        segment_looped = segment["z"] - base_z

        curve = segment["curve"]
        dx += curve

        x1, y1, w1 = project(x, 0, segment_looped, camera_x, camera_y, camera_z)
        x2, y2, w2 = project(x + dx, 0, segment_looped + SEGMENT_LENGTH, camera_x, camera_y, camera_z)

        if y2 >= y1:
            continue

        grass_color = GRASS if (segment["index"] % 2 == 0) else GRASS_ALT
        pygame.draw.polygon(screen, grass_color, [(0, y2), (SCREEN_WIDTH, y2), (SCREEN_WIDTH, y1), (0, y1)])

        pygame.draw.polygon(screen, ROAD, [
            (x1 - w1, y1), (x1 + w1, y1),
            (x2 + w2, y2), (x2 - w2, y2)
        ])

        if segment["index"] % 20 < 10:
            pygame.draw.polygon(screen, LANE, [
                (x1 - w1 * 0.05, y1), (x1 + w1 * 0.05, y1),
                (x2 + w2 * 0.05, y2), (x2 - w2 * 0.05, y2)
            ])

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, CAMERA_DEPTH, ROAD_WIDTH

def project(x, y, z, camera_x, camera_y, camera_z):
    dz = z - camera_z
    if dz == 0:
        dz = 0.0001
    scale = CAMERA_DEPTH / dz
    screen_x = (1 + scale * (x - camera_x)) * SCREEN_WIDTH / 2
    screen_y = (1 - scale * (y - camera_y)) * SCREEN_HEIGHT / 2
    screen_w = scale * ROAD_WIDTH * SCREEN_WIDTH / 2
    return screen_x, screen_y, screen_w

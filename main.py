import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 1200, 700
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Balls in a Circle")


def draw_circle():
    pygame.draw.circle(window, (255,255,255), (WIDTH//2, HEIGHT//2), 200, 2)

# Balls stuff
def create_ball(x, y, xv, yv, radius, color = None):
    if color == None:
        color = (255,0 ,0)# random.choice(list(colors.values()))
    ball = {'x': x, 'y': y, 'vector': {'x': xv, 'y': yv}, 'radius': radius, 'color': color, "original_color": color, "is_held": False}
    balls.append(ball)
    every_obj.append(ball)

def draw_all_balls():
    for ball in balls:
        pygame.draw.circle(window, ball['color'], (ball['x'], ball['y']), ball['radius'])
# Useful functions
def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

# Calc vector
def calc_vector(x1, y1, x2, y2, flip = False) -> tuple[float, float]:
    if flip:
        return [float(x1) - float(x2), float(y1) - float(y2)]
    return (float(x2) - float(x1), float(y2) - float(y1))


def simulate_physics():
    center: tuple = (WIDTH//2, HEIGHT//2)
    radius = 200
    gravity = 1
 
    for ball in balls:

        ball["y"] += ball["vector"]["y"]
        ball["x"] += ball["vector"]["x"]

        # Applay gravity
        ball["vector"]["y"] += gravity

        d = distance(center[0], center[1], ball["x"], ball["y"])
        if d > radius - ball["radius"]:
            v = calc_vector(ball["x"], ball["y"], center[0], center[1])
            ball["vector"]["x"] = v[0] * 0.05
            ball["vector"]["y"] = v[1] * 0.05
            

    # Check for collisions between balls
    for i, ball1 in enumerate(balls):
        for j, ball2 in enumerate(balls):
            if i != j:
                dx = ball2['x'] - ball1['x']
                dy = ball2['y'] - ball1['y']
                dist = (dx**2 + dy**2)**0.5 + 2

                # Check if the balls are colliding
                if dist < ball1['radius'] + ball2['radius']:
                    # Resolve overlap
                    overlap = ball1['radius'] + ball2['radius'] - dist
                    if dist != 0:
                        dx_norm = dx / dist
                        dy_norm = dy / dist
                    else:
                        dx_norm = 0
                        dy_norm = 0
                    ball1['x'] -= dx_norm * overlap / 2
                    ball1['y'] -= dy_norm * overlap / 2
                    ball2['x'] += dx_norm * overlap / 2
                    ball2['y'] += dy_norm * overlap / 2

                    # Calculate velocity components along the collision normal
                    v1n = ball1['vector']['x'] * dx_norm + ball1['vector']['y'] * dy_norm
                    v2n = ball2['vector']['x'] * dx_norm + ball2['vector']['y'] * dy_norm

                    # Exchange the normal components of velocity
                    ball1['vector']['x'] += (v2n - v1n) * dx_norm
                    ball1['vector']['y'] += (v2n - v1n) * dy_norm
                    ball2['vector']['x'] += (v1n - v2n) * dx_norm
                    ball2['vector']['y'] += (v1n - v2n) * dy_norm


# Set up lists
balls = []
every_obj = []
mouse_pos = []

# Set up variables
ball_size = 15


running = True
clock = pygame.time.Clock()
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill((95,95,95))

    # Check for mouse click events
    if pygame.mouse.get_pressed()[0]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if len(balls) == 0:
            create_ball(mouse_x, mouse_y, 0, 0, ball_size)
        if distance(balls[-1]["x"], balls[-1]["y"], mouse_x, mouse_y) > ball_size+2 and len(balls) < 200:
            last_x, last_y = mouse_x, mouse_y
            create_ball(mouse_x, mouse_y, 0, 0, ball_size)

    # Detect keyboard inputs
    keys = pygame.key.get_pressed()
    if keys[pygame.K_c]:
        balls = []


    draw_circle()
    draw_all_balls()
    simulate_physics()

    # Draw the number of balls
    font = pygame.font.Font(None, 24)
    text = font.render(f"Balls: {len(balls)}", True, (255, 255, 255))
    window.blit(text, (5, 10))
    # Draw the FPS
    font = pygame.font.Font(None, 24)
    text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
    window.blit(text, (5, 30))

    pygame.display.flip()

pygame.quit()

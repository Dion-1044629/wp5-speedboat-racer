import pygame
import math
from timer import CountdownTimer
from boat import Boat
from boat_input import BoatInputState, update_input

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    WORLD_W, WORLD_H = 4000, 3000
    pygame.display.set_caption("WP5 Speedboat Racer")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    input_state = BoatInputState()
    boat = Boat(x=640, y=360)
    race_timer = CountdownTimer(total_seconds=120)

    game_over = False
    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # seconds
        race_timer.update(dt)
        if race_timer.is_done:
            game_over = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if not game_over:
            gas = keys[pygame.K_w] or keys[pygame.K_UP]
            brk = keys[pygame.K_s] or keys[pygame.K_DOWN]
            left = keys[pygame.K_a] or keys[pygame.K_LEFT]
            right = keys[pygame.K_d] or keys[pygame.K_RIGHT]

            input_state = update_input(
                input_state,
                gas=bool(gas),
                brake=bool(brk),
                left=bool(left),
                right=bool(right),
                dt=dt,
            )

            boat.update(
                throttle=input_state.throttle,
                brake=input_state.brake,
                steer=input_state.steer,
                dt=dt,
            )

            boat.x = max(0, min(WORLD_W, boat.x))
            boat.y = max(0, min(WORLD_H, boat.y))

        else:
            if keys[pygame.K_ESCAPE]:
                running = False
            if keys[pygame.K_r]:
                boat.x, boat.y = 640, 360
                boat.angle = 0.0
                boat.speed = 0.0
                input_state = BoatInputState()
                race_timer = CountdownTimer(total_seconds=120)
                game_over = False

        screen.fill((20, 20, 25))
        timer_text = font.render(f"Time: {race_timer.as_text()}", True, (230, 230, 230))
        screen.blit(timer_text, (20, 50))

        cam_x = boat.x - 1280 / 2
        cam_y = boat.y - 720 / 2

        # World grid
        grid = 200
        for x in range(0, WORLD_W + 1, grid):
            sx = x - cam_x
            if 0 <= sx <= 1280:
                pygame.draw.line(screen, (35, 35, 45), (sx, -cam_y), (sx, WORLD_H - cam_y))
        for y in range(0, WORLD_H + 1, grid):
            sy = y - cam_y
            if 0 <= sy <= 720:
                pygame.draw.line(screen, (35, 35, 45), (-cam_x, sy), (WORLD_W - cam_x, sy))

        debug = f"world=({boat.x:.0f},{boat.y:.0f}) speed={boat.speed:.0f} throttle={input_state.throttle:.2f} steer={input_state.steer:.2f}"
        text = font.render(debug, True, (230, 230, 230))
        screen.blit(text, (20, 20))

        # Draw boat as a rotated triangle
        cx, cy = boat.x - cam_x, boat.y - cam_y
        a = boat.angle
        size = 18

        p1 = (cx + math.cos(a) * size * 1.6, cy + math.sin(a) * size * 1.6)
        p2 = (cx + math.cos(a + 2.5) * size, cy + math.sin(a + 2.5) * size)
        p3 = (cx + math.cos(a - 2.5) * size, cy + math.sin(a - 2.5) * size)

        pygame.draw.polygon(screen, (80, 170, 255), [p1, p2, p3])

        if game_over:
            overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            big = pygame.font.SysFont(None, 72)
            msg = big.render("GAME OVER", True, (255, 255, 255))
            sub = font.render("Press R to restart or ESC to quit", True, (230, 230, 230))
            screen.blit(msg, (1280/2 - msg.get_width()/2, 720/2 - 60))
            screen.blit(sub, (1280/2 - sub.get_width()/2, 720/2 + 10))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

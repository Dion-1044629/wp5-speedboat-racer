import pygame
from boat_input import BoatInputState, update_input

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("WP5 Speedboat Racer")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    input_state = BoatInputState()

    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
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

        screen.fill((20, 20, 25))
        debug = f"throttle={input_state.throttle:.2f} brake={input_state.brake:.2f} steer={input_state.steer:.2f}"
        text = font.render(debug, True, (230, 230, 230))
        screen.blit(text, (20, 20))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

import pygame
import math

DEBUG = False

from src.bot_ai import bot_decide
from src.track import Checkpoint, Track, RacerProgress, update_progress
from src.ranking import RacerSnapshot, position_of
from src.timer import CountdownTimer
from src.boat import Boat
from src.boat_input import BoatInputState, update_input

def separate_bots(bots, min_dist: float = 28.0, strength: float = 0.5):
    """
    Simple pairwise separation: if two bots are too close, push them apart a bit.
    strength: 0..1 factor per frame (small is fine).
    """
    for i in range(len(bots)):
        for j in range(i + 1, len(bots)):
            dx = bots[j].x - bots[i].x
            dy = bots[j].y - bots[i].y
            d = math.hypot(dx, dy)
            if d == 0:
                dx, dy, d = 1.0, 0.0, 1.0
            if d < min_dist:
                push = (min_dist - d) / min_dist * strength
                nx = dx / d
                ny = dy / d
                bots[i].x -= nx * push * min_dist
                bots[i].y -= ny * push * min_dist
                bots[j].x += nx * push * min_dist
                bots[j].y += ny * push * min_dist

def main():
    pygame.init()
    pygame.mixer.init()

    def dist2(ax, ay, bx, by):
        dx = ax - bx
        dy = ay - by
        return dx*dx + dy*dy

    SFX_START = pygame.mixer.Sound("assets/sfx/start.wav")
    SFX_END   = pygame.mixer.Sound("assets/sfx/end.wav")

    SFX_START.set_volume(0.25) 
    SFX_END.set_volume(0.35)

    screen = pygame.display.set_mode((1280, 720))
    WORLD_W, WORLD_H = 4000, 3000
    pygame.display.set_caption("WP5 Speedboat Racer")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    input_state = BoatInputState()
    boat = Boat(x=640, y=360)
    race_timer = CountdownTimer(total_seconds=120)

    BASE_PLAYER_MAX_SPEED = boat.max_speed
    BOOST_FACTOR = 1.35        
    BOOST_DURATION = 2.0       
    boost_time_left = 0.0

    PICKUP_RADIUS = 14
    BOAT_RADIUS = 18

    boost_pickups = [
        (1400, 600),
        (900, 1500),
        (640, 2000),
    ]

    track = Track([
        Checkpoint(640, 360, 80),     
        Checkpoint(1400, 360, 120),
        Checkpoint(1400, 1000, 120),
        Checkpoint(900, 1400, 80),
        Checkpoint(640, 2200, 80),    
    ])

    player_prog = RacerProgress()

    # tijdelijke bots (alleen posities, nog geen AI)
    bot_progs = [RacerProgress() for _ in range(4)]
    bots = [
        Boat(x=660, y=360),
        Boat(x=680, y=360),
        Boat(x=700, y=360),
        Boat(x=720, y=360),
    ]

    finish_times = {"P": None, "B1": None, "B2": None, "B3": None, "B4": None}

    for i in range(4):
        update_progress(track, bot_progs[i], bots[i].x, bots[i].y)

    game_over = False
    won = False

    end_sfx_played = False

    # START COUNTDOWN (Stap 3)
    START_COUNTDOWN = 3.0
    start_countdown = START_COUNTDOWN
    race_started = False

    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # seconds
        # Timer loopt pas nadat de race is gestart
        if race_started and (not game_over) and (not won):
            race_timer.update(dt)
            if race_timer.is_done and (not won):
                game_over = True
                if not end_sfx_played:
                    SFX_END.play()
                    end_sfx_played = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False


        # Countdown logica: 3-2-1-GO
        if (not race_started) and (not game_over) and (not won):
            start_countdown -= dt
            if start_countdown <= -0.5:
                race_started = True
                SFX_START.play()


        if (not game_over) and (not won) and race_started:
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
                steer_rate=2.2,   
                return_rate=4.0,  
            )

            if boost_time_left > 0:
                boost_time_left -= dt
                boat.max_speed = BASE_PLAYER_MAX_SPEED * BOOST_FACTOR
            else:
                boat.max_speed = BASE_PLAYER_MAX_SPEED

            boat.update(
                throttle=input_state.throttle,
                brake=input_state.brake,
                steer=input_state.steer,
                dt=dt,
            )

            boat.x = max(0, min(WORLD_W, boat.x))
            boat.y = max(0, min(WORLD_H, boat.y))

            if boost_pickups:
                hit_index = None
                hit_r2 = (BOAT_RADIUS + PICKUP_RADIUS) ** 2
                for idx, (px, py) in enumerate(boost_pickups):
                    if dist2(boat.x, boat.y, px, py) <= hit_r2:
                        hit_index = idx
                        break

                if hit_index is not None:
                    boost_time_left = BOOST_DURATION
                    # verwijder pickup (eenmalig)
                    boost_pickups.pop(hit_index)

            update_progress(track, player_prog, boat.x, boat.y)

            if player_prog.finished and finish_times["P"] is None:
                finish_times["P"] = race_timer.total_seconds - race_timer.remaining

            # Update bot boats using simple AI
            for i in range(4):
                d = bot_decide(track, bot_progs[i], bots[i].x, bots[i].y, bots[i].angle, bots[i].speed)
                bots[i].update(
                    throttle=min(d.throttle, 0.55), 
                    brake=d.brake,
                    steer=d.steer,
                    dt=dt
                )

                bots[i].x = max(0, min(WORLD_W, bots[i].x))
                bots[i].y = max(0, min(WORLD_H, bots[i].y))

                update_progress(track, bot_progs[i], bots[i].x, bots[i].y)
                bot_id = f"B{i+1}"
                if bot_progs[i].finished and finish_times[bot_id] is None:
                    finish_times[bot_id] = race_timer.total_seconds - race_timer.remaining


            separate_bots(bots)

            for b in bots:
                b.x = max(0, min(WORLD_W, b.x))
                b.y = max(0, min(WORLD_H, b.y))          

        else:
            if keys[pygame.K_r]:
                bots = [
                    Boat(x=660, y=360),
                    Boat(x=680, y=360),
                    Boat(x=700, y=360),
                    Boat(x=720, y=360),
                ]

                player_prog = RacerProgress()
                bot_progs = [RacerProgress() for _ in range(4)]

                for i in range(4):
                    update_progress(track, bot_progs[i], bots[i].x, bots[i].y)
                    
                boat.x, boat.y = 640, 360
                boat.angle = 0.0
                boat.speed = 0.0
                input_state = BoatInputState()
                race_timer = CountdownTimer(total_seconds=120)
                finish_times = {"P": None, "B1": None, "B2": None, "B3": None, "B4": None}
                game_over = False
                won = False
                end_sfx_played = False 

                start_countdown = START_COUNTDOWN
                race_started = False

                boost_time_left = 0.0
                boat.max_speed = BASE_PLAYER_MAX_SPEED

                # pickups opnieuw zetten bij restart
                boost_pickups = [
                    (1400, 600),
                    (900, 1500),
                    (640, 2000),
                ]

        screen.fill((20, 20, 25))
        timer_text = font.render(f"Time: {race_timer.as_text()}", True, (230, 230, 230))
        screen.blit(timer_text, (20, 50))

        cam_x = boat.x - 1280 / 2
        cam_y = boat.y - 720 / 2

        # World grid
        for cp in track.checkpoints:
            sx = cp.x - cam_x
            sy = cp.y - cam_y
            pygame.draw.circle(screen, (200, 200, 80), (sx, sy), cp.radius, 2)
        grid = 200
        for x in range(0, WORLD_W + 1, grid):
            sx = x - cam_x
            if 0 <= sx <= 1280:
                pygame.draw.line(screen, (35, 35, 45), (sx, -cam_y), (sx, WORLD_H - cam_y))
        for y in range(0, WORLD_H + 1, grid):
            sy = y - cam_y
            if 0 <= sy <= 720:
                pygame.draw.line(screen, (35, 35, 45), (-cam_x, sy), (WORLD_W - cam_x, sy))
        
        for (px, py) in boost_pickups:
            pygame.draw.circle(screen, (0, 200, 255), (px - cam_x, py - cam_y), PICKUP_RADIUS)
            pygame.draw.circle(screen, (255, 255, 255), (px - cam_x, py - cam_y), PICKUP_RADIUS, 2)

        if DEBUG:
            debug = f"world=({boat.x:.0f},{boat.y:.0f}) speed=... throttle={input_state.throttle:.2f} steer={input_state.steer:.2f}"
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
        for b in bots:
            pygame.draw.circle(screen, (255, 120, 120), (b.x - cam_x, b.y - cam_y), 10)
        if DEBUG:
            for i, b in enumerate(bots):
                label = font.render(f"B{i+1}:{bot_progs[i].next_cp_index}", True, (255, 180, 180))
                screen.blit(label, (b.x - cam_x + 12, b.y - cam_y - 12))

        racers = [
            RacerSnapshot("P", boat.x, boat.y, player_prog, finish_times["P"]),
        ]
        for i in range(4):
            bot_id = f"B{i+1}"
            racers.append(RacerSnapshot(bot_id, bots[i].x, bots[i].y, bot_progs[i], finish_times[bot_id]))

        pos = position_of(track, racers, "P")

        if (not game_over) and (not won):
            if player_prog.finished and pos == 1 and (not race_timer.is_done):
                won = True
                if not end_sfx_played:
                    SFX_END.play()
                    end_sfx_played = True

        pos_label = f"{pos}e"

        pos_text = font.render(f"Positie: {pos_label}", True, (230, 230, 230))
        screen.blit(pos_text, (1280 - pos_text.get_width() - 20, 20))

        if boost_time_left > 0:
            boost_text = font.render("BOOST!", True, (0, 200, 255))
            screen.blit(boost_text, (1280 - boost_text.get_width() - 20, 50))

        # Toon startcountdown in het midden van het scherm
        if (not race_started) and (not game_over) and (not won):
            if start_countdown > 2:
                txt = "3"
            elif start_countdown > 1:
                txt = "2"
            elif start_countdown > 0:
                txt = "1"
            else:
                txt = "GO!"

            big_font = pygame.font.SysFont(None, 96)
            t = big_font.render(txt, True, (255, 255, 255))
            screen.blit(t, ((1280 - t.get_width()) // 2, (720 - t.get_height()) // 2))


        if DEBUG:
            dbg = font.render(
                f"player_cp={player_prog.next_cp_index} finished={player_prog.finished}",
                True,
                (230, 230, 230),
            )
            screen.blit(dbg, (20, 100))

        if game_over:
            overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            big = pygame.font.SysFont(None, 72)
            msg = big.render("Game over, dude", True, (255, 255, 255))
            sub = font.render("Press R to restart or ESC to quit", True, (230, 230, 230))
            screen.blit(msg, (1280/2 - msg.get_width()/2, 720/2 - 60))
            screen.blit(sub, (1280/2 - sub.get_width()/2, 720/2 + 10))

        if won:
            overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            big = pygame.font.SysFont(None, 72)
            msg = big.render("YOU WIN!", True, (255, 255, 255))
            sub = font.render("Press R to restart or ESC to quit", True, (230, 230, 230))
            screen.blit(msg, (1280/2 - msg.get_width()/2, 720/2 - 60))
            screen.blit(sub, (1280/2 - sub.get_width()/2, 720/2 + 10))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

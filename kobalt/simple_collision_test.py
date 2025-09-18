import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame
from widgets import CollideRect, Player

# Disable sound for headless testing
os.environ['SDL_AUDIODRIVER'] = 'dummy'

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SIZE = (800, 600)
FPS = 60


def main():
    pygame.init()
    pygame.mouse.set_visible(False)

    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    running = True

    w, h = screen.get_size()

    # player
    player_w = 40
    player_h = 40
    player = Player(
        width=player_w,
        height=player_h,
        color=BLUE,
        fps=FPS,
        pos=(w // 2 - player_w // 2, h - player_h - 100),
        speed=200,
        screen_size=SIZE,
    )

    # platforms - simple colored rectangles
    platform_1_w = 200
    platform_1_h = 30
    platform_1 = CollideRect(
        screen_size=SIZE,
        x=100,
        y=SIZE[1] - platform_1_h - 80,
        width=platform_1_w,
        height=platform_1_h,
        color=GREEN,
    )

    platform_2_w = 150
    platform_2_h = 30
    platform_2 = CollideRect(
        screen_size=SIZE,
        x=400,
        y=SIZE[1] - platform_2_h - 150,
        width=platform_2_w,
        height=platform_2_h,
        color=RED,
    )

    platforms = [platform_1, platform_2]
    widgets = [player] + platforms

    frame_count = 0
    max_frames = 300  # Run for 5 seconds at 60 FPS

    print("Starting collision test...")
    print("Use A/D to move, SPACE to jump, SHIFT to crouch")
    print("Running for 5 seconds...")

    while running and frame_count < max_frames:
        frame_count += 1
        
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                player.handle_event(event)

        # drawing / updating
        dt = clock.tick(FPS) / 1000
        screen.fill((50, 50, 50))  # Dark gray background

        # player
        old_pos = (player.x, player.y)
        player.update(dt, screen)
        
        # Test collision resolution
        if player.is_moving():
            for platform in platforms:
                if player.rect.colliderect(platform.rect):
                    print(f"Collision detected at frame {frame_count}: player at ({player.x:.1f}, {player.y:.1f})")
                    player.resolve_collisions([platform])
                    print(f"Collision resolved: player moved to ({player.x:.1f}, {player.y:.1f})")

        player.draw(screen)

        # platforms
        for platform in platforms:
            platform.update(screen)
            platform.draw(screen)

        # display update
        pygame.display.flip()

    pygame.quit()
    print("Test completed successfully!")


if __name__ == "__main__":
    main()
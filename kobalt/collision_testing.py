import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame
from widgets import CollideRect, Player, Trail

from libs.winmode import PygameWindowController, WindowStates

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SIZE = (1280, 720)
FPS = 60


def main():
    pygame.init()
    pygame.mouse.set_visible(False)

    controller = PygameWindowController(SIZE, WindowStates.WINDOWED_STATELESS)
    screen = controller.get_screen()
    clock = pygame.time.Clock()
    running = True

    w, h = screen.get_size()

    # player
    # player_image = pygame.image.load("kobalt/assets/neon.png").convert_alpha()
    player_image = None  # Use solid color instead
    player_w = 80
    player_h = 80
    player = Player(
        width=player_w,
        height=player_h,
        color=BLUE,
        image=player_image,
        fps=FPS,
        pos=(w // 2 - player_w // 2, h - player_h),
        speed=200,
        screen_size=SIZE,
    )

    # trail
    trail = Trail(
        SIZE,
        color=(17, 61, 158),
        lifetime=2000,
        max_alpha=100,
    )

    # platforms
    # platform_image = pygame.image.load("kobalt/assets/platform.png").convert_alpha()
    platform_image = None  # Use solid color instead
    platform_1_w = 200
    platform_1_h = 100
    platform_1 = CollideRect(
        screen_size=SIZE,
        x=platform_1_w,
        y=SIZE[1] - platform_1_h + 20,
        width=platform_1_w,
        height=platform_1_h,
        color=(GREEN),
        image=platform_image,
    )

    platform_2_w = 70
    platform_2_h = 200
    platform_2 = CollideRect(  # bottom right
        screen_size=SIZE,
        x=100,
        y=SIZE[1] - platform_2_h - 50,
        width=platform_2_w,
        height=platform_2_h,
        color=(RED),
        image=platform_image,
    )

    platforms = [platform_1, platform_2]

    widgets = [player] + platforms

    while running:
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_F11:
                    controller.set_mode(
                        WindowStates.WINDOWED_STATELESS
                        if controller.is_current_fullscreen_mode()
                        else WindowStates.FULLSCREEN
                    )
                    w, h = screen.get_size()
                    for widget in widgets:
                        widget.update_position((w, h))

                player.handle_event(event)

        # drawing / updating
        dt = clock.tick(FPS) / 1000
        screen = controller.get_screen()
        screen.fill((0, 0, 0))

        # tracker trail
        trail.width = player.speed * dt + 2
        trail.height = player.speed * dt + 2
        trail.update(player.x + player.width // 2, player.y + player.height // 2)
        trail.draw(screen)

        # player
        player.update(dt, screen)
        player.draw(screen)

        # platform
        for platform in platforms:
            platform.update(screen)
            platform.draw(screen)

        # collisions
        if player.is_moving():
            player.resolve_collisions(platforms)

        # display update
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame
from widgets import Player, Trail, Widget

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

    # trail
    trail = Trail(
        SIZE,
        color=(17, 61, 158),
        lifetime=2000,
        max_alpha=100,
    )

    # platforms - calculated parkour
    platform_image = pygame.image.load("kobalt/assets/platform.png").convert_alpha()
    platforms = []

    base_y = SIZE[1] - 50
    base_x = 300
    platform_w = 120
    platform_h = 30
    x_gap = 180  # horizontal distance between platforms
    y_gap = 20  # vertical distance (must be <= h_max)

    for i in range(5):
        plat = Widget(
            screen_size=SIZE,
            x=base_x + i * x_gap,
            y=base_y - i * y_gap,
            width=platform_w,
            height=platform_h,
            color=GREEN if i < 4 else BLUE,  # last platform is goal
            image=None,
        )
        platforms.append(plat)

    # player
    player_image = pygame.image.load("kobalt/assets/player.png").convert_alpha()
    player_w = 40
    player_h = 40
    player = Player(
        screen_size=SIZE,
        x=player_w,
        y=h - player_h,
        width=player_w,
        height=player_h,
        color=BLUE,
        image=player_image,
    )

    widgets = [player] + platforms

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
        trail.width, trail.height = player.speed, player.speed
        trail.draw(screen, player.x + player.width // 2, player.y + player.height // 2)

        # player
        player.draw(screen, dt)

        # # platforms
        # for platform in platforms:d
        #     platform.draw(screen, dt)

        # display update
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()

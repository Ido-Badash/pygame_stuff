import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame
from widgets import Player

from libs.winmode import PygameWindowController, WindowStates

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
    player_w = 40
    player_h = 40
    player = Player(
        player_w,
        player_h,
        color=(14, 58, 154),
        pos=(w // 2 - player_w // 2, h - player_h),
        speed=200,
        ground_reset_time_ms=FPS,
    )

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
                    player.update_position((w, h))

                player.handle_event(event)

        # drawing / updating
        dt = clock.tick(FPS) / 1000
        screen = controller.get_screen()
        screen.fill((0, 0, 0))

        # player
        player.update(dt, screen)
        player.draw(screen)

        # display update
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()

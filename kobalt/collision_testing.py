import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame
from widgets import CollideRect, Player

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
    player_w = 40
    player_h = 40
    player = Player(
        SIZE,
        player_w,
        player_h,
        color=BLUE,
        fps=FPS,
        pos=(w // 2 - player_w // 2, h - player_h),
        speed=200,
    )

    # wall
    wall_1_w = 50
    wall_1_h = 100
    wall_1 = CollideRect(
        SIZE, wall_1_w, SIZE[1] - wall_1_h - 10, wall_1_w, wall_1_h, (GREEN)
    )

    wall_2_w = 200
    wall_2_h = 30
    wall_2 = CollideRect(  # bottom right
        SIZE,
        SIZE[0] - wall_2_w - 10,
        SIZE[1] - wall_2_h - 10,
        wall_2_w,
        wall_2_h,
        (RED),
    )

    walls = [wall_1, wall_2]

    widgets = [player] + walls

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

        # player
        player.update(dt, screen)
        player.draw(screen)

        # wall
        for wall in walls:
            wall.update(screen)
            wall.draw(screen)

        # collisions
        if player.is_moving():
            player.resolve_collisions(walls)

        # display update
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()

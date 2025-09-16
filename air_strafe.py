import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame

from kobalt import Player, Trail
from libs.winmode import PygameWindowController, WindowStates

SIZE = (1280, 720)
FPS = 60


def main():
    pygame.init()
    pygame.mouse.set_visible(False)

    FONT = pygame.font.SysFont("Courier", 50)

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

    # tracker trail
    player_trail = Trail(color=(255, 0, 0), lifetime=3000, max_alpha=100)

    while running:
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

        dt = clock.tick(FPS) / 1000
        screen = controller.get_screen()
        w, h = screen.get_size()
        screen.fill((0, 0, 0))

        # tracker trail
        player_trail.width = player.speed * dt
        player_trail.height = player.speed * dt
        player_trail.update(player.x + player.width // 2, player.y + player.height // 2)
        player_trail.draw(screen)

        # player
        player.update(dt, screen)
        player.draw(screen)

        # Draw speed value in top left, yellow
        speed = min(int(player.speed), player.max_air_strafe_speed)
        speed_label_surf = FONT.render("Speed: ", True, (255, 255, 255))
        speed_value_surf = FONT.render(f"{speed:.2f}", True, (0, 255, 0))
        speed_total_w = speed_label_surf.get_width() + speed_value_surf.get_width()
        speed_total_h = max(
            speed_label_surf.get_height(), speed_value_surf.get_height()
        )
        speed_info_surf = pygame.Surface(
            (speed_total_w, speed_total_h), pygame.SRCALPHA
        )
        speed_info_surf.set_alpha(175)
        speed_info_surf.blit(speed_label_surf, (0, 0))
        speed_info_surf.blit(speed_value_surf, (speed_label_surf.get_width(), 0))
        screen.blit(
            speed_info_surf,
            (
                w // 2 - speed_info_surf.get_width() // 2,
                h // 2 - speed_info_surf.get_height() // 2,
            ),
        )

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame
from analysis.plot_speed import plot_speed
from widgets import Player, Trail

from libs.winmode import PygameWindowController, WindowStates

# colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

SIZE = (1280, 720)
FPS = 60


def main():
    pygame.init()
    pygame.mouse.set_visible(False)

    FONT = pygame.font.SysFont("Courier", 30)

    controller = PygameWindowController(SIZE, WindowStates.WINDOWED_STATELESS)
    screen = controller.get_screen()
    clock = pygame.time.Clock()
    running = True

    w, h = screen.get_size()

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

    # tracker trail
    trail = Trail(
        SIZE,
        color=(17, 61, 158),
        lifetime=2000,
        max_alpha=100,
    )

    # keybinds and state display setup
    keybinds = [
        ("P", "Toggle Air Strafing"),
        ("F11", "Fullscreen"),
        ("ESC", "Quit"),
        ("SPACE", "Jump"),
        ("A/D", "Move Left/Right"),
    ]

    def get_state_lines():
        return [
            ("Air Strafing:", player.air_strafe),
            ("On Ground:", player.on_ground),
            ("Speed:", round(player.speed, 1)),
        ]

    speeds = []  # for plotting speed over time

    while running:
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_p:
                    player.air_strafe = not player.air_strafe
                    trail.set_color(GREEN if player.air_strafe else RED)
                if event.key == pygame.K_F11:
                    controller.set_mode(
                        WindowStates.WINDOWED_STATELESS
                        if controller.is_current_fullscreen_mode()
                        else WindowStates.FULLSCREEN
                    )
                    w, h = screen.get_size()
                    player.update_position((w, h))
                # pass only key events to the player
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
        speeds.append(float(player.speed))

        # Draw keybinds in top right, key in yellow, rest in gray
        y_offset = 10
        for key, desc in keybinds:
            key_surf = FONT.render(key, True, (255, 255, 0))
            desc_surf = FONT.render(f": {desc}", True, (200, 200, 200))
            x = screen.get_width() - (key_surf.get_width() + desc_surf.get_width()) - 10
            screen.blit(key_surf, (x, y_offset))
            screen.blit(desc_surf, (x + key_surf.get_width(), y_offset))
            y_offset += key_surf.get_height() + 2

        # Draw state values in top left, green/red for bools, yellow for speed
        y_offset = 10
        for label, value in get_state_lines():
            if isinstance(value, bool):
                label = label.strip(":")
                color = (0, 255, 0) if value else (255, 0, 0)
                val_text = "None"
                if label in ["Air Strafing", "Auto Jump"]:
                    val_text = "ON" if value else "OFF"
                elif label == "Strafing":
                    val_text = "YES" if player.air_strafe else "DISABLED"
                else:
                    val_text = "YES" if value else "NO"
                val_surf = FONT.render(val_text, True, color)
            elif label == "Speed":
                color = (255, 255, 0)
                val_surf = FONT.render(f"{value:.2f}", True, color)
            else:
                color = (255, 255, 0)
                val_surf = FONT.render(str(value), True, color)
            label_surf = FONT.render(label, True, (255, 255, 255))
            screen.blit(label_surf, (10, y_offset))
            screen.blit(val_surf, (10 + label_surf.get_width() + 5, y_offset))
            y_offset += label_surf.get_height() + 2

        # display update
        pygame.display.update()

    pygame.quit()

    # plot speeds after exiting the game loop
    try:
        plot_speed(speeds, title="Player Speed over Frames", show=True)
    except Exception as e:
        print(f"Plot skipped: {e}")


if __name__ == "__main__":
    main()

import pygame

from .widget import Widget


class Trail(Widget):
    def __init__(
        self,
        screen_size,
        color=(0, 0, 255),
        width=1,
        height=1,
        lifetime=3000,
        max_alpha=255,
        min_alpha=0,
    ):
        super().__init__(screen_size, 0, 0, width, height, color)
        self.lifetime = lifetime  # ms
        self.max_alpha = max_alpha
        self.min_alpha = min_alpha
        self.tracks = []  # (x, y, timestamp)

    def update_tracks(self, x, y):
        now = pygame.time.get_ticks()
        # stores all current params with each track
        self.tracks.append(
            {
                "x": x,
                "y": y,
                "t": now,
                "color": self.color,
                "width": self.width,
                "height": self.height,
                "lifetime": self.lifetime,
                "max_alpha": self.max_alpha,
                "min_alpha": self.min_alpha,
            }
        )
        # remove old tracks (using each track lifetime)
        self.tracks = [
            track for track in self.tracks if now - track["t"] < track["lifetime"]
        ]

    def draw(self, surf: pygame.Surface, x, y):
        self.update_tracks(x, y)
        now = pygame.time.get_ticks()
        for track in self.tracks:
            age = now - track["t"]
            # start at max_alpha and fade to min_alpha as age -> lifetime
            alpha = max(
                track["min_alpha"],
                track["max_alpha"]
                - int(track["max_alpha"] * (age / track["lifetime"])),
            )  # max - max * (age / lifetime) as (age / lifetime) starts at 1 -> min_alpha
            s = pygame.Surface((track["width"], track["height"]), pygame.SRCALPHA)
            s.fill((*track["color"], alpha))
            surf.blit(s, (track["x"], track["y"]))

    def handle_event(self, event):
        pass

    def set_color(self, color):
        super().set_color(color)

import pygame

from .widget import Widget


class CollideRect(Widget):
    """Used for rect collision between two `CollideRect` or more"""

    def __init__(self, screen_size, x, y, width, height, color):
        super().__init__(screen_size, x, y, width, height, color)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def update(self, surface):
        super().update(surface)
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.width = self.width
        self.rect.height = self.height

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    def handle_event(self, event):
        pass

    def resolve_collisions(self, colliders: list["CollideRect"]):
        """Move self out of any intersecting collider."""
        for c in colliders:
            if self is c:
                continue
            if self.rect.colliderect(c.rect):
                self.no_entry_collision(self.rect, c.rect)

    @staticmethod
    def no_entry_collision(rect1: pygame.Rect, rect2: pygame.Rect):
        """Prevents an object from entering another object, pushing it out on the closest side."""
        pass

import pygame

from .widget import Widget


class CollideRect(Widget):
    """Used for rect collision between two `CollideRect` or more"""

    def __init__(self, screen_size, x, y, width, height, color, image=None):
        super().__init__(screen_size, x, y, width, height, color, image)

    def update(self, surface):
        super().update(surface)
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.width = self.width
        self.rect.height = self.height

    def draw(self, surface: pygame.Surface):
        if self.image:
            img = pygame.transform.scale(self.image, (self.width, self.height))
            surface.blit(img, (self.x, self.y))
        else:
            pygame.draw.rect(surface, self.color, self.rect)

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

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
                # Create a temporary rect to calculate the resolution
                temp_rect = pygame.Rect(self.x, self.y, self.width, self.height)
                self.no_entry_collision(temp_rect, c.rect)
                # Apply the resolved position back to self
                self.x = temp_rect.x
                self.y = temp_rect.y

    @staticmethod
    def no_entry_collision(rect1: pygame.Rect, rect2: pygame.Rect):
        """Prevents an object from entering another object, pushing it out on the closest side."""
        if not rect1.colliderect(rect2):
            return
        
        # Calculate overlaps on each side
        overlap_left = rect2.right - rect1.left
        overlap_right = rect1.right - rect2.left
        overlap_top = rect2.bottom - rect1.top
        overlap_bottom = rect1.bottom - rect2.top
        
        # Find the smallest overlap (closest side)
        min_overlap_x = min(overlap_left, overlap_right)
        min_overlap_y = min(overlap_top, overlap_bottom)
        
        if min_overlap_x < min_overlap_y:
            # Resolve horizontally
            if overlap_left < overlap_right:
                # Push rect1 to the left
                rect1.x = rect2.left - rect1.width
            else:
                # Push rect1 to the right
                rect1.x = rect2.right
        else:
            # Resolve vertically
            if overlap_top < overlap_bottom:
                # Push rect1 up
                rect1.y = rect2.top - rect1.height
            else:
                # Push rect1 down
                rect1.y = rect2.bottom

import pygame


class Widget:
    def __init__(
        self,
        screen_size=(1280, 720),
        x=0,
        y=0,
        width=1,
        height=1,
        color=(255, 255, 255),
        image=None,
    ):
        self.screen_size = screen_size
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self.color = color
        self.image = image
        # position ratios
        self.ratio_x = (self.x + self.width) / screen_size[0]
        self.ratio_y = (self.y + self.height) / screen_size[1]

    def draw(self, surface: pygame.Surface, dt):
        self._update(dt)

        if self.image:
            img = pygame.transform.scale(self.image, (self.width, self.height))
            surface.blit(img, (self.x, self.y))
        else:
            pygame.draw.rect(surface, self.color, self.rect)

    def _update(self, dt):
        self.update_ratio_from_position()

    def update_position(self, new_screen_size):
        old_rx, old_ry = self.ratio_x, self.ratio_y
        self.screen_size = new_screen_size
        self.x = int(old_rx * new_screen_size[0]) - self.width
        self.y = int(old_ry * new_screen_size[1]) - self.height
        self.update_ratio_from_position()

    def update_ratio_from_position(self) -> None:
        """Update internal screen ratio based on current position."""
        self.ratio_x = (self.x + self.width) / self.screen_size[0]
        self.ratio_y = (self.y + self.height) / self.screen_size[1]

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_size(self, width, height):
        self.width = width
        self.height = height

    def set_color(self, color):
        self.color = color

    def set_image(self, image):
        self.image = image

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.update_ratio_from_position()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.update_ratio_from_position()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        self.update_ratio_from_position()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        self.update_ratio_from_position()

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def check_collision(self, other: "Widget"):
        return self.rect.colliderect(other.rect)

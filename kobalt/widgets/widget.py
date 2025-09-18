from abc import ABC, abstractmethod

import pygame


class Widget(ABC):
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
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.image = image
        # position ratios
        self.ratio_x = (x + width) / screen_size[0]
        self.ratio_y = (y + height) / screen_size[1]

    @abstractmethod
    def update(self, surface):
        self.update_ratio_from_position()

    @abstractmethod
    def draw(self, surface):
        pass

    @abstractmethod
    def handle_event(self, event):
        pass

    def update_position(self, new_screen_size):
        self.screen_size = new_screen_size
        self.x = int(self.ratio_x * new_screen_size[0]) - self.width
        self.y = int(self.ratio_y * new_screen_size[1]) - self.height

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
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

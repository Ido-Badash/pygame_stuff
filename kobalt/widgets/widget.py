from abc import ABC, abstractmethod

import pygame


class Widget(ABC):
    def __init__(self, x=0, y=0, width=1, height=1, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    @abstractmethod
    def update(self, surface):
        pass

    @abstractmethod
    def draw(self, surface):
        pass

    @abstractmethod
    def handle_event(self, event):
        pass

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_size(self, width, height):
        self.width = width
        self.height = height

    def set_color(self, color):
        self.color = color

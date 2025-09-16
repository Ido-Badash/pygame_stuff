from typing import Dict, Tuple

from screeninfo import get_monitors

from .window_states import WindowStates


class WindowController:
    def __init__(
        self,
        mode: int,
        size: Tuple[int, int],
        mode_sizes: Dict[int, Tuple[int, int]] = None,
    ):
        self.mode = mode
        self.mode_sizes = mode_sizes or {}
        self.size = size
        if mode not in self.mode_sizes:
            self.mode_sizes[mode] = size

    # getters
    def get_mode(self) -> int:
        return self.mode

    def get_size(self) -> Tuple[int, int]:
        return self.mode_sizes.get(self.mode, self.size)

    # setters
    def set_mode(self, new_mode: int):
        self.mode = new_mode
        if new_mode not in self.mode_sizes:
            self.mode_sizes[new_mode] = self.size

    def set_size(self, new_size: Tuple[int, int]):
        self.size = new_size
        self.mode_sizes[self.mode] = new_size

    def set_mode_size(self, mode: int, size: Tuple[int, int]):
        self.mode_sizes[mode] = size

    def mode_to_flag(self) -> int:
        raise NotImplementedError("mode_to_flag should be implemented in a subclass")

    def is_current_fullscreen_mode(self):
        return self.is_fullscreen_mode(self.mode)

    # properties
    @property
    def width(self) -> int:
        return self.size[0]

    @property
    def height(self) -> int:
        return self.size[1]

    # static methods
    @staticmethod
    def is_fullscreen_mode(mode: int) -> bool:
        return mode in WindowStates.fullscreen_states

    @staticmethod
    def get_user_win_size() -> Tuple[int, int]:
        primary = next((m for m in get_monitors() if m.is_primary), None)
        return (primary.width, primary.height)

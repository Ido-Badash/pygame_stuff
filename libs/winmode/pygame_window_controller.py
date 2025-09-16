import os
from typing import Dict, List, Tuple

import pygame

from .window_controller import WindowController
from .window_states import WindowStates

KEY_MODE_TYPE = Dict[Tuple[int, int], int]
DEFAULT_KEYS = [
    (pygame.KMOD_CTRL, pygame.K_1),
    (pygame.KMOD_CTRL, pygame.K_2),
    (pygame.KMOD_CTRL, pygame.K_3),
    (pygame.KMOD_CTRL, pygame.K_4),
    (pygame.KMOD_CTRL, pygame.K_5),
]
DEFAULT_KEY_MODE_MAP: KEY_MODE_TYPE = dict(
    zip(
        DEFAULT_KEYS,
        WindowStates.all_states,
    )
)

FLAGS_VALUES = [
    pygame.RESIZABLE,
    0,
    pygame.NOFRAME,
    pygame.NOFRAME,
    pygame.FULLSCREEN,
    0,
]

MODE_FLAG_MAP = dict(zip(WindowStates.all_states_w_none, FLAGS_VALUES))


class PygameWindowController(WindowController):
    def __init__(
        self,
        size: tuple[int, int],
        mode: int = WindowStates.WINDOWED_STATELESS,
        flags: int = 0,
        depth: int = 0,
        display: int = 0,
        vsync: int = 0,
        mode_sizes: dict = None,
        key_mode_map: KEY_MODE_TYPE = None,
    ):
        super().__init__(mode, size, mode_sizes)
        self.flags = flags
        self.depth = depth
        self.display = display
        self.vsync = vsync
        self.key_mode_map = key_mode_map or DEFAULT_KEY_MODE_MAP.copy()
        self._screen = self._create_screen()

    def handle_event(self, event: pygame.event.Event) -> bool:
        mode = self.get_mode_for_event(event)
        if self.set_mode(mode):
            return True
        return False

    def mode_to_flag(self) -> int:
        return MODE_FLAG_MAP.get(self.mode, 0)

    def get_flag(self) -> int:
        return self.flags | self.mode_to_flag()

    def get_mode_for_event(self, event: pygame.event.Event) -> int | None:
        key = event.key if hasattr(event, "key") else None
        mods = event.mod if hasattr(event, "mod") else 0

        # Try exact match first
        result = self.key_mode_map.get((mods, key))
        if result is not None:
            return result

        # Try with just the CTRL bit
        if mods & pygame.KMOD_CTRL:
            result = self.key_mode_map.get((pygame.KMOD_CTRL, key))
            if result is not None:
                return result

        # Fallback to no modifier
        return self.key_mode_map.get((0, key))

    def get_screen(self) -> pygame.Surface:
        return self._screen

    def set_size(self, width: int, height: int):
        super().set_size((width, height))
        self._create_screen()

    def set_mode(self, mode: int) -> bool:
        prev_mode = self.get_mode()
        if mode is not None and mode != prev_mode:
            # if leaving fullscreen, go to WINDOWED_FULLSCREEN first to avoid GUI bugs
            if (
                prev_mode == WindowStates.FULLSCREEN
                and not mode in WindowStates.fullscreen_states
            ):
                super().set_mode(WindowStates.WINDOWED_FULLSCREEN)
                super().set_mode_size(
                    WindowStates.WINDOWED_FULLSCREEN,
                    WindowController.get_user_win_size(),
                )
                self._create_screen()
                pygame.event.pump()
            super().set_mode(mode)

            # for fullscreen modes use monitor size
            if mode in WindowStates.fullscreen_states:
                super().set_mode_size(mode, WindowController.get_user_win_size())
            self._create_screen()
            return True  # mode was changed
        return False  # mode was not changed

    def set_screen(self, new_screen):
        self._screen = new_screen

    def _create_screen(self) -> pygame.Surface:
        size = self.get_size()
        if self.mode in WindowStates.fullscreen_states:
            # force fullscreen window at (0, 0)
            os.environ["SDL_VIDEO_CENTERED"] = "0"
            os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"
            size = WindowController.get_user_win_size()

        flags = self.flags | self.mode_to_flag()
        screen = pygame.display.set_mode(
            size, flags, self.depth, self.display, self.vsync
        )
        self._screen = screen
        return screen

    @staticmethod
    def custom_key_mode_map_builder(
        keys: List[int],
        modes: List[str],
        mods: List[int] = None,
    ) -> KEY_MODE_TYPE:
        mods = mods or [0] * len(keys)
        if not (len(keys) == len(modes) == len(mods)):
            raise ValueError("keys, modes, and mods must all have the same length")
        return {(mod, key): mode for key, mode, mod in zip(keys, modes, mods)}

    @staticmethod
    def simple_key_mode_map_builder(
        keys: List[int], modes: List[str] = WindowStates.all_states, mod: int = 0
    ) -> KEY_MODE_TYPE:
        return PygameWindowController.custom_key_mode_map_builder(
            keys,
            modes,
            [mod] * len(keys),
        )

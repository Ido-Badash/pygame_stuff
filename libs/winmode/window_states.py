class WindowStates:
    # main states
    WINDOWED = 0
    """Standard windowed mode with resizable borders and window decorations."""

    WINDOWED_STATELESS = 1
    """Windowed mode with fixed size and window decorations; resizing is disabled."""

    BORDERLESS = 2
    """Fixed-size window without borders or window decorations."""

    WINDOWED_FULLSCREEN = 3
    """Borderless window that covers the entire monitor, matching its resolution."""

    FULLSCREEN = 4
    """Exclusive fullscreen mode, taking over the entire display output."""

    # other states
    DEFAULT = WINDOWED_STATELESS
    NONE = -1

    # state codes
    all_states = [
        WINDOWED,
        WINDOWED_STATELESS,
        BORDERLESS,
        WINDOWED_FULLSCREEN,
        FULLSCREEN,
    ]

    all_states_w_none = all_states + [NONE]

    fullscreen_states = [FULLSCREEN, WINDOWED_FULLSCREEN]

    non_fullscreen_states = [WINDOWED, WINDOWED_STATELESS, BORDERLESS]

    names = {
        WINDOWED: "Windowed",
        WINDOWED_STATELESS: "Windowed Stateless",
        BORDERLESS: "Borderless",
        WINDOWED_FULLSCREEN: "Windowed Fullscreen",
        FULLSCREEN: "Fullscreen",
        NONE: "None",
    }

    @classmethod
    def get_name(cls, state: int) -> str:
        """Get the human-readable name for a given window state code."""
        return cls.names.get(state, "Unknown")

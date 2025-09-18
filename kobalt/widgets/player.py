import pygame

from .collide_rect import CollideRect
from .widget import Widget


class Player(CollideRect):
    """
    A controllable player character with movement, jumping, crouching,
    and optional air-strafing physics.

    This implementation uses velocity-based movement with horizontal velocity (vx)
    and vertical velocity (vy) for smooth physics-based character control.

    Parameters
    ----------
    width : int
        Width of the player sprite.
    height : int
        Height of the player sprite.
    color : tuple[int, int, int], optional
        RGB color of the player. Defaults to blue (0, 0, 255).
    image : pygame.Surface, optional
        Image sprite to use instead of solid color. Defaults to None.
    fps : int, optional
        Frames per second for timing calculations. Defaults to 60.
    pos : tuple[int, int], optional
        Initial (x, y) position. Defaults to (0, 0).
    speed : float, optional
        Base horizontal speed. Defaults to 200.
    gravity : float, optional
        Gravitational acceleration. Defaults to 0.5.
    disable_user_controls : bool, optional
        Disable all keyboard input. Defaults to False.
    enable_crouching : bool, optional
        Enable or disable crouching. Defaults to True.
    enable_air_strafing : bool, optional
        Enable or disable air-strafing. Defaults to True.
    auto_jump : bool, optional
        Automatically jump upon landing. Defaults to False.
    jump_height : float, optional
        Vertical velocity for jumps. Defaults to 8.
    air_strafe_power : float, optional
        Acceleration rate while strafing in the air. 
        Defaults to speed/40 for consistent scaling.
    max_air_strafe_speed : float, optional
        Maximum air-strafe speed. Defaults to 1000.
    air_strafe_restore_rate : float, optional
        Rate at which the air-strafe bonus decays. Defaults to 1.
    ground_reset_time_ms : int, optional
        Time on ground before resetting air-strafe bonus (ms). Defaults to fps.
    air_strafe_bonus_decay_threshold : float, optional
        Threshold below which bonus resets to 0. Defaults to 0.001.
    air_strafe_bonus_dt_scale : float, optional
        Scaling factor for delta time adjustments. Defaults to fps.
    crouch_height_factor : float, optional
        Factor to reduce height when crouching. Defaults to 1.2.
    crouching_speed : float, optional
        Movement speed while crouching. Defaults to 50% of base speed.
    crouching_gravity_pull : float, optional
        Reduced gravity effect while crouching. Defaults to 1.0.
    screen_size : tuple[int, int], optional
        Dimensions of the screen (width, height). Defaults to (1280, 720).

    Key Features
    -----------
    - Velocity-based movement using vx (horizontal) and vy (vertical) velocities
    - Air-strafing that only increases when moving in exactly one direction
    - Collision detection and resolution
    - Crouching mechanics with height adjustment
    - Configurable physics parameters that scale with base speed
    """

    def __init__(
        self,
        width: int,
        height: int,
        color: tuple[int, int, int] = (0, 0, 255),
        image: pygame.Surface | None = None,
        fps: int = 60,
        pos: tuple[int, int] = (0, 0),
        speed: float = 200,
        gravity: float = 0.5,
        disable_user_controls: bool = False,
        enable_crouching: bool = True,
        enable_air_strafing: bool = True,
        auto_jump: bool = False,
        jump_height: float | None = None,
        air_strafe_power: float | None = None,
        max_air_strafe_speed: float | None = None,
        air_strafe_restore_rate: float | None = None,
        ground_reset_time_ms: int | None = None,
        air_strafe_bonus_decay_threshold: float | None = None,
        air_strafe_bonus_dt_scale: float | None = None,
        crouch_height_factor: float | None = None,
        crouching_speed: float | None = None,
        crouching_gravity_pull: float | None = None,
        screen_size: tuple[int, int] = (1280, 720),
    ):
        x, y = pos
        super().__init__(screen_size, x, y, width, height, color, image)
        self.fps = fps
        self.speed = speed
        self.original_speed = speed
        self.screen_size = screen_size

        # physics
        self.gravity = gravity
        self.original_gravity = gravity
        self.jump_height = jump_height if jump_height is not None else 8
        self.on_ground = False
        self.jump_vy = 0
        self.auto_jump = auto_jump

        # velocity
        self.vx = 0.0
        self.vy = 0.0

        # air strafing
        self.enable_air_strafing = enable_air_strafing
        self.air_strafe_power = (
            air_strafe_power if air_strafe_power is not None else speed / 40
        )
        self.max_air_strafe_speed = (
            max_air_strafe_speed if max_air_strafe_speed is not None else 1000
        )
        self.air_strafe_restore_rate = (
            air_strafe_restore_rate if air_strafe_restore_rate is not None else 1
        )
        self.air_strafe_bonus_decay_threshold = (
            air_strafe_bonus_decay_threshold
            if air_strafe_bonus_decay_threshold is not None
            else 0.001
        )
        self.air_strafe_bonus_dt_scale = (
            air_strafe_bonus_dt_scale if air_strafe_bonus_dt_scale is not None else fps
        )
        self.ground_reset_time_ms = (
            ground_reset_time_ms if ground_reset_time_ms is not None else fps
        )

        self.air_strafe_bonus = 0.0
        self.strafing = False
        self.collision = False
        self.ground_time = 0

        # crouching
        self.enable_crouching = enable_crouching
        self.crouching = False
        self.crouch_height_factor = (
            crouch_height_factor if crouch_height_factor is not None else 1.2
        )
        self.crouching_speed = (
            min(crouching_speed, self.speed)
            if crouching_speed is not None
            else self.speed * 0.5
        )
        self.crouching_gravity_pull = (
            crouching_gravity_pull if crouching_gravity_pull is not None else 1.0
        )
        self.standing_height = height
        self.crouch_height = int(self.standing_height // self.crouch_height_factor)

        # movement flags
        self.moving_right = False
        self.moving_left = False
        self.can_move = True
        self.disable_user_controls = disable_user_controls

    # Update loop ---------------------------------------------------
    def update(self, dt, surf: pygame.Surface):
        """Update player state each frame."""
        super().update(surf)
        size = surf.get_size()

        # --- update logic ---
        keys = pygame.key.get_pressed() if not self.disable_user_controls else None
        self.collision = False

        self.vx = 0.0  # Reset horizontal velocity each frame

        if self.can_move:
            # movement flags
            moving_right = (keys and keys[pygame.K_d]) or self.moving_right
            moving_left = (keys and keys[pygame.K_a]) or self.moving_left

            # crouch input
            if keys and keys[pygame.K_LSHIFT]:
                self.crouching = True
            elif not self.disable_user_controls:
                self.crouching = False
            # If user controls are disabled, keep the current crouching state

            # strafing only in air and when moving right or left (but not both)
            self.strafing = (
                not self.on_ground
                and self.enable_air_strafing
                and ((moving_right and not moving_left) or (moving_left and not moving_right))
            )

            # --- AIR STRAFING (modify air_strafe_bonus) ---
            if self.strafing and not self.collision:
                max_bonus = max(0.0, self.max_air_strafe_speed - self.original_speed)
                self.air_strafe_bonus = min(
                    self.air_strafe_bonus
                    + self.air_strafe_power * dt * self.air_strafe_bonus_dt_scale,
                    max_bonus,
                )
            else:
                self.decay_air_strafe(dt)

            # --- CROUCHING ---
            if self.enable_crouching:
                if self.crouching and self.on_ground:
                    # reduce gravity pull while crouched on ground
                    self.gravity = self.crouching_gravity_pull
                    if self.height != self.crouch_height:
                        bottom = self.y + self.height
                        self.height = self.crouch_height
                        self.y = bottom - self.height
                else:
                    self.gravity = self.original_gravity
                    if self.height != self.standing_height:
                        bottom = self.y + self.height
                        self.height = self.standing_height
                        self.y = bottom - self.height

            # add horizontal movement (after all speed logic)
            if self.crouching and self.on_ground:
                effective_speed = self.crouching_speed
            elif self.crouching and not self.on_ground:
                effective_speed = self.crouching_speed + self.air_strafe_bonus
            else:
                effective_speed = self.original_speed + self.air_strafe_bonus

            if moving_right and not moving_left:
                self.vx = effective_speed
            elif moving_left and not moving_right:
                self.vx = -effective_speed
            else:
                self.vx = 0.0

        # set self.speed for display/state
        if self.crouching and self.on_ground:
            self.speed = self.crouching_speed
        elif self.crouching and not self.on_ground:
            self.speed = self.crouching_speed + self.air_strafe_bonus
        else:
            self.speed = self.original_speed + self.air_strafe_bonus

        # gravity handle (vertical)
        self.jump_vy += self.gravity
        self.vy = self.jump_vy

        # Apply velocities to position
        self.x += self.vx * dt
        self.y += self.vy

        # floor border
        self._floor_border(size)

        # screen walls borders
        self._walls_border(size)

        # ground timer
        if self.on_ground:
            self.ground_time += dt * 1000  # ms
            if self.ground_time > self.ground_reset_time_ms:
                self.air_strafe_bonus -= (
                    self.air_strafe_bonus
                    * self.air_strafe_restore_rate
                    * (dt * self.air_strafe_bonus_dt_scale)
                )
                if self.air_strafe_bonus < self.air_strafe_bonus_decay_threshold:
                    self.air_strafe_bonus = 0.0
        else:
            self.ground_time = 0

        if self.auto_jump and self.on_ground:
            self.jump()

    def draw(self, surf: pygame.Surface) -> None:
        """Render the player to the given surface."""
        if self.image:
            img = pygame.transform.scale(self.image, (self.width, self.height))
            surf.blit(img, (self.x, self.y))
        else:
            pygame.draw.rect(surf, self.color, self.rect)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle keyboard events for jumping."""
        if self.disable_user_controls:
            return
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_SPACE
            and self.on_ground
            and self.can_move
        ):
            self.jump()

    def decay_air_strafe(self, dt: float) -> None:
        """Decay the air strafe bonus by the configured rate."""
        self.air_strafe_bonus -= (
            self.air_strafe_bonus * self.air_strafe_restore_rate * dt
        )
        if self.air_strafe_bonus < self.air_strafe_bonus_decay_threshold:
            self.air_strafe_bonus = 0.0

    def jump(self) -> None:
        """Trigger a jump."""
        self.vy = self.jump_vy = -self.jump_height

    # Private methods ----------------------------------------------
    def _floor_border(self, size: tuple[int, int]) -> None:
        """Handle collision with the floor."""
        if self.y >= size[1] - self.height:
            # hit floor
            self.collision = True
            self.y = size[1] - self.height
            self.jump_vy = 0
            if not self.on_ground:
                self.ground_time = 0  # landed
            self.on_ground = True
        else:
            if self.on_ground:
                # left ground
                self.ground_time = 0
            self.on_ground = False

    def _walls_border(self, size: tuple[int, int]) -> None:
        # left wall
        if self.x < -self.width:
            self.collision = True
            self.x = size[0] - self.width // 2
        # right wall
        if self.x > size[0]:
            self.collision = True
            self.x = -self.width // 2

    # Is -------------------------------------------------------
    def is_air_strafing_enabled(self) -> bool:
        return self.enable_air_strafing

    def is_moving(self) -> bool:
        """Checks if the player is currently moving"""
        return self.vx != 0 or self.vy != 0

    # Toggles -------------------------------------------------------
    def toggle_air_strafing(self) -> None:
        self.enable_air_strafing = not self.enable_air_strafing

    def toggle_auto_jump(self) -> None:
        self.auto_jump = not self.auto_jump

    def toggle_movement(self) -> None:
        if self.can_move:
            self.stop_movement()
        else:
            self.start_movement()

    # Set ----------------------------------------------------
    def set_size(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    # Manual movement -----------------------------------------------
    def move_right(self, moving: bool = True) -> None:
        self.moving_right = moving

    def move_left(self, moving: bool = True) -> None:
        self.moving_left = moving

    def stop_movement(self) -> None:
        self.can_move = False
        self.move_right(False)
        self.move_left(False)

    def start_movement(self) -> None:
        self.can_move = True
        self.move_right(False)
        self.move_left(False)

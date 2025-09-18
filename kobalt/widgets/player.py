import pygame

from .widget import Widget


class Player(Widget):
    """
    Simple controllable player built on Widget.
    Uses key state for left/right movement and event for jump.
    """

    def __init__(
        self,
        screen_size=(1280, 720),
        x=0,
        y=0,
        width=50,
        height=50,
        color=(0, 255, 0),
        image=None,
        speed=5,
        jump_height=8,
        gravity=0.5,
        air_strafe: bool = True,
        air_strafe_grow: float | None = None,
        air_strafe_decay: float | None = None,
        max_speed: int | None = None,
        air_strafe_ground_threshold_ms: int = 100,
    ):
        super().__init__(screen_size, x, y, width, height, color, image)

        # movement
        self.speed = speed
        self.old_speed = speed
        self.jump_height = jump_height
        self.gravity = gravity

        # air strafe
        self.air_strafe = air_strafe
        self.max_speed = max_speed if max_speed is not None else speed * 2.5
        self.air_strafe_grow = (
            air_strafe_grow
            if air_strafe_grow is not None
            else (self.max_speed - speed) * 0.01
        )
        self.air_strafe_decay = (
            air_strafe_decay if air_strafe_decay is not None else 0.98
        )
        self.air_strafe_ground_threshold_ms = air_strafe_ground_threshold_ms
        # tracked time spent on the ground (milliseconds)
        self.time_on_ground_ms = 0

        # physics
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False

    def draw(self, surface: pygame.Surface, dt):
        self._update(dt)

        # draw
        if self.image:
            img = pygame.transform.scale(self.image, (self.width, self.height))
            surface.blit(img, (self.x, self.y))
        else:
            pygame.draw.rect(surface, self.color, self.rect)

    def handle_event(self, event: pygame.event.Event):
        if (event.key in [pygame.K_SPACE, pygame.K_UP]) and self.on_ground:
            self.vel_y = -self.jump_height
            self.on_ground = False
            # leaving ground: reset ground timer
            self.time_on_ground_ms = 0

    def _update(self, dt):
        self._handle_horizontal_movement()
        self._apply_gravity()
        self._move()
        self._check_vertical_bounds()
        # track time spent on ground (ms)
        if self.on_ground:
            self.time_on_ground_ms += dt * 1000
        else:
            self.time_on_ground_ms = 0

    def _handle_horizontal_movement(self):
        keys = pygame.key.get_pressed()
        going_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        going_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]

        # direction: -1 (left), 0 (none or both), +1 (right)
        dirx = int(going_right) - int(going_left)
        self.vel_x = dirx * self.speed

        if not self.air_strafe:
            self.speed = self.old_speed
            return

        if dirx != 0 and self.time_on_ground_ms < self.air_strafe_ground_threshold_ms:
            self._grow_air_strafe()
        else:
            self._decay_air_strafe()

    def _grow_air_strafe(self):
        self.speed = min(self.speed + self.air_strafe_grow, self.max_speed)

    def _decay_air_strafe(self):
        self.speed = max(
            self.speed * self.air_strafe_decay,
            self.old_speed,
        )

    def _apply_gravity(self):
        self.vel_y += self.gravity

    def _move(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def _check_vertical_bounds(self):
        w, h = self.screen_size

        # prevent falling below the bottom of the screen
        if self.y + self.height > h:
            self.y = h - self.height
            self.vel_y = 0
            self.on_ground = True
        # make the sides loop
        if self.x > w:  # right side loop
            self.x = -self.width
        if self.x < -self.width:  # left side loop
            self.x = w

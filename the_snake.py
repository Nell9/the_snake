from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет границы ячейки - блекло-белый:
BORDER_COLOR = (200, 200, 200)

# Цвет яблока - красный:
APPLE_COLOR = (255, 0, 0)

# Цвет змейки - зеленый:
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Описывает все игровые обьекты."""

    position: tuple[int, int]
    body_color: tuple[int, int, int]

    def __init__(self):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс описывающий сущность <Яблоко>."""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self) -> tuple[int, int]:
        """Возвращает случайную позицию ячейки"""
        x = (randint(0, SCREEN_WIDTH) % GRID_SIZE) * GRID_SIZE
        y = (randint(0, SCREEN_HEIGHT) % GRID_SIZE) * GRID_SIZE
        self.position = (x, y)
        return (x, y)


class Snake(GameObject):
    """Класс описывающий сущность <Змейка>."""

    positions: list = []
    next_direction: tuple | None = None
    direction: tuple = RIGHT
    __lenght: int = 1
    last: tuple | None = None

    def __init__(self):
        super().__init__()
        self.positions.append(self.position)
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple_position):
        self.last = self.positions[-1]

        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        position_with_direction = tuple(
            x * y for x, y in zip(self.direction, (GRID_SIZE, GRID_SIZE))
        )
        position_head = tuple(
            x + y for x, y in zip(self.positions[0], position_with_direction)
        )

        if position_head[0] >= SCREEN_WIDTH:
            position_head = (0, position_head[1])
        elif position_head[0] < 0:
            position_head = (SCREEN_WIDTH, position_head[1])

        if position_head[1] >= SCREEN_HEIGHT:
            position_head = (position_head[0], 0)
        elif position_head[1] < 0:
            position_head = (position_head[0], SCREEN_HEIGHT)

        if position_head in self.positions:
            self.reset()

        if apple_position == position_head:
            self.positions.insert(0, apple_position)
            return True

        self.positions.insert(0, position_head)
        del self.positions[-1]
        return False

    def draw(self):
        for self.position in self.positions:
            super().draw()

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    @property
    def get_head_position(self): ...

    def reset(self):
        for position in self.positions:
            last_rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        pygame.display.flip()


def handle_keys(game_object):
    """Обработчик событий."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    # Инициализация PyGame:
    pygame.init()
    # Objects:
    apple = Apple()
    snake = Snake()

    running = True

    while running:
        handle_keys(snake)
        snake.draw()
        apple.draw()
        apple_was_eat = snake.move(apple.position)
        if apple_was_eat:
            apple.randomize_position()

        pygame.display.update()
        clock.tick(SPEED)


if __name__ == "__main__":
    main()


# Метод draw класса Snake.
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     Отрисовка головы змейки.
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     Затирание последнего сегмента.
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя.
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку.
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None

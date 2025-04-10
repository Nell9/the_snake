from random import choice

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цветовые характеристики:
BOARD_BACKGROUND_COLOR = (112, 128, 144)
BORDER_COLOR = (200, 200, 200)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15

# Начальная позиция змейки:
CENTRAL_POINT = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Координаты всех ячеек поля:
ALL_CELLS = set(
    (x * GRID_SIZE, y * GRID_SIZE)
    for x in range(GRID_SIZE)
    for y in range(GRID_SIZE)
)

# Допустимые изменения направления движения для обьекта Snake.
TURNS = {
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT
}

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Описывает все игровые обьекты."""

    def __init__(self, body_color: tuple = None, border_color: tuple = None):
        self.body_color: tuple[int, int, int] = body_color
        self.border_color: tuple[int, int, int] = border_color
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def draw(self):
        """Обязательный метод"""
        raise NotImplementedError(
            f'Метод draw не переопределен для обьекта {self}.')

    def draw_one_cell(
            self,
            position: tuple,
            background_color: tuple = None):
        """Отрисовка контура и заливка одной ячейки."""
        background_color = background_color or self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, background_color, rect)
        if background_color != BOARD_BACKGROUND_COLOR:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс описывающий сущность <Яблоко>."""

    def __init__(
            self, color: tuple = APPLE_COLOR, reserved_positions: list = None):
        super().__init__(color)
        self.randomize_position(reserved_positions or [])

    def draw(self):
        """Отрисовка яблока"""
        self.draw_one_cell(self.position)

    def randomize_position(self, reserved_positions: list):
        """Возвращает случайную позицию ячейки."""
        self.position = choice(tuple(ALL_CELLS - set(reserved_positions)))


class Snake(GameObject):
    """Класс описывающий сущность <Змейка>."""

    def __init__(self, color: tuple = SNAKE_COLOR):
        super().__init__(color)
        self.reset()

    def update_direction(self, new_direction):
        """Обновляет направление движения."""
        self.direction = new_direction

    def move(self):
        """Передвигает змейку в текущую позицию"""
        self.positions.insert(0, self.get_new_head_position())
        self.last = self.positions.pop()

    def restore_tail(self):
        """Восстанавливает хвост змеи"""
        self.positions.insert(-1, self.last)

    def draw(self):
        """
        Отрисовка ячеек змеи по координатам
        и затирание крайней клетки если змея передвинулась.
        """
        self.draw_one_cell(self.get_head_position())
        if self.last:
            self.draw_one_cell(self.last, BOARD_BACKGROUND_COLOR)

    def reset(self):
        """Сброс змеи в начальное состояние"""
        self.positions = [CENTRAL_POINT]
        self.direction = RIGHT
        self.last = None

    def get_new_head_position(self):
        """Вычисляет новую позицию головы змеи."""
        x_direction, y_direction = self.direction
        position_head_x, position_head_y = self.get_head_position()
        return (
            (position_head_x + (x_direction * GRID_SIZE) + SCREEN_WIDTH)
            % SCREEN_WIDTH,
            (position_head_y + (y_direction * GRID_SIZE) + SCREEN_HEIGHT)
            % SCREEN_HEIGHT
        )

    def get_head_position(self):
        """Возвращает позицию головы змеи"""
        return self.positions[0]

    def __len__(self):
        """Возвращает длину змеи."""
        return len(self.positions)


def handle_keys(snake: Snake):
    """Обработчик событий."""
    for event in pg.event.get():
        if (event.type == pg.QUIT
                or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE)):
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            snake.update_direction(TURNS.get(
                (snake.direction, event.key),
                snake.direction))


def main():
    """Main."""
    # Инициализация pg:
    pg.init()
    snake = Snake()
    apple = Apple(reserved_positions=snake.positions)
    screen.fill(BOARD_BACKGROUND_COLOR)

    running = True
    while running:
        handle_keys(snake)
        snake.move()
        if snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)
        elif apple.position == snake.get_head_position():
            apple.randomize_position(snake.positions)
            snake.restore_tail()

        pg.display.set_caption('Змейка. Длина змеи: ' + str(len(snake)))
        snake.draw()
        apple.draw()
        pg.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    print("gellow world")
    test test
    main()

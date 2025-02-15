from random import randint

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

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
screen.fill(BOARD_BACKGROUND_COLOR)
pg.display.set_caption(f'Змейка. speed: {SPEED}, score: 0')

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
            background_color: tuple = None,
            border_color: tuple = None):
        """Отрисовка контура и заливка одной ячейки."""
        if not background_color:
            background_color = self.body_color
        if not border_color:
            border_color = self.border_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, background_color, rect)
        pg.draw.rect(screen, border_color, rect, 1)


class Apple(GameObject):
    """Класс описывающий сущность <Яблоко>."""

    def __init__(
            self, color: tuple = None,
            border_color: tuple = None,
            reserved_positions: list = ()):
        super().__init__(color, border_color)
        self.reserved_positions = reserved_positions
        self.position = self.randomize_position()

    def draw(self):
        """Отрисовка яблока"""
        self.draw_one_cell(self.position)

    def randomize_position(self) -> tuple[int, int]:
        """Возвращает случайную позицию ячейки."""
        while True:
            x = (randint(0, SCREEN_WIDTH) // GRID_SIZE) * GRID_SIZE
            y = (randint(0, SCREEN_HEIGHT) // GRID_SIZE) * GRID_SIZE
            if (x, y) not in self.reserved_positions:
                break
        self.position = (x, y)
        return (x, y)


class Snake(GameObject):
    """Класс описывающий сущность <Змейка>."""

    def __init__(self, color: tuple = None, border_color: tuple = None):
        super().__init__(color, border_color)
        self.positions: list = []
        self.reset()
        self.next_direction: tuple | None = None
        self.direction: tuple = RIGHT
        self.__lenght: int = 1
        self.last: tuple | None = None

    def get_new_direction(self, new_direction: tuple = None):
        """Получает новое направление"""
        self.next_direction = new_direction

    def update_direction(self):
        """Обновляет направление движения."""
        if self.next_direction:
            self.direction = self.next_direction

    def move(self, apple_position: tuple[int, int] = None):
        """
        Отрисовывает змейку, проверяет сьедено ли яблоко.

        Параметры:
            apple_position: tuple[int, int] - Координаты яблока.
        """
        self.last = self.positions[-1]
        self.update_direction()
        position_head = self.get_new_head_position()

        if apple_position == position_head:
            self.positions.insert(0, apple_position)
            return True

        self.positions.insert(0, position_head)
        self.positions.pop()

    def draw(self):
        """
        Отрисовка ячеек змеи по координатам
        и затирание крайней клетки если змея передвинулась.
        """
        self.draw_one_cell(self.positions[0])
        if self.last:
            self.draw_one_cell(
                self.last, BOARD_BACKGROUND_COLOR,
                BOARD_BACKGROUND_COLOR)

    def reset(self):
        """Сброс змеи в начальное состояние"""
        for position in self.positions:
            self.draw_one_cell(
                position,
                BOARD_BACKGROUND_COLOR,
                BOARD_BACKGROUND_COLOR)
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT

    def get_new_head_position(self):
        """Вычисляет новую позицию головы змеи."""
        position_with_direction = tuple(
            x1 * x2 for x1, x2 in zip(self.direction, (GRID_SIZE, GRID_SIZE))
        )

        position_head_x = (
            self.positions[0][0] + position_with_direction[0] + SCREEN_WIDTH
        ) % SCREEN_WIDTH

        position_head_y = (
            self.positions[0][1] + position_with_direction[1] + SCREEN_HEIGHT
        ) % SCREEN_HEIGHT

        return (position_head_x, position_head_y)

    @property
    def get_head_position(self):
        """Возвращает позицию головы змеи"""
        return self.positions[0]


def handle_keys(game_object: Snake = None):
    """Обработчик событий."""
    events = {
        (LEFT, pg.K_UP): UP,
        (RIGHT, pg.K_UP): UP,
        (LEFT, pg.K_DOWN): DOWN,
        (RIGHT, pg.K_DOWN): DOWN,
        (UP, pg.K_LEFT): LEFT,
        (DOWN, pg.K_LEFT): LEFT,
        (UP, pg.K_RIGHT): RIGHT,
        (DOWN, pg.K_RIGHT): RIGHT
    }

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()

            new_direction = events.get(
                (game_object.direction, event.key),
                game_object.direction)
            game_object.get_new_direction(new_direction)


def main():
    """Ну main, хз что написать"""
    # Инициализация pg:
    pg.init()
    # Objects:
    player_score = 0
    snake = Snake(SNAKE_COLOR, BORDER_COLOR)
    apple = Apple(APPLE_COLOR, BORDER_COLOR, snake.positions)

    running = True
    while running:
        handle_keys(snake)

        if snake.get_head_position in snake.positions[1:]:
            snake.reset()
            player_score = 0
            pg.display.set_caption(f'Змейка. speed: {SPEED}, score: 0')
            pg.display.flip()
            continue

        apple_was_eat = snake.move(apple.position)
        if apple_was_eat:
            player_score += 1
            pg.display.set_caption(
                f"""
                Змейка. speed: {SPEED}, score: {player_score}
                """)
            apple.randomize_position()

        snake.draw()
        apple.draw()
        pg.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()

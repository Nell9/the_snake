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
DEFAULT_HEAD_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Допустимые изменения направления движения для обьекта Snake.
turns = {
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
            background_color: tuple = None,
            erase: bool = False):
        """Отрисовка контура и заливка одной ячейки."""
        background_color = background_color or self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, background_color, rect)
        if erase:
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect, 1)
        else:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс описывающий сущность <Яблоко>."""

    def __init__(
            self, color: tuple = APPLE_COLOR,
            # Практикум не принимает на ревью
            # не константные параметры по умолчанию.
            # Если указываю None - не проходит pytest.
            # Поэтому ().
            reserved_positions: list = ()):
        super().__init__(color)
        self.randomize_position(reserved_positions)

    def draw(self):
        """Отрисовка яблока"""
        self.draw_one_cell(self.position)

    # Практикум не принимает на ревью
    # не константные параметры по умолчанию.
    # Если указываю None - не проходит pytest.
    # Поэтому ().
    def randomize_position(
            self,
            reserved_positions: list = ()) -> tuple[int, int]:
        """Возвращает случайную позицию ячейки."""
        ALL_CELLS = set((x * GRID_SIZE, y * GRID_SIZE)
                        for x in range(GRID_SIZE)
                        for y in range(GRID_SIZE))
        self.position = choice(tuple(ALL_CELLS - set(reserved_positions)))


class Snake(GameObject):
    """Класс описывающий сущность <Змейка>."""

    def __init__(self, color: tuple = SNAKE_COLOR):
        super().__init__(color)
        self.positions: list = [DEFAULT_HEAD_POSITION]
        self.direction: tuple = RIGHT
        self.__lenght: int = 1
        self.last: tuple | None = None
        self.reset()

    def update_direction(self, new_direction):
        """Обновляет направление движения."""
        self.direction = new_direction

    def move(self):
        """Передвигает змейку в текущую позицию"""
        self.last = self.positions[-1]
        self.positions.insert(0, self.get_new_head_position())
        self.positions.pop()

    def draw(self):
        """
        Отрисовка ячеек змеи по координатам
        и затирание крайней клетки если змея передвинулась.
        """
        self.draw_one_cell(self.get_head_position())
        # TODO
        if self.last:
            self.draw_one_cell(self.last, BOARD_BACKGROUND_COLOR, True)

    def reset(self):
        """Сброс змеи в начальное состояние"""
        self.positions = [DEFAULT_HEAD_POSITION]
        self.direction = RIGHT
        self.__lenght = None
        self.last = None

    def get_new_head_position(self):
        """Вычисляет новую позицию головы змеи."""
        x_shift = self.direction[0] * GRID_SIZE
        y_shift = self.direction[1] * GRID_SIZE

        position_head_x = self.get_head_position()[0]
        position_head_y = self.get_head_position()[1]

        position_head_x = (
            position_head_x + x_shift + SCREEN_WIDTH
        ) % SCREEN_WIDTH

        position_head_y = (
            position_head_y + y_shift + SCREEN_HEIGHT
        ) % SCREEN_HEIGHT

        return (position_head_x, position_head_y)

    def get_head_position(self):
        """Возвращает позицию головы змеи"""
        return self.positions[0]


# Без указания параметра по умолчанию не дает закрузить на ревью.
# Не проходит тесты. Поэтому оставляю None.
def handle_keys(game_object: GameObject = None):
    """Обработчик событий."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            game_object.update_direction(turns.get(
                (game_object.direction, event.key),
                game_object.direction))


def main():
    """Ну main, хз что написать"""
    # Инициализация pg:
    pg.init()
    player_score = 0
    snake = Snake()
    apple = Apple(reserved_positions=snake.positions)
    screen.fill(BOARD_BACKGROUND_COLOR)

    running = True

    while running:
        handle_keys(snake)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            player_score = 0
            apple.randomize_position(apple.position)
            screen.fill(BOARD_BACKGROUND_COLOR)

        if apple.position == snake.get_new_head_position():
            player_score += 1
            snake.positions.insert(0, apple.position)
            apple.randomize_position(snake.positions)
        else:
            snake.move()

        apple.draw()
        snake.draw()
        pg.display.set_caption(
            f'Змейка. speed: {SPEED}, score: {player_score}')
        pg.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()

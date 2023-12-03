import pygame
import random
import logging

# Настройки окна игры
WIDTH = 800
HEIGHT = 600
FPS = 10

# Настройки змейки
SNAKE_SIZE = 20
SNAKE_SPEED = 20

# Настройки цветов
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Инициализация Pygame
pygame.init()

# Установка размеров и заголовка окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

# Инициализация логгера
logging.basicConfig(filename='game.log', level=logging.INFO, format='%(asctime)s %(message)s')
logging.basicConfig(filename='moves.log', level=logging.INFO, format='%(asctime)s %(message)s')

clock = pygame.time.Clock()


class Snake:
    """Класс для управления змейкой"""

    def __init__(self):
        self.segments = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = random.choice(['up', 'down', 'left', 'right'])

    def move(self):
        x, y = self.segments[0]
        if self.direction == 'up':
            y -= SNAKE_SPEED
        elif self.direction == 'down':
            y += SNAKE_SPEED
        elif self.direction == 'left':
            x -= SNAKE_SPEED
        elif self.direction == 'right':
            x += SNAKE_SPEED

        self.segments.insert(0, (x, y))
        self.segments.pop()

    def change_direction(self, new_direction):
        if new_direction == 'up' and self.direction != 'down':
            self.direction = new_direction
        elif new_direction == 'down' and self.direction != 'up':
            self.direction = new_direction
        elif new_direction == 'left' and self.direction != 'right':
            self.direction = new_direction
        elif new_direction == 'right' and self.direction != 'left':
            self.direction = new_direction
        logging.info(f"Snake moved {new_direction}")

    def draw(self):
        for segment in self.segments:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))


class Food:
    """Класс для отображения еды"""

    def __init__(self):
        self.position = self.generate_position()

    @staticmethod
    def generate_position():
        x = random.randrange(0, WIDTH, SNAKE_SIZE)
        y = random.randrange(0, HEIGHT, SNAKE_SIZE)
        return x, y

    def draw(self):
        pygame.draw.rect(screen, RED, (self.position[0], self.position[1], SNAKE_SIZE, SNAKE_SIZE))


logging.info("Game started")
# Создание объектов змейки и еды
snake = Snake()
logging.info("Snake is created")
food = Food()
logging.info("Food is created")

# Главный цикл игры
running = True
while running:
    clock.tick(FPS)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction('up')
            elif event.key == pygame.K_DOWN:
                snake.change_direction('down')
            elif event.key == pygame.K_LEFT:
                snake.change_direction('left')
            elif event.key == pygame.K_RIGHT:
                snake.change_direction('right')

    # Проверка столкновения с едой
    if snake.segments[0] == food.position:
        logging.info(f"Snake ate an apple. Length = {len(snake.segments)+1}")
        snake.segments.append(snake.segments[-1])
        food.position = food.generate_position()

    # Проверка столкновения со стенами
    if (snake.segments[0][0] < 0 or snake.segments[0][0] >= WIDTH
            or snake.segments[0][1] < 0 or snake.segments[0][1] >= HEIGHT):
        logging.info('Crushed into a wall')
        running = False

    # Проверка столкновения с собой
    if snake.segments[0] in snake.segments[2:]:
        logging.info('Crushed into itself')
        running = False

    # Обновление змейки и еды
    snake.move()

    # Отрисовка
    screen.fill(BLACK)
    snake.draw()

    food.draw()

    # Обновление экрана
    pygame.display.flip()

# Завершение Pygame
pygame.quit()
logging.info("Game over\n\n")

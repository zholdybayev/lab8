import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

clock = pygame.time.Clock()

coordinates = ()


class Wall:
    def __init__(self) -> None:
        self.amount = 1
        self.points = [random_coordinates()]
        self.color = GRAY
    
    def draw(self, surface):
        for p in self.points:
            r = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
    
    def add_new_walls(self, snake):
        self.amount += 1
        if self.amount > 10:
            self.amount = 10
        self.points = []
        for i in range(self.amount):
            x, y = random_coordinates()
            while (x * GRID_SIZE, y * GRID_SIZE) in snake.positions:
                x, y = random_coordinates()
            self.points.append(random_coordinates())

    def get_points(self):
        return self.points
    
    def reset(self):
        self.amount = 1
        self.points = [random_coordinates()]

def random_coordinates():
    return (random.randint(0, GRID_SIZE), random.randint(0, GRID_SIZE))

def draw_food(surface, points = None):
    if points is None:
        x, y = random_coordinates()
        global coordinates
        coordinates = (x, y)
        while coordinates in wall.get_points():
            x, y = random_coordinates()
            coordinates = (x, y)
        rect = pygame.Rect(((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(surface, GREEN, rect)
        return True
    else:
        x, y = points
        coordinates = (x, y)
        rect = pygame.Rect(((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(surface, GREEN, rect)
        return True

class Snake:
    def __init__(self) -> None:
        self.length = 1
        self.positions = [((WIDTH / 2), (HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = RED

    def get_head_position(self):
            return self.positions[0]
    
    def turn(self, point):
        self.direction = point
    
    def get_longer(self, coordinates):
        current = self.get_head_position()
        if ((((coordinates[0] * GRID_SIZE) % WIDTH), ((coordinates[1] * GRID_SIZE) % HEIGHT)) == current):
            self.length+=1
            return True
  
    def move(self, wall : Wall):
        current = self.get_head_position()
        x, y = self.direction
        new = (((current[0] + (x*GRID_SIZE)) % WIDTH), (current[1] + (y*GRID_SIZE)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:] or new in self.positions[1:] or (current[0] // 20, current[1] // 20) in wall.get_points():
            wall.reset()
            self.reset()
            draw_food(screen)
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((WIDTH / 2), (HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])


    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, WHITE, r, 1)




snake = Snake()
wall = Wall()
running = True
draw_food(screen)
wall.draw(screen)
print(coordinates)
print(snake.get_head_position())
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.turn(UP)
            elif event.key == pygame.K_DOWN:
                snake.turn(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.turn(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.turn(RIGHT)
    
    if snake.get_longer(coordinates):
            draw_food(screen)
            print(snake.get_longer(coordinates))
            wall.add_new_walls(snake)
    snake.move(wall)

    screen.fill(BLACK)   
    snake.draw(screen)
    wall.draw(screen)
    draw_food(screen, coordinates) 
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()

import pygame
import random

pygame.init()

W = 500
BLOCK = 20
UI_HEIGHT = 40

screen = pygame.display.set_mode((W, W))
pygame.display.set_caption("Snake PBO")
clock = pygame.time.Clock()

BG = (25, 25, 25)
GREEN = (0, 255, 100)
RED = (255, 70, 70)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
YELLOW = (255, 200, 0)

font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 40)

class GameObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake(GameObject):
    def __init__(self):
        super().__init__(200, 200)
        self.body = [(self.x, self.y)]
        self.direction = (BLOCK, 0)

    def move(self):
        head = (self.body[0][0] + self.direction[0],
                self.body[0][1] + self.direction[1])
        self.body.insert(0, head)

    def pop_tail(self):
        self.body.pop()

    def draw(self):
        for x, y in self.body:
            pygame.draw.rect(screen, GREEN, (x, y, BLOCK, BLOCK))

class Food(GameObject):
    def __init__(self, snake_body):
        super().__init__(0, 0)
        self.spawn(snake_body)

    def spawn(self, snake_body):
        while True:
            self.x = random.randrange(0, W, BLOCK)
            self.y = random.randrange(UI_HEIGHT, W, BLOCK)
            if (self.x, self.y) not in snake_body:
                break

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, BLOCK, BLOCK))

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.running = True
        self.game_over = False
        self.score = 0
        self.high_score = 0

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if not self.game_over:
                    if event.key == pygame.K_UP and self.snake.direction != (0, BLOCK):
                        self.snake.direction = (0, -BLOCK)
                    elif event.key == pygame.K_DOWN and self.snake.direction != (0, -BLOCK):
                        self.snake.direction = (0, BLOCK)
                    elif event.key == pygame.K_LEFT and self.snake.direction != (BLOCK, 0):
                        self.snake.direction = (-BLOCK, 0)
                    elif event.key == pygame.K_RIGHT and self.snake.direction != (-BLOCK, 0):
                        self.snake.direction = (BLOCK, 0)
                else:
                    if event.key == pygame.K_r:
                        if self.score > self.high_score:
                            self.high_score = self.score
                        self.snake = Snake()
                        self.food = Food(self.snake.body)
                        self.score = 0
                        self.game_over = False

    def update(self):
        if self.game_over:
            return

        self.snake.move()
        head = self.snake.body[0]

        if (head[0] < 0 or head[0] >= W or
            head[1] < 0 or head[1] >= W or
            head in self.snake.body[1:] or
            head[1] < UI_HEIGHT):
            self.game_over = True
            return

        if head == (self.food.x, self.food.y):
            self.food.spawn(self.snake.body)
            self.score += 1
        else:
            self.snake.pop_tail()

    def draw_ui(self):
        pygame.draw.rect(screen, GRAY, (0, 0, W, UI_HEIGHT))

        score_text = font.render(f"Score: {self.score}", True, WHITE)
        high_text = font.render(f"High: {self.high_score}", True, YELLOW)

        screen.blit(score_text, (10, 10))
        screen.blit(high_text, (250, 10))

    def draw(self):
        screen.fill(BG)

        self.snake.draw()
        self.food.draw()
        self.draw_ui()

        if self.game_over:
            over_text = big_font.render("GAME OVER", True, RED)
            info_text = font.render("Tekan R untuk ulang", True, WHITE)

            screen.blit(over_text, (170, 230))
            screen.blit(info_text, (150, 270))

        pygame.display.flip()

    def run(self):
        while self.running:
            clock.tick(7)
            self.input()
            self.update()
            self.draw()

        pygame.quit()

game = Game()
game.run()
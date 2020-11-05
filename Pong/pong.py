from random import randint

import pygame

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.velocity = [randint(4, 6), randint(-4, 4)]

        self.rect = self.image.get_rect()
        self.rect.x = 345
        self.rect.y = 195

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-4, 4)


class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

    def move_up(self, pixels):
        self.rect.y -= pixels
        if self.rect.y < 0:
            self.rect.y = 0

    def move_down(self, pixels):
        self.rect.y += pixels
        if self.rect.y > 400:
            self.rect.y = 400

size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")

paddle_a = Paddle(WHITE, 10, 100)
paddle_a.rect.x = 20
paddle_a.rect.y = 200

paddle_b = Paddle(WHITE, 10, 100)
paddle_b.rect.x = 670
paddle_b.rect.y = 200

ball = Ball(WHITE,10,10)
# ball.rect.x = 345
# ball.rect.y = 195

all_sprites_list = pygame.sprite.Group()

all_sprites_list.add(paddle_a)
all_sprites_list.add(paddle_b)
all_sprites_list.add(ball)

score_a = 0
score_b = 0

game_over = False
clock = pygame.time.Clock()
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:  # Pressing the x Key will quit the game
                game_over = True
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddle_a.move_up(5)
    if keys[pygame.K_s]:
        paddle_a.move_down(5)
    if keys[pygame.K_UP]:
        paddle_b.move_up(5)
    if keys[pygame.K_DOWN]:
        paddle_b.move_down(5)

    all_sprites_list.update()

    if ball.rect.x >= 690:
        score_a += 1
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x <= 0:
        score_b += 1
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y > 490:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y < 0:
        ball.velocity[1] = -ball.velocity[1]

    if pygame.sprite.collide_mask(ball, paddle_a) :
        if ball.velocity[0] <= 0:
            ball.bounce()
    if pygame.sprite.collide_mask(ball, paddle_b):
        if ball.velocity[0] >= 0:
            ball.bounce()


    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)
    all_sprites_list.draw(screen)

    font = pygame.font.Font(None, 74)
    text = font.render(str(score_a), 1, WHITE)
    screen.blit(text, (250, 10))
    text = font.render(str(score_b), 1, WHITE)
    screen.blit(text, (420, 10))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height, ball):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.ball = ball
        self.rect = self.image.get_rect()
        self.update()

    def update(self):
        self.rect.x = self.ball.x
        self.rect.y = self.ball.y


class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height, paddle):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.paddle = paddle
        self.rect = self.image.get_rect()
        self.update()

    def update(self):
        self.rect.x = self.paddle.x
        self.rect.y = self.paddle.y
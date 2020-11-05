import time
from random import randint

import keras
import pygame

import pongUI
from bot import PongBot

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class UI:
    def __init__(self, pong):
        pygame.init()
        self.size = (700, 500)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Pong")
        self.paddle_a_sprite = pongUI.Paddle(WHITE, 10, 100, pong.paddle_a)
        self.paddle_b_sprite = pongUI.Paddle(WHITE, 10, 100, pong.paddle_b)
        self.ball_sprite = pongUI.Ball(WHITE, 10, 10, pong.ball)
        self.all_sprites_list = pygame.sprite.Group()
        self.all_sprites_list.add(self.paddle_a_sprite)
        self.all_sprites_list.add(self.paddle_b_sprite)
        self.all_sprites_list.add(self.ball_sprite)
        self.clock = pygame.time.Clock()


class Ball:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.velocity = [randint(5, 7), randint(-4, 4)]
        self.x = 345
        self.y = 195

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-4, 4)


class Paddle:
    def __init__(self, width, height, x, y, ):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def move_up(self, pixels):
        self.y -= pixels
        if self.y < 0:
            self.y = 0

    def move_down(self, pixels):
        self.y += pixels
        if self.y > 400:
            self.y = 400


class Pong:
    def __init__(self, human_player_one = True, human_player_two = True):
        self.ball = Ball(10, 10)
        self.paddle_a = Paddle(10, 100, 20, 200)
        self.paddle_b = Paddle(10, 100, 670, 200)
        self.score_a = 0
        self.score_b = 0
        self.all_things = [self.ball, self.paddle_a, self.paddle_b]
        self.human_player_one = human_player_one
        self.human_player_two = human_player_two

    def get_updates(self, bot_one, bot_two, max_score):
        game_over = False
        self.ball.update()
        if not self.human_player_one:
            move = bot_one.get_move(self.ball, self.paddle_a)
            if move[0] == 1:
                self.paddle_a.move_up(5)
            elif move[1] == 1:
                self.paddle_a.move_down(5)
        if not self.human_player_two:
            move = bot_two.get_move(self.ball, self.paddle_b)
            if move[0] == 1:
                self.paddle_b.move_up(5)
            elif move[1] == 1:
                self.paddle_b.move_down(5)

        if self.ball.x >= 690:
            self.score_a += 1
            if self.score_a == max_score:
                game_over = True
            self.ball.velocity[0] = -self.ball.velocity[0]
        if self.ball.x <= 0:
            self.score_b += 1
            if self.score_b == max_score:
                game_over = True
            self.ball.velocity[0] = -self.ball.velocity[0]
        if self.ball.y > 490:
            self.ball.velocity[1] = -self.ball.velocity[1]
        if self.ball.y < 0:
            self.ball.velocity[1] = -self.ball.velocity[1]

        if colliding(self.ball, self.paddle_a):
            if self.ball.velocity[0] <= 0:
                self.ball.bounce()
        if colliding(self.ball, self.paddle_b):
            if self.ball.velocity[0] >= 0:
                self.ball.bounce()
        return game_over

    def update_ui(self, ui, hide_ui):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                hide_ui = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:  # Pressing the x Key will quit the game
                    hide_ui = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.human_player_one:
            self.paddle_a.move_up(5)
        if keys[pygame.K_s] and self.human_player_one:
            self.paddle_a.move_down(5)
        if keys[pygame.K_UP] and self.human_player_two:
            self.paddle_b.move_up(5)
        if keys[pygame.K_DOWN] and self.human_player_two:
            self.paddle_b.move_down(5)
        if not hide_ui:
            ui.all_sprites_list.update()
            ui.screen.fill(BLACK)
            pygame.draw.line(ui.screen, WHITE, [349, 0], [349, 500], 5)
            ui.all_sprites_list.draw(ui.screen)
            font = pygame.font.Font(None, 74)
            text = font.render(str(self.score_a), 1, WHITE)
            ui.screen.blit(text, (250, 10))
            text = font.render(str(self.score_b), 1, WHITE)
            ui.screen.blit(text, (420, 10))
            pygame.display.flip()
            if self.human_player_two or self.human_player_one:
                ui.clock.tick(60)
        return hide_ui

    def run(self, bot_one=None, bot_two=None, with_ui=True, max_score=7):

        hide_ui = False
        if with_ui:
            ui = UI(self)

        game_over = False
        while not game_over:
            game_over = self.get_updates(bot_one, bot_two, max_score)
            if with_ui:
                hide_ui = self.update_ui(ui, hide_ui)

        if with_ui:
            pygame.quit()
        if self.score_a == max_score:
            # player 1
            return 0
        elif self.score_b == max_score:
            # player 2
            return 1
        # quit early
        return -1


def colliding(ball, paddle):
    if paddle.x <= ball.x <= paddle.x + paddle.width or paddle.x <= ball.x + ball.width <= paddle.x + paddle.width:
        if paddle.y <= ball.y <= paddle.y + paddle.height or paddle.y <= ball.y + ball.height <= paddle.y + paddle.height:
            return True
    return False

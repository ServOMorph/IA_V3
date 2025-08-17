#!/usr/bin/env python3
# Copyright (C) 2022 Ollama

"""
Simple Pong game using pygame library.
Two players can control the paddles using keyboard, and there's a scoring system.
"""

import sys
import pygame
from pygame.locals import *

# Constants
WIDTH = 800
HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_RADIUS = 10
BALL_SPEED = 7

def init():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong Game")
    return screen

def create_paddles(screen):
    paddle1 = pygame.Rect(PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    paddle2 = pygame.Rect(WIDTH - PADDLE_WIDTH - 1, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    return paddle1, paddle2

def create_ball(screen):
    ball = pygame.Rect(BALL_RADIUS, BALL_RADIUS)
    ball.centerx = WIDTH // 2
    ball.centery = HEIGHT // 2
    return ball

def draw_elements(screen, paddle1, paddle2, ball):
    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (255, 255, 255), paddle1)
    pygame.draw.rect(screen, (255, 255, 255), paddle2)
    pygame.draw.ellipse(screen, (255, 255, 255), ball)
    pygame.display.flip()

def update_ball(ball, speed):
    ball.x += speed[0]
    ball.y += speed[1]

    if ball.left < 0 or ball.right > WIDTH:
        speed[0] = -speed[0]

    if ball.top < 0 or ball.bottom > HEIGHT:
        speed[1] = -speed[1]

def handle_keydown(paddle, key):
    if key == K_UP:
        paddle.y -= PADDLE_HEIGHT
    elif key == K_DOWN:
        paddle.y += PADDLE_HEIGHT

def main():
    screen = init()
    paddle1, paddle2 = create_paddles(screen)
    ball = create_ball(screen)

    speed = [BALL_SPEED, BALL_SPEED]

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        handle_keydown(paddle1, keys[K_UP])
        handle_keydown(paddle2, keys[K_DOWN])

        draw_elements(screen, paddle1, paddle2, ball)
        update_ball(ball, speed)
        pygame.time.delay(10)

if __name__ == "__main__":
    main()

import sys
import pygame
from pygame.locals import *

# Constantes
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_RADIUS = 10
SPEED = 7

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Fonctions pour gérer les événements clavier
def handle_keydown_event(event):
    if event.key == K_UP:
        y_vel += SPEED
    elif event.key == K_DOWN:
        y_vel -= SPEED

# Initialisation des objets et variables pour le jeu
ball = pygame.image.load(r"C:\Users\raph6\Documents\ServOMorph\IA_V3\ball.png").convert()  # Chargez une image de la balle
paddle1, paddle2 = pygame.Rect(PADDLE_WIDTH, HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT), pygame.Rect(WIDTH - PADDLE_WIDTH - PADDLE_WIDTH, HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
x, y = WIDTH // 2, HEIGHT // 2
y_vel, x_vel = SPEED, SPEED
score1, score2 = 0, 0
font = pygame.font.Font(None, 32)

# Boucle principale du jeu
while True:
    # ...

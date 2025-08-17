# Nom du script: pong_game.py

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
ball = pygame.image.load('ball.png').convert()  # Chargez une image de la balle
paddle1, paddle2 = pygame.Rect(PADDLE_WIDTH, HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT), pygame.Rect(WIDTH - PADDLE_WIDTH - PADDLE_WIDTH, HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
x, y = WIDTH // 2, HEIGHT // 2
y_vel, x_vel = SPEED, SPEED
score1, score2 = 0, 0
font = pygame.font.Font(None, 32)

# Boucle principale du jeu
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            handle_keydown_event(event)

    # Mise à jour des positions des objets et vérification de la collision
    x += x_vel
    y += y_vel
    paddle1.y += y_vel if pygame.Rect(paddle1, ball).colliderect([paddle1]) else 0
    paddle2.y += -y_vel if pygame.Rect(paddle2, ball).colliderect([paddle2]) else 0

    # Détection de la collision avec les bords de l'écran
    if x <= BALL_RADIUS or x + BALL_RADIUS >= WIDTH - BALL_RADIUS:
        x_vel *= -1
    if y <= BALL_RADIUS or y + BALL_RADIUS >= HEIGHT - BALL_RADIUS:
        y_vel *= -1

    # Détection de la collision entre les deux joueurs et la balle
    if x < 0 and y >= paddle2.y and y <= paddle2.y + PADDLE_HEIGHT or \
       x + BALL_RADIUS > WIDTH and y >= paddle1.y and y <= paddle1.y + PADDLE_HEIGHT:
        x = WIDTH // 2
        x_vel *= -1
        score2 += 1

    # Affichage des éléments graphiques et du score
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), paddle1)
    pygame.draw.rect(screen, (255, 255, 255), paddle2)
    screen.blit(ball, (x, y))
    text_surface = font.render(f"Score: {score1}:{score2}", True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(text_surface, text_rect)

    # Mise à jour de la fenêtre graphique et du temps d'exécution
    pygame.display.update()
    clock.tick(60)

import time
import os

# Constants
WIDTH = 80
HEIGHT = 10
BALL_SPEED_X = 2
BALL_SPEED_Y = 2
PADDLE_WIDTH = 4
PADDLE_HEIGHT = 3
LEFT_PADDLE_POS_Y = int(HEIGHT / 2)
RIGHT_PADDLE_POS_Y = LEFT_PADDLE_POS_Y
BALL_POS_X = WIDTH // 2
BALL_POS_Y = HEIGHT // 2

# Draw functions
def draw_paddle(y, side):
    attr = 1 if side == "left" else -1
    os.system(f'cls')
    for i in range(PADDLE_HEIGHT):
        print(f'\u2588' * PADDLE_WIDTH, end='\r')
    print(f"\u2502" * WIDTH)
    print(f'\u2588' * PADDLE_WIDTH, end='\r')
    for i in range(PADDLE_HEIGHT - 1):
        print(f'\u2500{attr * "\u2502"}' * (PADDLE_WIDTH - 2) + '\u2502', end='\r')

def draw_ball():
    os.system('cls')
    print(f"\u2588" * WIDTH)
    print(f'\u2502' * BALL_POS_X + ' ' * (WIDTH - BALL_POS_X - 1) + '\u2502')
    print(f"\u2588" * WIDTH)
    for y in range(HEIGHT):
        if y == BALL_POS_Y:
            print(f'{(" " * (BALL_POS_X))}\u2588{" " * (WIDTH - BALL_POS_X)}')
        else:
            print(f'\u2502' * WIDTH)
    draw_paddle(LEFT_PADDLE_POS_Y, "left")
    draw_paddle(RIGHT_PADDLE_POS_Y, "right")

# Main game loop
def main():
    while True:
        time.sleep(0.05)
        draw_ball()
        os.system('cls')  # Clear the screen after drawing

        # Update ball position
        BALL_POS_X += BALL_SPEED_X
        if BALL_POS_X < 1 or BALL_POS_X + 3 >= WIDTH:
            BALL_SPEED_X *= -1

        BALL_POS_Y += BALL_SPEED_Y
        if BALL_POS_Y < 1 or BALL_POS_Y + 3 > HEIGHT:
            BALL_POS_Y = HEIGHT // 2
            BALL_SPEED_Y *= -1

        # Paddle movement
        if ord(input("A")) == 65 and LEFT_PADDLE_POS_Y > 1:
            LEFT_PADDLE_POS_Y -= 1
        elif ord(input("D")) == 68 and RIGHT_PADDLE_POS_Y < HEIGHT - PADDLE_HEIGHT:
            RIGHT_PADDLE_POS_Y += 1

        # Check ball collisions with paddles
        if BALL_POS_X in range(LEFT_PADDLE_POS_Y, LEFT_PADDLE_POS_Y + PADDLE_HEIGHT) and BALL_POS_Y == LEFT_PADDLE_POS_Y:
            BALL_SPEED_X *= -1
        elif BALL_POS_X in range(RIGHT_PADDLE_POS_Y, RIGHT_PADDLE_POS_Y + PADDLE_HEIGHT) and BALL_POS_Y == RIGHT_PADDLE_POS_Y:
            BALL_SPEED_X *= -1

if __name__ == "__main__":
    main()

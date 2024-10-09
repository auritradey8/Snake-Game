import pygame
import sys
import random
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def generate_new_apple():
    return random.randrange(50, 750 - apple_size, apple_size), random.randrange(50, 550 - apple_size, apple_size)

def reset_game():
    global snake_pos, move_x, move_y, apple_x, apple_y, show_arena, game_over, score, end_msg
    snake_pos = [(display[0] // 2 - snake_size // 2, display[1] // 2 - snake_size // 2)]
    move_x = move_y = 0
    apple_x, apple_y = generate_new_apple()
    show_arena = game_over = end_msg = False
    score = 0

def display_msg(msg, color):
    global text_surface, text_rect, blink, blink_interval, last_blink_time
    font = pygame.font.Font(None, 40)
    text_color = color
    text_surface = font.render(msg, True, text_color)
    text_rect = text_surface.get_rect(center=(display[0] // 2, display[1] // 2))

    blink = True
    blink_interval = 500
    last_blink_time = pygame.time.get_ticks()

if __name__ == "__main__":  # Corrected __name__ check
    pygame.init()
    display = (800, 600)
    screen = pygame.display.set_mode(display)
    pygame.display.set_caption("Snake Game")

    display_msg("Press [Enter] to Begin", (255, 255, 255))

    snake_size = 20
    snake_color = (0, 255, 0)
    snake_pos = [(display[0] // 2 - snake_size // 2, display[1] // 2 - snake_size // 2)]
    snake_speed = 0.3
    show_arena = False

    game_over = False

    move_x = 0
    move_y = 0

    apple_size = 20
    apple_color = (255, 0, 0)
    apple_x, apple_y = generate_new_apple()

    score = 0
    end_msg = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == pygame.K_RETURN and not show_arena and not game_over:
                    show_arena = True
                if event.key == pygame.K_RETURN and game_over:
                    reset_game()

                if show_arena and not game_over:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        move_x = 0
                        move_y = -snake_speed 
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        move_x = 0
                        move_y = snake_speed
                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        move_x = -snake_speed
                        move_y = 0 
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        move_x = snake_speed
                        move_y = 0

        screen.fill((0, 0, 0))

        if show_arena and not game_over:
            arena_color = (255, 255, 255)
            border_thickness = 1
            pygame.draw.rect(screen, arena_color, (50, 50, 700, 500), border_thickness)

            new_head = (snake_pos[0][0] + move_x, snake_pos[0][1] + move_y)
            snake_pos = [new_head] + snake_pos[:-1]

            if abs(new_head[0] - apple_x) < apple_size and abs(new_head[1] - apple_y) < apple_size:
                apple_x, apple_y = generate_new_apple()
                snake_pos.append(snake_pos[-1])
                score += 1

            pygame.draw.rect(screen, apple_color, (apple_x, apple_y, apple_size, apple_size))

            if new_head[0] < 50 or new_head[0] + snake_size > 750 or new_head[1] < 50 or new_head[1] + snake_size > 550:
                game_over = True
                show_arena = False

            if len(snake_pos) > 3 and new_head in snake_pos[1:]:
                game_over = True

            for pos in snake_pos:
                pygame.draw.rect(screen, snake_color, (pos[0], pos[1], snake_size, snake_size))

        elif game_over:
            display_msg("Game Over! Press [Enter] to Restart", (255, 0, 0))
            screen.blit(text_surface, text_rect)
            
            if not end_msg:
                print(f"Game Over! You scored {score}")
                try:
                    with open("score.txt", "r+") as scores:
                        prev_scores = [int(x) for x in scores.read().split("\n") if x.strip()]
                        prev_best = max(prev_scores) if prev_scores else 0
                        if score > prev_best:
                            print("NEW BEST!")
                        scores.write(f"{score}\n")
                except FileNotFoundError:
                    with open("score.txt", "w") as scores:
                        scores.write(f"{score}\n")

                end_msg = True

        else:
            current_time = pygame.time.get_ticks()
            if current_time - last_blink_time >= blink_interval:
                blink = not blink
                last_blink_time = current_time

            if blink:
                screen.blit(text_surface, text_rect)

        pygame.display.update()

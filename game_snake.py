import pygame
import random
import time

pygame.init()

# Настройки окна
WIDTH, HEIGHT = 600, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Загрузка фонового изображения (без масштабирования)
background = pygame.image.load("background_1.png")
bg_width, bg_height = background.get_size()

# Цвета
YELLOW = (255, 255, 0)  # Цвет змейки
FOOD_COLORS = [(255, 0, 0), (0, 0, 255)]  # Красный и синий цвета еды
WHITE = (255, 255, 255)

# Шрифт
font = pygame.font.Font(None, 36)  # Стандартный шрифт, размер 36
game_over_font = pygame.font.Font(None, 50)  # Крупный шрифт для "Game Over"

clock = pygame.time.Clock()


def game_over(score):
    """Отображает Game Over, ждет 5 секунд и спрашивает про перезапуск"""
    win.fill((0, 0, 0))  # Черный экран
    game_over_text = game_over_font.render(f"Game Over! Your score: {score}", True, WHITE)
    retry_text = font.render("Try again? (Y/N)", True, WHITE)

    win.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
    win.blit(retry_text, (WIDTH // 2 - 100, HEIGHT // 2 + 10))
    pygame.display.update()

    time.sleep(2)  # Пауза 2 секунды перед вводом

    # Ждем нажатия Y или N
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True  # Перезапуск
                elif event.key == pygame.K_n:
                    pygame.quit()
                    quit()
        time.sleep(0.1)


def main():
    """Основная функция игры"""
    # Переменные игры
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    food_pos = [random.randrange(1, WIDTH // 10) * 10, random.randrange(1, HEIGHT // 10) * 10]
    food_spawn = True
    direction = 'RIGHT'
    change_to = direction
    speed = 15
    score = 0
    food_color_index = 0
    last_food_flash = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        # Изменение направления
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Движение змейки
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        # Добавление новой головы
        snake_body.insert(0, list(snake_pos))

        # Проверка на поедание еды
        if snake_pos == food_pos:
            food_spawn = False
            score += 1  # Увеличиваем счет
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, WIDTH // 10) * 10, random.randrange(1, HEIGHT // 10) * 10]

        food_spawn = True

        # Проверка на столкновение со стеной
        if snake_pos[0] < 0 or snake_pos[0] > WIDTH - 10 or snake_pos[1] < 0 or snake_pos[1] > HEIGHT - 10:
            if game_over(score):
                main()  # Перезапуск игры
            else:
                pygame.quit()
                quit()

        # Проверка на столкновение с самой собой
        for block in snake_body[1:]:
            if snake_pos == block:
                if game_over(score):
                    main()  # Перезапуск игры
                else:
                    pygame.quit()
                    quit()

        # Отрисовка фона без масштабирования
        bg_x = (WIDTH - bg_width) // 2
        bg_y = (HEIGHT - bg_height) // 2
        win.fill((0, 0, 0))
        win.blit(background, (bg_x, bg_y))

        # Мигание еды каждые 500 мс
        current_time = pygame.time.get_ticks()
        if current_time - last_food_flash > 500:
            food_color_index = (food_color_index + 1) % 2
            last_food_flash = current_time

        # Отрисовка змейки и еды
        for pos in snake_body:
            pygame.draw.rect(win, YELLOW, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(win, FOOD_COLORS[food_color_index], pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Отображение счета
        score_text = font.render(f"Score: {score}", True, WHITE)
        win.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(speed)


# Запуск игры
main()

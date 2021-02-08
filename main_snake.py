import pygame as pg
import pygame
import sys
import random
import pygame_menu

import threading

pg.init()
pygame.init()

# тут добавляем звук и картинки на фон
pygame.display.set_icon(pygame.image.load("scale_1200.png"))
image = pygame.image.load('backgraund.jpg')
sound1 = pg.mixer.Sound('music.wav')
sound2 = pg.mixer.Sound('music2.mp3')
sound_eating = pg.mixer.Sound('zvuk-otkusyivaniya-yabloka-13332.wav')
sound_click = pg.mixer.Sound('clikc.wav')
sound_knock = pg.mixer.Sound('doorknock1.wav')
sound_ai = pg.mixer.Sound('bolno-1.7-3.4.mp3')
block_size = 20
big_apple_color = (139, 0, 255)
roter_apple_color = (0, 0, 0)  # цвет гнилого яблока
color_wrame = (0, 255, 200)
head_color = (0, 200, 150)
white = (255, 255, 255)
red = (255, 0, 0)
snake_color = (0, 100, 0)
blue = (200, 250, 250)
size = [600, 800]  # размер окна
bloks = 20  # кол-во блоков
mar = 1
header_mar = 70
apples = []

size = [block_size * bloks + 2 * block_size + mar * bloks,
        block_size * bloks + 2 * block_size + mar * bloks + header_mar]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Лучший Змейка на Диком Западе')
timer = pygame.time.Clock()
shrift = pygame.font.SysFont('shrift', 36)

pause = False
apple_time_life = 1  # время добавления бонус яблока
wall = False  # Установить для этой переменной значение «True», если хотите, чтобы змея врезалась в стену
apple_decay_time = 10
apple_time_dead = 5  # Как долго будет ждать гниющее яблоко


# Класс змеки где мы узнаеи где она
class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        if wall:
            return 0 != self.x < bloks - 1 and 0 != self.y < bloks - 1
        else:
            return True

    def __eq__(self, other):
        return isinstance(other, Snake) and self.x == other.x and self.y == other.y


class super_apple:
    def __init__(self, x, y, decay, decay_time):
        self.x = x
        self.y = y
        self.decay = decay  # время распадаться
        self.dacay_time = decay_time  # гнилое время
        self.tvert = True  # гнилой или нет
        self.gnil = False
        self.thread = 0

    def Tick(self):
        while not self.gnil and self.tvert:
            self.decay -= 1

            if self.decay <= 0:
                self.tvert = False
                break

            timer.tick(1)

        while not self.gnil and not self.tvert:
            self.dacay_time -= 1

            if self.dacay_time <= 0:
                self.gnil = True
                self.gnil = True
                break

            timer.tick(1)


# рисуем поле для змеи
def draw_block(color, row, column):
    pygame.draw.rect(screen, color, [block_size + column * bloks + mar * (column + 1),
                                     header_mar + block_size + row * block_size + mar * (row + 1),
                                     block_size, block_size])


# эта фунция относится к модулю pygame_menu, она запускает игру при нажатии клавиши играть
def start_the_game():
    def random_block():
        x = random.randint(0, bloks - 1)
        y = random.randint(0, bloks - 1)
        empty_block = Snake(x, y)
        # Тут рандомно располагаем яблоко
        while empty_block in snake_block:
            empty_block.x = random.randint(0, bloks - 1)
            empty_block.y = random.randint(0, bloks - 1)
        return empty_block

    def job():
        while 0 == 0:  # :)
            blog_krona = random_block()

            super_Apl = super_apple(blog_krona.x, blog_krona.y, apple_decay_time, apple_time_dead)
            super_Apl.thread = threading.Thread(target=super_Apl.Tick)
            super_Apl.thread.start()

            apples.append(super_Apl)

            timer.tick(apple_time_life)

    total = 0  # счет сброшен
    snake_block = [Snake(9, 8), Snake(9, 9), Snake(9, 10)]
    apple = random_block()
    d_row = 0
    d_col = 1
    total = 0
    speed_snake = 1
    apples = []

    t1 = threading.Thread(target=job)
    t1.start()

    Pause = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('произошел выход из игры')
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # Происходит отслеживание нажатия клавиш
                if event.key == pygame.K_ESCAPE:
                    Pause = not Pause
                if event.key == pygame.K_UP and d_col != 0:
                    d_row = -1
                    d_col = 0
                    sound_click.play()
                elif event.key == pygame.K_DOWN and d_col != 0:
                    d_row = 1
                    d_col = 0
                    sound_click.play()
                elif event.key == pygame.K_LEFT and d_row != 0:
                    d_row = 0
                    d_col = -1
                    sound_click.play()
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    d_row = 0
                    d_col = 1
                    sound_click.play()
                elif event.key == pygame.K_F1:  # Подключение музыки
                    sound1.play()
                elif event.key == pygame.K_F2:
                    sound1.stop()
                elif event.key == pygame.K_F3:
                    sound2.play()
                elif event.key == pygame.K_F4:
                    sound2.stop()
                # Здесь на экране распологаются информационые сообщения
        screen.fill(color_wrame)
        pygame.draw.rect(screen, head_color, [0, 0, size[0], header_mar])
        total_text = shrift.render(f"Всего: {len(snake_block)}", 10, red)
        total_speed = shrift.render(f"Скорость змейки: {speed_snake}", 10, (255, 0, 255))
        pause_text = shrift.render("Игра на паузе; нажмите ESC", 20, red)
        screen.blit(total_text, (block_size, block_size))
        screen.blit(total_speed, (block_size + 200, block_size))
        # блоки один белый другой голубой
        for row in range(bloks):
            for column in range(bloks):
                if (row + column) % 2 == 0:
                    color = blue
                else:
                    color = white

                draw_block(color, row, column)
        # если змея стукается об экраны поля то игра прекращается
        head = snake_block[-1]
        if not head.is_inside():
            print('сломалась программка')
            sound_knock.play()
            # pygame.quit()
            # sys.exit()
            break

        # если голова змеи находится на яблоке то она его съедает и увеличивается
        if apple == head:
            sound_eating.play()
            total += 1
            speed_snake = total // 5 + 1
            snake_block.append(apple)
            apple = random_block()

        for big_apple in apples:
            if big_apple.x == head.x and big_apple.y == head.y:
                if big_apple.tvert:
                    sound_eating.play()
                    total += 2
                    bl_ok = Snake(big_apple.x, big_apple.y)
                    snake_block.append(bl_ok)
                    snake_block.append(bl_ok)
                else:
                    # звук тухлого яблока
                    total -= 1
                    snake_block.pop(0)

                big_apple.gnil = True
                apples.remove(big_apple)

        # если игра не паузе сохраняем положение змейки и выводим текст на экран
        if Pause:
            new_head = Snake(head.x + d_row, head.y + d_col)

            if not wall:
                if new_head.x < 0:
                    new_head.x = bloks - 1

                if new_head.x > bloks - 1:
                    new_head.x = 0

                if new_head.y < 0:
                    new_head.y = bloks - 1

                if new_head.y > bloks - 1:
                    new_head.y = 0

            if new_head in snake_block:
                print('змея врезалась в себя')
                sound_ai.play()
                # pygame.quit()
                # sys.exit()
                break

            snake_block.append(new_head)
            snake_block.pop(0)

        draw_block(red, apple.x, apple.y)

        for apl in apples:
            if apl.gnil:
                apples.remove(apl)
            else:
                if apl.tvert:
                    draw_block(big_apple_color, apl.x, apl.y)
                else:
                    draw_block(roter_apple_color, apl.x, apl.y)

        for block in snake_block:
            draw_block(snake_color, block.x, block.y)

        if not Pause:
            screen.blit(pause_text, (int(size[0] / 10), int(size[1] / 2)))

        pygame.display.flip()
        timer.tick(3 + speed_snake)


# тема меню игры
main_theme = pygame_menu.themes.THEME_DARK.copy()
main_theme.set_background_color_opacity(0.2)

menu = pygame_menu.Menu(300, 400, '',
                        theme=main_theme)

# кнопки в меню игры
menu.add_button('Играть', start_the_game)
menu.add_button('Выход', pygame_menu.events.EXIT)
#

while True:

    screen.blit(image, (0, 0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()

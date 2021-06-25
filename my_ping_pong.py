# импортируем библиотеку random
import random
from tkinter import *

# Добавляем глобальные переменные

# глобальные переменные
# настройки окна
width = 900
height = 300

# настройки ракеток

# ширина ракетки
pad_w = 10
# высота ракетки
pad_h = 100

# настройки мяча
# Насколько будет увеличиваться скорость мяча с каждым ударом
ball_speed_up = 1.1
# Максимальная скорость мяча
ball_max_speed = 40
# радиус мяча
ball_diameter = 30

initial_speed = 3
ball_x_speed = initial_speed * random.choice([-1, 1])
ball_y_speed = initial_speed

# Счет игроков
player_1_score = 0
player_2_score = 0

# Добавим глобальную переменную отвечающую за расстояние
# до правого края игрового поля
right_line_distance = width - pad_w


def update_score(player):
    global player_1_score, player_2_score
    if player == 'right':
        player_1_score += 1
        c.itemconfig(p_1_text, text=player_1_score)
    else:
        player_2_score += 1
        c.itemconfig(p_2_text, text=player_2_score)


# один из игроков пропустил мяч
def spawn_ball():
    global ball_x_speed
    global ball_y_speed
    # Выставляем мяч по центру
    c.coords(ball, width / 2 - ball_diameter / 2,
             height / 2 - ball_diameter / 2,
             width / 2 + ball_diameter / 2,
             height / 2 + ball_diameter / 2)
    # Задаем мячу направление в сторону проигравшего игрока,
    # но снижаем скорость до изначальной
    ball_x_speed = -(ball_x_speed * -initial_speed) / abs(ball_x_speed)
    ball_y_speed = -(ball_y_speed * -initial_speed) / abs(ball_y_speed) * random.choice([-1, 1]) * random.random()


# функция отскока мяча
def bounce(action):
    global ball_x_speed, ball_y_speed
    # ударили ракеткой
    if action == 'strike':
        if abs(ball_x_speed) < ball_max_speed:
            ball_x_speed *= -ball_speed_up
            if abs(ball_y_speed) < ball_max_speed:
                ball_y_speed = ball_x_speed * ball_speed_up * random.choice([-1, 1])
            else:
                ball_y_speed = ball_y_speed * random.choice([-1, 1])
        else:
            ball_x_speed = -ball_x_speed
            ball_y_speed = ball_x_speed * random.choice([-1, 1])
    else:
        ball_y_speed = -ball_y_speed


# устанавливаем окно
root = Tk()
root.title('Ping Pong')

# область анимации
c = Canvas(root, width=width, height=height, background='#003300')
c.pack()

# элементы игрового поля

# левая линия
c.create_line(pad_w, 0, pad_w, height, fill='white')
# правая линия
c.create_line(width - pad_w, 0, width - pad_w, height, fill='white')
# центральная линия
c.create_line(width / 2, 0, width / 2, height, fill='white')

# установка игровых объектов

# создаем мяч
ball = c.create_oval(width / 2 - ball_diameter / 2,
                     height / 2 + ball_diameter / 2,
                     width / 2 + ball_diameter / 2,
                     height / 2 - ball_diameter / 2, fill='white')

# левая ракетка
left_pad = c.create_line(pad_w / 2, 0, pad_w / 2, pad_h, width=pad_w, fill='yellow')

# правая ракетка
right_pad = c.create_line(width - pad_w / 2, 0, width - pad_w / 2,
                          pad_h, width=pad_w, fill='yellow')

p_1_text = c.create_text(width - width / 6, pad_h / 4,
                         text=player_1_score,
                         font='Arial 20',
                         fill='white')

p_2_text = c.create_text(width / 6, pad_h / 4,
                         text=player_2_score,
                         font='Arial 20',
                         fill='white')

# добавим глобальные переменные для скорости движения мяча
# по горизонтали
ball_x_change = 20
# по вертикали
ball_y_change = 0


def move_ball():
    # определяем координаты сторон мяча и его центра
    ball_left, ball_top, ball_right, ball_bot = c.coords(ball)
    ball_center = (ball_top + ball_bot) / 2

    # вертикальный отскок
    # Если мы далеко от вертикальных линий - просто двигаем мяч
    if ball_right + ball_x_speed < right_line_distance and \
            ball_left + ball_x_speed > pad_w:
        c.move(ball, ball_x_speed, ball_y_speed)
    # Если мяч касается своей правой или левой стороной границы поля
    elif ball_right == right_line_distance or ball_left == pad_w:
        # Проверяем правой или левой стороны мы касаемся
        if ball_right > width / 2:
            # Если правой, то сравниваем позицию центра мяча
            # с позицией правой ракетки.
            # И если мяч в пределах ракетки делаем отскок
            if c.coords(right_pad)[1] < ball_center < c.coords(right_pad)[3]:
                bounce('strike')
            else:
                # Иначе игрок пропустил - тут оставим пока pass, его мы заменим на подсчет очков и респаун мячика
                update_score('left')
                spawn_ball()
        else:
            # То же самое для левого игрока
            if c.coords(left_pad)[1] < ball_center < c.coords(left_pad)[3]:
                bounce('strike')
            else:
                update_score('right')
                spawn_ball()
    # Проверка ситуации, в которой мячик может вылететь за границы игрового поля.
    # В таком случае просто двигаем его к границе поля.
    else:
        if ball_right > width / 2:
            c.move(ball, right_line_distance - ball_right, ball_y_speed)
        else:
            c.move(ball, -ball_left + pad_w, ball_y_speed)
    # горизонтальный отскок
    if ball_top + ball_y_speed < 0 or ball_bot + ball_y_speed > height:
        bounce('ricochet')


# зададим глобальные переменные скорости движения ракеток
# скорось с которой будут ездить ракетки
pad_speed = 20
# скорость левой платформы
left_pad_speed = 0
# скорость правой ракетки
right_pad_speed = 0


# функция движения обеих ракеток
def move_pads():
    # для удобства создадим словарь, где ракетке соответствует ее скорость
    pads = { left_pad: left_pad_speed,
             right_pad: right_pad_speed }
    # перебираем ракетки
    for pad in pads:
        # двигаем ракетку с заданной скоростью
        c.move(pad, 0, pads[pad])
        # если ракетка вылезает за игровое поле возвращаем ее на место
        if c.coords(pad)[1] < 0:
            c.move(pad, 0, -c.coords(pad)[1])
        elif c.coords(pad)[3] > height:
            c.move(pad, 0, height - c.coords(pad)[3])


def main():
    move_ball()
    move_pads()
    # вызываем саму себя каждые 30 миллисекунд
    root.after(30, main)


# Установим фокус на Canvas чтобы он реагировал на нажатия клавиш
c.focus_set()


# Напишем функцию обработки нажатия клавиш
def movement_handler(event):
    global left_pad_speed, right_pad_speed
    if event.keysym == 'w':
        left_pad_speed = -pad_speed
    elif event.keysym == 's':
        left_pad_speed = pad_speed
    elif event.keysym == 'Up':
        right_pad_speed = -pad_speed
    elif event.keysym == 'Down':
        right_pad_speed = pad_speed


# Привяжем к Canvas эту функцию
c.bind('<KeyPress>', movement_handler)


# Создадим функцию реагирования на отпускание клавиши
def stop_pad(event):
    global left_pad_speed, right_pad_speed
    if event.keysym in 'ws':
        left_pad_speed = 0
    elif event.keysym in ('Up', 'Down'):
        right_pad_speed = 0


# Привяжем к Canvas эту функцию
c.bind('<KeyRelease>', stop_pad)

# запускаем движение
main()

# запускаем работу окна
root.mainloop()

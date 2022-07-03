# -*- coding: utf-8 -*-


import blessed
import time
import playsound as ps
import terminal_snake as ts


term = blessed.Terminal()


body2 = term.on_yellow4 + '  ' + term.normal
bg2 = term.on_snow3 + '  ' + term.normal
f2 = term.on_red + '  ' + term.normal
ct2 = {'head_u': body2, 'head_d': body2,
       'head_l': body2, 'head_r': body2,
       'tail_u': body2, 'tail_d': body2,
       'tail_l': body2, 'tail_r': body2,
       'empty': bg2, 'fruit': f2}


with term.fullscreen(), term.hidden_cursor():
    print(term.gold + 'SNAKE GAME' + term.normal)
    ps.playsound('start.mp3', False)
    time.sleep(2.7)

    input('Press ENTER to continue...')

    while True:
        print(term.clear, end='')
        length = input('Length: ')
        height = input('Height: ')

        try:
            length = int(length)
            height = int(height)
            break
        except ValueError:
            time.sleep(1)
            input('Length or height is not a number. Press ENTER to retry.')

    time.sleep(1)
    print(term.clear + 'Use ARROW keys to move. Press P to pause...')
    time.sleep(2)
    print(term.clear + term.normal)

    game = ts.Grid(length, height, ct2)
    snake = game.spawn_new_snake()
    snake.occupy_space()

    f_eaten = 0
    steps = 0
    s_list = [snake]
    f_list = []
    with term.cbreak(), term.hidden_cursor():
        while True:
            time.sleep(0.1)

            print(term.home, end='')

            if snake.out_of_grid(game):
                break

            if snake.is_head_tail_crash():
                break

            if f_list:
                for fruit in f_list:
                    if snake.eat_fruit(fruit):
                        f_eaten += 1
                        f_list.remove(fruit)
                        snake.grow_snake()
                        ps.playsound('eat.mp3', False)
                        break

            game.run_grid(s_list, f_list)
            game.print_grid_list()
            print(f'{steps} steps x {f_eaten} fruit')

            keypress = term.inkey(0.02)
            old_dir = snake.snake_body[0][1]

            if keypress == 'p' or keypress == 'P':
                while True:
                    keypress = term.inkey()
                    if keypress == 'p' or keypress == 'P':
                        break
            elif keypress.name == 'KEY_RIGHT' and old_dir != 'l':
                new_dir = 'r'
            elif keypress.name == 'KEY_LEFT' and old_dir != 'r':
                new_dir = 'l'
            elif keypress.name == 'KEY_UP' and old_dir != 'd':
                new_dir = 'u'
            elif keypress.name == 'KEY_DOWN' and old_dir != 'u':
                new_dir = 'd'
            else:
                new_dir = old_dir

            snake.move_snake(new_dir)
            steps += 1

            if steps % 5 == 0 and f_list == []:
                while True:
                    fruit = game.spawn_fruit()

                    intersect = ts.GameObject.is_intersect(fruit.coords_list)
                    if intersect == False:
                        f_list.append(fruit)
                        fruit.occupy_space()
                        break

    ps.playsound('end.mp3', False)
    time.sleep(2)

    print(term.white_on_firebrick4 + term.clear + 'GAME OVER')
    time.sleep(2)
    print(f'You have survived {steps} steps.')
    time.sleep(1)

    print(f'You have eaten {f_eaten} fruits')

    time.sleep(2)
    input('\nPress ENTER to continue...')




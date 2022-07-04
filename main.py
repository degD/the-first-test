# -*- coding: utf-8 -*-


import blessed
import time
import playsound as ps
import terminal_snake as ts
# playsound is a little library to play mp3 files.


term = blessed.Terminal()
# Blessed is a wrapper around the classic curses


# These are characters for the snake.
# on_color are backgrounds. While just color is foreground color,
# and in color1_on_color2 color1 is foreground and color2 is background.
# It's like saying color1 on color2.
body2 = term.on_yellow4 + '  ' + term.normal
bg2 = term.on_snow3 + '  ' + term.normal
f2 = term.on_red + '  ' + term.normal
ct2 = {'head_u': body2, 'head_d': body2,
       'head_l': body2, 'head_r': body2,
       'tail_u': body2, 'tail_d': body2,
       'tail_l': body2, 'tail_r': body2,
       'empty': bg2, 'fruit': f2}


# term.fullscreen() saves your current console (terminal) screen, and
# restores it when you exit.
# term.hidden_cursor() hides the cursor.
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
        
        if length < 3 or height < 3:
            time.sleep(1)
            input('Length and height should be less than three. Press ENTER to retry.')

    time.sleep(1)
    print(term.clear + 'Use ARROW keys to move. Press P to pause...')
    time.sleep(2)
    print(term.clear + term.normal)
    # Prompting and taking the data thus far.

    game = ts.Grid(length, height, ct2)
    snake = game.spawn_new_snake()
    snake.occupy_space()
    # Creating some game objects and getting ready.

    f_eaten = 0
    steps = 0
    s_list = [snake]
    f_list = []
    # Sone in-game variables. f_eaten == number of fruits eaten.
    # Each step is a full turn of the following loop.
    # term.cbreak() makes it so each character can be inputted without
    # pressing the ENTER, using the special term.inkey() method.
    with term.cbreak(), term.hidden_cursor():
        while True:
            time.sleep(0.2)

            print(term.home, end='')

            # If snake crash, then game over.
            if snake.out_of_grid(game):
                break
            if snake.is_head_tail_crash():
                break
            
            # If there is no space left to move, than also game over.
            # That it because there might be a bug with the 
            # fruit spawner, that might cause an infinite loop.
            # If the spawner tries to spawn a fruit, when there is exactly no space left,
            # then of course it won't be able find an appropriate place, which will cause the loop.
            if length*height == ts.GameObject.occupied_number():
                break
            
            # Checks whether the fruit exist or not, and if it does,
            # if snake is in a position to eat it or not, which is basically
            # asking if head and fruit are on the same coordinates or not.
            # Eats the fruit and grows the snake if that is true.
            if f_list:
                for fruit in f_list:
                    if snake.eat_fruit(fruit):
                        f_eaten += 1
                        f_list.remove(fruit)
                        snake.grow_snake()
                        ps.playsound('eat.mp3', False)
                        break
            
            # Printing the game area, or grid.
            game.run_grid(s_list, f_list)
            game.print_grid_list()
            print(f'{steps} steps x {f_eaten} fruit')

            # Taking the keypress, 0.02 is timeout.
            keypress = term.inkey(0.02)
            old_dir = snake.snake_body[0][1]

            # Pauses if keypress is p/P and waits until p/P pressed again.
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
            # Snake can only turn by 90 degrees. Snake cannot and will not do any 180 turns. 
            # Pressing any other key except r,l,u,d or not pressing at all before the timeout will
            # make the snake to keep going to that location.

            snake.move_snake(new_dir)
            steps += 1

            # Spawn a fruit every 5 steps if there isn't any other fruit.
            if steps % 5 == 0 and f_list == []:
                while True:
                    fruit = game.spawn_fruit()

                    # Fruit's coordinates are randomly chosen.
                    # So checking them to be sure no intersection will happen.
                    intersect = ts.GameObject.is_intersect(fruit.coords_list)
                    if intersect == False:
                        f_list.append(fruit)
                        fruit.occupy_space()
                        break
    
    # End sound and screen.
    ps.playsound('end.mp3', False)
    time.sleep(2)

    print(term.white_on_firebrick4 + term.clear + 'GAME OVER')
    
    time.sleep(2) 
    print(f'You have survived {steps} steps.')
    time.sleep(1)
    print(f'You have eaten {f_eaten} fruits')

    time.sleep(1)
    ps.playsound('eat.mp3', False)
    if length*height == ts.GameObject.occupied_number():
        print('You won the game!')
    # This is equal to covering every coordinate over the grid.
    # Which is, infact, really hard. It's a victory.
    
    time.sleep(2)
    input('\nPress ENTER to continue...')

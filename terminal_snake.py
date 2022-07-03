# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 09:33:21 2022

@author: degD

This file consists of classes and functions for the game
"""


import random


class Grid:
    """
    Class for the game area.
    """

    def __init__(self, length, height, char_dict):
        """
        Class for the game area.
        Assumes LengthxHeight is size of the area.
        char_dict is a dict that stores the symbols for the game.
        """
        # Because length and height give the size, they should start from 1, instead of 0.
        if length < 3 or height < 3:  # Or there wouldn't be enough space for the snake
            raise ValueError('All arguments should be greater or equal to 3.')
        self.grid_area = (length, height)
        
        self.char_dict = char_dict
        # char_dict example:
        # ct1 = {'head_u': '^', 'head_d': 'v',
        #        'head_l': '<', 'head_r': '>',
        #        'tail_u': '|', 'tail_d': '|',
        #        'tail_l': '-', 'tail_r': '-',
        #        'empty': '*', 'fruit': 'p'}
        
        self.empty_grid_list = []
        self.create_empty_grid_list()
        # empty_grid_list is a list that consists of only the 'empty' symbols.
        # It is created as a LengthxHeight matrix, using lists.

        self.grid_list = []
        # First, a swallow (and deep) copy of empty_grid_list is created.
        # Then game objects, such as snake and fruit, will be placed on it.

    def spawn_new_snake(self):
        """
        Returns a new snake object. Its section coordinates are chosen
        randomly and of course, next to each other.
        """
        head_x = random.randint(1, self.grid_area[0]-2)
        head_y = random.randint(1, self.grid_area[1]-2)
        # Choosing a random coordinate for the snakes head.

        # Then choosing another coordinate next to head.
        tail_coords = random.choice(((head_x-1, head_y), 
                                    (head_x+1, head_y), 
                                    (head_x, head_y-1), 
                                    (head_x, head_y+1)))

        tail_x = tail_coords[0]
        tail_y = tail_coords[1]

        # Creating a snake object.
        return Snake((head_x, head_y), (tail_x, tail_y))

    def spawn_fruit(self):
        """
        Returns a fruit object. Its coordinates are chosen randomly
        from the grid.
        """
        fruit_x = random.randint(1, self.grid_area[0]-2)
        fruit_y = random.randint(1, self.grid_area[1]-2)
        
        return Fruit((fruit_x, fruit_y))

    def create_empty_grid_list(self):
        """
        Creates the empty_grid_list from length and height.
        """
        length = self.grid_area[0]
        height = self.grid_area[1]
        
        symbol_empty = self.char_dict['empty']

        # Here, creating row lists and putting them in a bigger list, creating a matrix.
        row = [symbol_empty for _ in range(length)]
        self.empty_grid_list = [list(row) for _ in range(height)]  # list(row) to prevent list mutation.

    def copy_empty_grid(self):
        """
        Refreshes grid_list to empty_grid_list.
        """
        self.grid_list = []
        for row in self.empty_grid_list:
            self.grid_list.append(row[:])
        # Doing this instead of just using list.copy.
        # That's because inner lists are not getting copied otherwise.

    def add_snake_to_grid_list(self, snake):
        """
        Assumes snake is a Snake object.
        Add the symbols of snake's sections to the grid_list.
        Raises a ValueError if grid_list == [].
        """
        if not self.grid_list:
            raise ValueError('grid_list should be created.')

        # Helper function to add a symbol to grid.
        def add_to_grid(x, y, symbol):
            self.grid_list[y][x] = symbol
        
        head_sect = snake.snake_body[0]
        head_x, head_y = head_sect[0][0], head_sect[0][1]
        head_dir = head_sect[1]
        head_symbol = self.char_dict['head_'+head_dir]
        add_to_grid(head_x, head_y, head_symbol)
        
        for sect in snake.snake_body[1:]:
            sect_x, sect_y = sect[0][0], sect[0][1]
            # *_dir is either r,l,u,d
            sect_dir = sect[1]
            sect_symbol = self.char_dict['tail_'+sect_dir]
            add_to_grid(sect_x, sect_y, sect_symbol)

    def add_fruit_to_grid(self, fruit):
        """
        Assumes fruit is a Fruit object.
        Add the symbol for fruit.
        Raises a ValueError if grid_list == [].
        """
        if not self.grid_list:
            raise ValueError('grid_list should be created.')
            
        x, y = fruit.coords_list[0][0], fruit.coords_list[0][1]
        symbol = self.char_dict['fruit']
        
        self.grid_list[y][x] = symbol

    def print_grid_list(self):
        """
        Print the grid_list as a string.
        """
        res = ''

        # Combining grid_list in res
        for row in self.grid_list:
            res += ''.join(row)
            res += '\n'

        print(res, end='')

    def run_grid(self, snakes_iter, fruits_iter):
        """
        Assumes snake_iter and fruit_iter are iterables that contain
        Snake and Fruit objects, respectively.
        Raises a ValueError if grid_list == [].
        Refreshes the grid_list and adds game objects to it.
        """
        if not self.empty_grid_list:
            raise ValueError('empty_grid_list should be created.')
        
        self.copy_empty_grid()
        
        for snake in snakes_iter:
            self.add_snake_to_grid_list(snake)
        
        for fruit in fruits_iter:
            self.add_fruit_to_grid(fruit)
        

class GameObject:
    """Class for game objects."""
    occupied_coordinates = {}
    # This dict stores all the coordinates of game objects.
    
    def __init__(self):
        self.obj_index = len(GameObject.occupied_coordinates)

    def occupy_space(self):
        i = self.obj_index
        GameObject.occupied_coordinates[i] = self.coords_list

    def empty_space(self):
        i = self.obj_index
        GameObject.occupied_coordinates.pop(i)

    def update_space(self):
        i = self.obj_index
        GameObject.occupied_coordinates[i] = self.coords_list
    
    # Checks if any coordinate from the given coords_list already exists in the
    # occupied_coordinates dictionary.
    @classmethod
    def is_intersect(cls, new_coords_list):
        for new_coord in new_coords_list:
            for occu_list in GameObject.occupied_coordinates:
                if new_coord in occu_list:
                    return True
        return False
    

class Snake(GameObject):
    """
    Snake, the main protagonist of the game.
    """
    def __init__(self, *sections_coords):
        """
        Snake, the main protagonist of the game.
        Assumes Snake object is instanced with at least 2 coordinate tuples.
        Raises a ValueError instead.
        """
        # It should be at least 2 sections long to be created.
        if len(sections_coords) < 2:
            raise ValueError

        # A list that contains coordinates of sections.
        self.coords_list = list(sections_coords)
        GameObject.__init__(self)
        
        self.snake_len = len(sections_coords)

        # snake_body is a list that contains information about sections.
        self.snake_body = []
        
        for i in range(self.snake_len-1):
            current_section = sections_coords[i]
            next_section = sections_coords[i+1]
            
            curr_x, curr_y = current_section[0], current_section[1]
            next_x, next_y = next_section[0], next_section[1]
            
            if curr_x > next_x:
                snake_section = ((curr_x, curr_y), 'r')
            elif curr_x < next_x:
                snake_section = ((curr_x, curr_y), 'l')
            elif curr_y > next_y:
                snake_section = ((curr_x, curr_y), 'd')
            elif curr_y < next_y:
                snake_section = ((curr_x, curr_y), 'u')
            
            self.snake_body.append(snake_section)
        
        last_section = sections_coords[-1]
        prev_section = sections_coords[-2]
        
        last_x, last_y = last_section[0], last_section[1]
        prev_x, prev_y = prev_section[0], prev_section[1]
        
        if prev_x > last_x:
            snake_section = ((last_x, last_y), 'r')
        elif prev_x < last_x:
            snake_section = ((last_x, last_y), 'l')
        elif prev_y > last_y:
            snake_section = ((last_x, last_y), 'd')
        elif prev_y < last_y:
            snake_section = ((last_x, last_y), 'u')
        
        self.snake_body.append(snake_section)

    def set_coords_list(self):
        self.coords_list = []
        
        for sect in self.snake_body:
            self.coords_list.append(sect[0])

    def move_snake(self, new_dir):
        
        def update_coords(sect, new_dir):
            coords = sect[0]
            x, y = coords[0], coords[1]
            
            if new_dir == 'u':
                y -= 1
            elif new_dir == 'd':
                y += 1
            elif new_dir == 'l':
                x -= 1
            elif new_dir == 'r':
                x += 1
            
            return (x, y), new_dir
        
        for i in range(self.snake_len):
            sect = self.snake_body[i]
            old_dir = sect[1]
            
            new_sect = update_coords(sect, new_dir)
            self.snake_body[i] = new_sect
            
            new_dir = old_dir
        
        self.set_coords_list()
        self.update_space()

    def grow_snake(self):
        sect = self.snake_body[-1]
        x, y = sect[0][0], sect[0][1]
        
        if sect[1] == 'u':
            y += 1
        elif sect[1] == 'd':
            y -= 1
        elif sect[1] == 'l':
            x += 1
        elif sect[1] == 'r':
            x -= 1
        
        new_sect = ((x, y), sect[1])
        self.snake_body.append(new_sect)

        self.snake_len += 1
        self.set_coords_list()
        self.update_space()

    def eat_fruit(self, fruit):
        """
        Checks if head of the snake and fruit appear on the same coordinates.

        :param fruit: Assumes fruit is a Fruit object
        :return:
        Returns True if head of the snake and fruit appear on the same coordinates.
        Also removes fruit from the occupied_coordinates list. Returns False otherwise.
        """
        head_coords = self.coords_list[0]
        fruit_coords = fruit.coords_list[0]

        if head_coords == fruit_coords:
            fruit.empty_space()
            return True
        else:
            return False

    def is_head_tail_crash(self):
        """

        :return:
        """
        head_coords = self.coords_list[0]

        for coords in self.coords_list[1:]:
            if head_coords == coords:
                return True
        return False

    def out_of_grid(self, grid):
        head_coords = self.coords_list[0]
        head_x, head_y = head_coords[0], head_coords[1]

        grid_length = grid.grid_area[0]
        grid_height = grid.grid_area[1]

        if (-1 < head_x < grid_length) and (-1 < head_y < grid_height):
            return False
        else:
            return True


class Fruit(GameObject):
    def __init__(self, coords):
        self.coords_list = [coords]
        GameObject.__init__(self)

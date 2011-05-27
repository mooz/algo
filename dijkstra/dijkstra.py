#!/usr/bin/env python

import pprint
import sys

class Cell(object):
    def __init__(self, x, y, score = None, done = False, prev = None, wall = False):
        self.x = x
        self.y = y
        self.score = score
        self.done = done
        self.prev = prev
        self.wall = wall

    def __str__(self):
        if self.wall:
            return "[WALL]"
        str_represent = "%4s" % str(self.score)
        if self.done:
            str_represent = " {0}*".format(str_represent)
        else:
            str_represent = " {0} ".format(str_represent)
        return str_represent

def create_field(size_x, size_y):
    return [[Cell(x, y) for y in range(0, size_y)] for x in range(0, size_x)]

def access_field(field, x, y):
    if x < 0 or y < 0:
        return None
    try:
        cell = field[x][y]
        # skip wall
        return None if cell.wall else cell
    except IndexError:
        return None

def trail_sibling(field, cell, x, y):
    target = access_field(field, x, y)
    if target is None:
        return
    next_score = cell.score + 1         # distance is fixed to 1
    if target.score is None or next_score < target.score:
        target.prev = cell
        target.score = next_score

def trail_from(field, cell):
    trail_sibling(field, cell, cell.x + 1, cell.y)
    trail_sibling(field, cell, cell.x - 1, cell.y)
    trail_sibling(field, cell, cell.x, cell.y - 1)
    trail_sibling(field, cell, cell.x, cell.y + 1)

def get_next_cell(field):
    next_cell = None
    for row in field:
        for cell in row:
            if cell.done or cell.score is None:
                continue
            if next_cell is None or next_cell.score > cell.score:
                next_cell = cell
    return next_cell

def print_field(field):
    print("\n".join([", ".join([str(cell) for cell in row]) for row in field]))

def dijkstra(field):
    while True:
        cell = get_next_cell(field)
        if cell is None:
            break
        trail_from(field, cell)
        cell.done = True
        print_field(field)
        print("--------------------------------------------------")

if __name__ == "__main__":
    maze = create_field(6, 6)
    maze[0][0].score = 0
    maze[0][2].wall = True
    maze[3][2].wall = True
    maze[1][5].wall = True
    dijkstra(maze)
    print_field(maze)

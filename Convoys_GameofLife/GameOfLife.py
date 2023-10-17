#!/usr/bin/python3

import curses
import random
import time
import copy


def GameOfLife(stdscr):
    k = 0
    cursor_x, cursor_y = 0, 0
    generations = 0
    grid = []
    height, width = stdscr.getmaxyx()
    rows, cols = int(height-2), width
    speed = .2
    pause = False

    stdscr.clear()
    stdscr.refresh()

    # colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    def initialize():
        return [[False for _ in range(cols)] for _ in range(rows)]

    def seed():
        grid = initialize()
        for i in range(rows):
            for j in range(cols):
                if int(random.random() * 4) == 0:
                    grid[i][j] = True
        return grid

    def play(grid):
        noOfCellsAlive = 0
        nGrid = copy.deepcopy(grid)
        dR = [1, 1, 1, -1, -1, -1, 0, 0]
        dC = [1, 0, -1, -1, 0, 1, 1, -1]

        def isValid(r, c) -> bool:
            return (r >= 0 and r < rows and c >= 0 and c < cols)

        for i in range(rows):
            for j in range(cols):
                count = 0
                for r1, c1 in zip(dR, dC):
                    r = r1+i
                    c = c1+j

                    if isValid(r, c) and grid[r][c]:
                        count += 1

                if grid[i][j] and (count < 2 or count > 3):
                    nGrid[i][j] = False
                if grid[i][j] == False and count == 3:
                    nGrid[i][j] = True

                noOfCellsAlive += nGrid[i][j]

        return [nGrid, noOfCellsAlive]

    # Inception
    grid = seed()

    while True:
        # Initialization
        stdscr.clear()
        stdscr.nodelay(1)
        nHeight, nWidth = stdscr.getmaxyx()

        generations += 1

        # If windows dimension changes #responsive :)
        if ((nHeight != height) or (nWidth != width)):
            height, width = nHeight, nWidth
            rows, cols = int(height-3), width
            grid = seed()

        # Simulating Generations
        grid, noOfCellsAlive = play(grid)

        # Menu Cmds
        if k == ord('q'):
            break
        elif k == ord('r'):
            grid = seed()
            generations = 0
        elif k == ord('f'):
            speed = 0.1
        elif k == ord('s'):
            speed = 1

        # Displaying grid
        stdscr.attron(curses.color_pair(1))
        stdscr.attron(curses.A_BOLD)
        for i in range(rows):
            for j in range(cols):
                stdscr.addstr(i, j, chr(0x2B1A) if grid[i][j] else ' ')

        stdscr.attroff(curses.color_pair(1))
        stdscr.attroff(curses.A_BOLD)

        # Declaration of strings
        title = 'Game Of Life'
        credits = 'By @zeal2end'
        statusbarstr = "Exit: 'q' | Seed: 'r' | Fast: 'f' | Slow: 's' | Genration: {} | Alive Cells: {}".format(
            generations, noOfCellsAlive)

        # calculations
        start_x_title = 0
        start_x_credit = width - len(credits) - 1
        start_y = int(height - 2)

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))

        # Rendering title
        stdscr.addstr(start_y, start_x_title, title)
        stdscr.addstr(start_y, start_x_credit, credits)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))

        # Refresh the screen
        stdscr.refresh()
        time.sleep(speed)

        # Wait for next input
        k = stdscr.getch()


def main():
    curses.wrapper(GameOfLife)


if __name__ == "__main__":
    main()
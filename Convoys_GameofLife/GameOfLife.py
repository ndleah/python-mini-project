#!/usr/bin/python3

import curses
import random
import time
import copy


def GameOfLife(stdscr):
    k = 0
    generations = 0
    height, width = stdscr.getmaxyx()
    rows, cols = max(1, height - 3), max(1, width - 1)
    speed = 0.2
    pause = False

    stdscr.clear()
    stdscr.refresh()

    # colors in curses
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    def initialize():
        return [[False for _ in range(cols)] for _ in range(rows)]

    def seed():
        grid = initialize()
        for i in range(rows):
            for j in range(cols):
                if random.random() < 0.25:
                    grid[i][j] = True
        return grid

    def play(grid):
        noOfCellsAlive = 0
        nGrid = copy.deepcopy(grid)
        dR = [1, 1, 1, -1, -1, -1, 0, 0]
        dC = [1, 0, -1, -1, 0, 1, 1, -1]

        def isValid(r, c) -> bool:
            return (0 <= r < rows and 0 <= c < cols)

        for i in range(rows):
            for j in range(cols):
                count = 0
                for r1, c1 in zip(dR, dC):
                    r = r1 + i
                    c = c1 + j
                    if isValid(r, c) and grid[r][c]:
                        count += 1

                if grid[i][j] and (count < 2 or count > 3):
                    nGrid[i][j] = False
                elif not grid[i][j] and count == 3:
                    nGrid[i][j] = True

                if nGrid[i][j]:
                    noOfCellsAlive += 1

        return nGrid, noOfCellsAlive

    def safe_addstr(y, x, str_content, attr=0):
        """Safely write string to curses window without boundary overflow crash."""
        if y < 0 or y >= height or x < 0 or x >= width:
            return
        max_len = width - x - 1
        if max_len <= 0:
            return
        try:
            stdscr.addstr(y, x, str_content[:max_len], attr)
        except curses.error:
            pass

    # Inception
    grid = seed()
    noOfCellsAlive = sum(sum(1 for cell in row if cell) for row in grid)

    while True:
        stdscr.clear()
        stdscr.nodelay(1)
        nHeight, nWidth = stdscr.getmaxyx()

        # Handle window resize
        if (nHeight != height) or (nWidth != width):
            height, width = nHeight, nWidth
            rows, cols = max(1, height - 3), max(1, width - 1)
            grid = seed()

        # Handle commands
        if k == ord('q'):
            break
        elif k == ord('r'):
            grid = seed()
            generations = 0
            pause = False
        elif k == ord('f'):
            speed = 0.05
        elif k == ord('s'):
            speed = 0.5
        elif k == ord('p') or k == ord(' '):
            pause = not pause

        # Simulate Generation if not paused
        if not pause:
            generations += 1
            grid, noOfCellsAlive = play(grid)

        # Displaying grid
        color_attr = curses.color_pair(1) | curses.A_BOLD
        for i in range(min(rows, height - 3)):
            for j in range(min(cols, width - 1)):
                if grid[i][j]:
                    safe_addstr(i, j, '#', color_attr)

        # Status strings
        title = 'Game Of Life'
        credits = 'By @zeal2end'
        pause_str = ' [PAUSED]' if pause else ''
        statusbarstr = "Exit: 'q' | Reset: 'r' | Pause: 'p'/'Space' | Fast: 'f' | Slow: 's' | Gen: {}{} | Alive: {}".format(
            generations, pause_str, noOfCellsAlive)

        start_x_title = 0
        start_x_credit = max(0, width - len(credits) - 1)
        start_y = max(0, height - 2)

        # Render status bar
        safe_addstr(height - 1, 0, statusbarstr, curses.color_pair(3))

        # Render title & credits
        safe_addstr(start_y, start_x_title, title, curses.color_pair(2))
        safe_addstr(start_y, start_x_credit, credits, curses.color_pair(2))

        stdscr.refresh()
        time.sleep(speed)

        k = stdscr.getch()


def main():
    curses.wrapper(GameOfLife)


if __name__ == "__main__":
    main()
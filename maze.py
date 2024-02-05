import random
import time
from cell import Cell


class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y,
                 win=None, seed=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []

        if seed is not None:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x = self._x1 + i * self._cell_size_x
        y = self._y1 + j * self._cell_size_y
        x2 = x + self._cell_size_x
        y2 = y + self._cell_size_y

        cell = self._cells[i][j]
        cell.draw(x, y, x2, y2)
        self._animate()

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows -
                                        1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.01)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True

        while True:
            directions = []

            if i > 0 and not self._cells[i-1][j].visited:
                directions.append(("left", i-1, j))
            if j > 0 and not self._cells[i][j-1].visited:
                directions.append(("up", i, j-1))
            if i < self._num_cols-1 and not self._cells[i+1][j].visited:
                directions.append(("right", i+1, j))
            if j < self._num_rows-1 and not self._cells[i][j+1].visited:
                directions.append(("down", i, j+1))

            if not directions:
                self._draw_cell(i, j)
                return

            direction, next_i, next_j = random.choice(directions)

            if direction == "left":
                self._cells[i][j].has_left_wall = False
                self._cells[next_i][next_j].has_right_wall = False
            elif direction == "right":
                self._cells[i][j].has_right_wall = False
                self._cells[next_i][next_j].has_left_wall = False
            elif direction == "up":
                self._cells[i][j].has_top_wall = False
                self._cells[next_i][next_j].has_bottom_wall = False
            elif direction == "down":
                self._cells[i][j].has_bottom_wall = False
                self._cells[next_i][next_j].has_top_wall = False

            # Recursively call _break_walls_r for the next cell
            self._break_walls_r(next_i, next_j)

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        current_cell = self._cells[i][j]
        current_cell.visited = True

        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        directions = {
            "left": (i-1, j),
            "up": (i, j-1),
            "right": (i+1, j),
            "down": (i, j+1)
        }

        for direction, (next_i, next_j) in directions.items():
            # Check if the next cell is within bounds and not blocked by a wall
            if 0 <= next_i < self._num_cols and 0 <= next_j < self._num_rows and \
               not self._is_wall_blocking(current_cell, direction) and \
               not self._cells[next_i][next_j].visited:

                current_cell.draw_move(self._cells[next_i][next_j])
                if self._solve_r(next_i, next_j):
                    return True
                else:
                    current_cell.draw_move(
                        self._cells[next_i][next_j], undo=True)

        return False

    def _is_wall_blocking(self, cell, direction):
        if direction == "left":
            return cell.has_left_wall
        elif direction == "up":
            return cell.has_top_wall
        elif direction == "right":
            return cell.has_right_wall
        elif direction == "down":
            return cell.has_bottom_wall
        return True

    def reset_maze(self):
        if self._win:
            self._win.get_canvas().delete("all")

        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()

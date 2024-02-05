import unittest
from maze import Maze
from cell import Cell


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_different_dimensions(self):
        m2 = Maze(0, 0, 5, 15, 20, 20)
        self.assertEqual(len(m2._cells), 15)
        self.assertEqual(len(m2._cells[0]), 5)

    def test_maze_edge_cases(self):
        m1 = Maze(0, 0, 1, 1, 10, 10)
        self.assertEqual(len(m1._cells), 1)
        self.assertEqual(len(m1._cells[0]), 1)

        m2 = Maze(0, 0, 1, 2, 10, 10)
        self.assertEqual(len(m2._cells), 2)
        self.assertEqual(len(m2._cells[0]), 1)

    def test_cell_access(self):
        m = Maze(0, 0, 4, 4, 10, 10)
        cell = m._cells[1][1]
        self.assertIsInstance(cell, Cell)

    def test_maze_break_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            m1._cells[0][0].has_top_wall,
            False,
        )
        self.assertEqual(
            m1._cells[num_cols - 1][num_rows - 1].has_bottom_wall,
            False,
        )

    def test_reset_cells_visited(self):
        m = Maze(0, 0, 5, 5, 10, 10)
        # Mark a few cells as visited
        m._cells[0][0].visited = True
        m._cells[1][1].visited = True
        m._cells[2][2].visited = True

        m._reset_cells_visited()

        # Check if all cells are reset to visited = False
        for i in range(5):
            for j in range(5):
                self.assertFalse(m._cells[i][j].visited)


if __name__ == "__main__":
    unittest.main()

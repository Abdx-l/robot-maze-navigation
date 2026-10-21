import unittest
from maze import Maze, Robot, explore, replay


class MazeTests(unittest.TestCase):
    def test_sensors_and_route(self):
        maze = Maze("#####\n#S.G#\n#####")
        robot = Robot(maze)
        self.assertEqual(robot.sensors(), {"front": False, "left": False, "right": True})
        route, visited, _ = explore(maze)
        self.assertEqual(route, [1, 1])
        self.assertEqual(len(visited), 3)
        self.assertEqual(replay(maze, route), ["TURN_RIGHT", "FORWARD", "FORWARD"])

    def test_backtracking(self):
        maze = Maze("########\n#S..####\n#.######\n#....G##\n########")
        route, visited, commands = explore(maze)
        self.assertEqual(len(route), 6)
        self.assertGreater(len(visited), len(route) + 1)
        self.assertIn("TURN_AROUND", commands)
        self.assertTrue(replay(maze, route))

    def test_unreachable_and_invalid(self):
        with self.assertRaises(ValueError): explore(Maze("#####\n#S#G#\n#####"))
        with self.assertRaises(ValueError): Maze("S.G\n##")
        with self.assertRaises(ValueError): Maze("S..")

    def test_collision(self):
        robot = Robot(Maze("#####\n#S.G#\n#####"))
        with self.assertRaises(ValueError): robot.move(0)


if __name__ == "__main__":
    unittest.main()


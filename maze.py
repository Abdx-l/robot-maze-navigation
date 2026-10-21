import argparse
from pathlib import Path

DIRS = ((0, -1), (1, 0), (0, 1), (-1, 0))  # N E S W
NAMES = "NESW"


class Maze:
    def __init__(self, text):
        lines = text.splitlines()
        if not lines or any(len(row) != len(lines[0]) for row in lines):
            raise ValueError("maze must be nonempty and rectangular")
        if any(char not in "#.SG" for row in lines for char in row):
            raise ValueError("invalid maze cell")
        starts = [(x, y) for y, row in enumerate(lines) for x, c in enumerate(row) if c == "S"]
        goals = [(x, y) for y, row in enumerate(lines) for x, c in enumerate(row) if c == "G"]
        if len(starts) != 1 or len(goals) != 1:
            raise ValueError("maze needs exactly one start and goal")
        self.lines, self.start, self.goal = lines, starts[0], goals[0]

    def open(self, position):
        x, y = position
        return 0 <= y < len(self.lines) and 0 <= x < len(self.lines[0]) and self.lines[y][x] != "#"


class Robot:
    def __init__(self, maze):
        self.maze = maze
        self.position = maze.start
        self.heading = 0
        self.commands = []

    def neighbor(self, direction):
        x, y = self.position
        dx, dy = DIRS[direction]
        return x + dx, y + dy

    def sensors(self):
        return {relative: self.maze.open(self.neighbor((self.heading + offset) % 4))
                for relative, offset in (("front", 0), ("left", -1), ("right", 1))}

    def move(self, direction):
        if not self.maze.open(self.neighbor(direction)):
            raise ValueError("collision")
        delta = (direction - self.heading) % 4
        if delta == 1: self.commands.append("TURN_RIGHT")
        elif delta == 2: self.commands.append("TURN_AROUND")
        elif delta == 3: self.commands.append("TURN_LEFT")
        self.heading = direction
        self.position = self.neighbor(direction)
        self.commands.append("FORWARD")


def explore(maze):
    robot = Robot(maze)
    visited = {maze.start}
    route = []

    def search():
        if robot.position == maze.goal:
            return True
        # Only inspect open corridors through relative sensor observations.
        for offset, sensor in ((-1, "left"), (0, "front"), (1, "right")):
            direction = (robot.heading + offset) % 4
            candidate = robot.neighbor(direction)
            if robot.sensors()[sensor] and candidate not in visited:
                previous = robot.heading
                robot.move(direction)
                visited.add(candidate)
                route.append(direction)
                if search(): return True
                route.pop()
                robot.move((direction + 2) % 4)
                # Return to the old orientation; turning in place is represented
                # as an instruction for a differential-drive controller.
                delta = (previous - robot.heading) % 4
                if delta == 1: robot.commands.append("TURN_RIGHT")
                elif delta == 2: robot.commands.append("TURN_AROUND")
                elif delta == 3: robot.commands.append("TURN_LEFT")
                robot.heading = previous
        # The cell behind is physically reachable after entering a corridor.
        # Consider it only if it has not been visited (start has no such cell).
        direction = (robot.heading + 2) % 4
        candidate = robot.neighbor(direction)
        if maze.open(candidate) and candidate not in visited:
            previous = robot.heading
            robot.move(direction)
            visited.add(candidate)
            route.append(direction)
            if search(): return True
            route.pop()
            robot.move((direction + 2) % 4)
            delta = (previous - robot.heading) % 4
            if delta == 1: robot.commands.append("TURN_RIGHT")
            elif delta == 2: robot.commands.append("TURN_AROUND")
            elif delta == 3: robot.commands.append("TURN_LEFT")
            robot.heading = previous
        return False

    if not search():
        raise ValueError("goal is unreachable")
    return route, visited, robot.commands


def replay(maze, route):
    robot = Robot(maze)
    for direction in route:
        robot.move(direction)
    if robot.position != maze.goal:
        raise ValueError("route does not reach goal")
    return robot.commands


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("map", type=Path)
    args = parser.parse_args()
    try:
        maze = Maze(args.map.read_text(encoding="utf-8"))
        route, visited, exploration = explore(maze)
        print("Visited:", len(visited))
        print("Route:", " ".join(NAMES[d] for d in route))
        print("Exploration commands:", len(exploration))
        print("Replay:", " ".join(replay(maze, route)))
    except (OSError, ValueError) as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    main()


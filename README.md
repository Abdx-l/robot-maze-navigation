# Robot Maze Navigation

A sensor-driven maze exploration and route-learning model for a differential-drive robot. The controller sees only the three cells in front, left, and right of its current heading. It explores with depth-first search, records the first path to the goal, and can replay that path without exploration. A small HCS12-style assembly controller in `firmware/controller.asm` shows the sensor-to-motor state interface; port addresses and timing must be adapted to a real board.

## Run

```sh
python maze.py examples/maze.txt
python -m unittest discover -s tests -v
```

Map legend: `#` wall, `.` corridor, `S` start, `G` goal. The simulator reports visited cells, learned route, and motor-level turn/forward commands. It verifies that replay reaches the goal. This is a software model, not a claim of physical sensor calibration or deployment.

The assembly module expects bumper/IR-derived obstruction bits on `SENSOR_PORT` (bit 0 front, bit 1 left, bit 2 right), and emits motor command codes on `MOTOR_PORT`. `GOAL_PORT` bit 0 stops the robot. The controller is an integration scaffold: map the symbols to the target HCS12 memory map and provide turn-completion feedback before driving motors.


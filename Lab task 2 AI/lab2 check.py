# lab2_check.py
# Lab 2 - checks the stateful agent and tests a noisy sequence near 26.
# Run with:  python lab2_check.py

from lab2_model import StatefulClassroomAgent

# Part 1: a few quick checks with expected answers written first
agent = StatefulClassroomAgent()
checks = [
    ((29, True), ("COOL", True)),
    ((29, True), ("COOL", False)),
    ((20, True), ("IDLE", True)),
    ((26, True), ("IDLE", False)),
    ((19, True), ("WARM", True)),
    ((29, False), ("ECO", True)),
]

passed = 0
for percept, expected in checks:
    actual = agent.act(*percept)
    ok = actual == expected
    if ok:
        passed += 1
    print(percept, "expected", expected, "got", actual, "OK" if ok else "WRONG")
print(passed, "of", len(checks), "checks passed")

# Part 2: noisy readings around 26 degrees
print()
print("noisy sequence around 26")
noisy = StatefulClassroomAgent()
readings = [25.9, 26.1, 25.9, 26.1, 25.9, 26.1]
commands = 0
for temp in readings:
    target, send = noisy.act(temp, True)
    if send:
        commands += 1
    print(temp, target, "command sent" if send else "no command")
print("commands sent:", commands, "out of", len(readings), "readings")

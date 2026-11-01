# lab2_model.py
# Lab 2, Task 3 - classroom agent that remembers its previous mode.
# Run with:  python lab2_model.py
#
# The thresholds and the empty room priority are the same as before.
# The only new thing is that act() now returns two values: the target mode
# and a flag that says if a new command really needs to be sent.


class StatefulClassroomAgent:
    def __init__(self):
        self.previous_mode = None   # nothing has been sent yet

    def decide(self, temp, occupied):
        # same rules as the reflex agent
        if not occupied:
            return "ECO"
        if temp > 26:
            return "COOL"
        if temp < 20:
            return "WARM"
        return "IDLE"

    def act(self, temp, occupied):
        target = self.decide(temp, occupied)
        send = target != self.previous_mode
        self.previous_mode = target
        return target, send


if __name__ == "__main__":
    agent = StatefulClassroomAgent()

    percepts = [
        (29, True),    # first percept, should send COOL
        (29, True),    # repeated percept, no new command
        (26, True),    # exact boundary, IDLE (mode transition from COOL)
        (20, True),    # other exact boundary, still IDLE
        (19, True),    # transition to WARM
        (29, False),   # empty room, ECO
        (24, False),   # still empty, no new command
        (29, True),    # people came back, COOL again
    ]

    for step, percept in enumerate(percepts, 1):
        before = agent.previous_mode
        target, send = agent.act(*percept)
        if send:
            outcome = "command sent"
        else:
            outcome = "no command"
        print(step, "| previous:", before, "| percept:", percept,
              "| target:", target, "|", outcome)

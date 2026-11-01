# lab2_percepts.py
# Lab 2 - simple reflex classroom agent and its percept trace.
# Run with:  python lab2_percepts.py
#
# Temperature is in degrees Celsius and occupied is True or False.
# ECO, COOL, WARM and IDLE are just labels, no hardware is controlled.


class ClassroomAgent:
    def act(self, temp, occupied):
        # an empty room comes first, whatever the temperature is
        if not occupied:
            return "ECO"
        if temp > 26:
            return "COOL"
        if temp < 20:
            return "WARM"
        return "IDLE"


agent = ClassroomAgent()

percepts = [(29, True), (29, True), (20, True),
            (26, True), (19, True), (29, False)]

for step, percept in enumerate(percepts, 1):
    print(step, percept, "target mode", agent.act(*percept))

# This agent has no memory, so step 2 gives COOL again even though
# step 1 already asked for cooling.

# lab1_compare.py
# Lab 1 - compares a rule based check with a probability threshold.
# Run with:  python lab1_compare.py
#
# The probability values below are invented demo numbers. Nothing is trained
# here, so this shows behaviour only. It says nothing about accuracy.


def symbolic(score, complete):
    # the conditions are written out, so we can see exactly why it decides
    if complete and score >= 70:
        return "Review"
    return "Hold"


def threshold(probability):
    # only looks at one number, it never checks the documents
    if probability >= 0.70:
        return "Review"
    return "Hold"


cases = [
    # name,            score, complete, probability
    ("complete_high",   82,   True,     0.81),
    ("complete_low",    68,   True,     0.74),
    ("incomplete_high", 91,   False,    0.88),
    ("boundary",        70,   True,     0.70),
]

print("case | symbolic | threshold | disagreement")
for name, score, complete, prob in cases:
    a = symbolic(score, complete)
    b = threshold(prob)
    print(name, a, b, a != b, sep=" | ")

# Extra check: change the boundary values one at a time to see which one matters
print()
print("boundary check")
print("score 69, complete:", symbolic(69, True))
print("probability 0.69  :", threshold(0.69))

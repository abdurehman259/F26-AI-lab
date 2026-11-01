# lab1_rules.py
# Lab 1, Task 2 - rule-based scholarship screening with two extra conditions.
# Run with:  python lab1_rules.py
#
# NOTE: every threshold below is a made-up lab assumption. It is not a real
# scholarship policy. "Review" only means "send to a human reviewer".

MIN_SCORE = 70   # from the original example
MIN_GPA = 2.5    # new condition 1 (assumed value)
# new condition 2: the applicant must have a recommendation letter on file


def screen(app):
    """Check one application and return (decision, reason)."""
    if not app["documents_complete"]:
        return "Hold", "documents are incomplete"
    if app["score"] < MIN_SCORE:
        return "Hold", "score " + str(app["score"]) + " is below " + str(MIN_SCORE)
    if app["gpa"] < MIN_GPA:
        return "Hold", "GPA " + str(app["gpa"]) + " is below " + str(MIN_GPA)
    if not app["has_letter"]:
        return "Hold", "no recommendation letter"
    return "Review", "all conditions satisfied"


# Four core test cases. The expected result is written by hand BEFORE running.
tests = [
    # name,            score, docs,  gpa, letter, expected
    ("pass_case",       82,  True,  3.4, True,  "Review"),
    ("low_gpa",         78,  True,  2.1, True,  "Hold"),
    ("missing_letter",  85,  True,  3.2, False, "Hold"),
    ("boundary",        70,  True,  2.5, True,  "Review"),  # exactly on both limits
]

passed = 0
for name, score, docs, gpa, letter, expected in tests:
    app = {
        "score": score,
        "documents_complete": docs,
        "gpa": gpa,
        "has_letter": letter,
    }
    actual, reason = screen(app)

    print("Case     :", name)
    print("Input    :", app)
    print("Expected :", expected)
    print("Actual   :", actual)
    print("Reason   :", reason)
    if actual == expected:
        print("Result   : OK")
        passed += 1
    else:
        print("Result   : MISMATCH")
    print("-" * 50)

print(passed, "of", len(tests), "cases matched the expected result")

# Ratings
STRONGLY_BAD = 1
SLIGHTLY_BAD = 2
NEUTRAL = 3
SLIGHTLY_GOOD = 4
STRONGLY_GOOD = 5

RATINGS = [STRONGLY_BAD, SLIGHTLY_BAD, NEUTRAL, SLIGHTLY_GOOD, STRONGLY_GOOD]

DID_NOT_MEET = {
    "BF": "Not a good fit",
    "NR": "Did not respond",
    "NI": "Not interested",
    "TB": "Too busy",
    "OT": "Other",
}
# Above dictionary with keys and values reversed
DID_NOT_MEET_REV = dict(zip(DID_NOT_MEET.values(), DID_NOT_MEET.keys()))

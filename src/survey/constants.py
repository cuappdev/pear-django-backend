# Ratings
STRONGLY_BAD = 1
SLIGHTLY_BAD = 2
NEUTRAL = 3
SLIGHTLY_GOOD = 4
STRONGLY_GOOD = 5

RATINGS = [STRONGLY_BAD, SLIGHTLY_BAD, NEUTRAL, SLIGHTLY_GOOD, STRONGLY_GOOD]

BAD_FIT = ("BF", "Not a good fit")
NO_RESPONSE = ("NR", "They didn't respond")
NOT_INTERESTED = ("NI", "Not interested")
TOO_BUSY = ("TB", "Too busy")
OTHER = ("OT", "Other")

DID_NOT_MEET = [BAD_FIT, NO_RESPONSE, NOT_INTERESTED, TOO_BUSY, OTHER]
DID_NOT_MEET_SHORT = list(map(lambda x: x[0], DID_NOT_MEET))
DID_NOT_MEET_LONG = list(map(lambda x: x[1], DID_NOT_MEET))


def short_to_long(short_name):
    """Convert a short name to a long name"""
    if short_name == BAD_FIT[0]:
        return BAD_FIT[1]
    elif short_name == NO_RESPONSE[0]:
        return NO_RESPONSE[1]
    elif short_name == NOT_INTERESTED[0]:
        return NOT_INTERESTED[1]
    elif short_name == TOO_BUSY[0]:
        return TOO_BUSY[1]
    elif short_name == OTHER[0]:
        return OTHER[1]
    else:
        return None


def long_to_short(long_name):
    """Convert a long name to a short name"""
    if long_name == BAD_FIT[1]:
        return BAD_FIT[0]
    elif long_name == NO_RESPONSE[1]:
        return NO_RESPONSE[0]
    elif long_name == NOT_INTERESTED[1]:
        return NOT_INTERESTED[0]
    elif long_name == TOO_BUSY[1]:
        return TOO_BUSY[0]
    elif long_name == OTHER[1]:
        return OTHER[0]
    else:
        return None

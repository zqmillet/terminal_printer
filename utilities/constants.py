class FLAG:
    BEGIN = '\x1b'
    ENG = 'm'

class STATUS:
    IDEL = 0
    BEGIN = 1
    END = 2

class CONTROL:
    UNDER_LINE = 4
    BOLD_ON = 1
    CANCEL = 0
    SET_FORE_COLOR = 38
    SET_BACK_COLOR = 48
    SET_DEFAULT_FORE_COLOR = 39
    SET_DEFAULT_BACK_COLOR = 49
    SYSTEM_FORE_COLOR = {
        30: (0,0,0),
        31: (255,0,0),
        32: (0,255,0),
        33: (255,255,0),
        34: (0,0,255),
        35: (255,0,255),
        36: (0,255,255),
        37: (255,255,255)
    }
    SYSTEM_BACK_COLOR = {
        40: (0,0,0),
        41: (255,0,0),
        42: (0,255,0),
        43: (255,255,0),
        44: (0,0,255),
        45: (255,0,255),
        46: (0,255,255),
        47: (255,255,255)
    }



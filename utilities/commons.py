import unicodedata

def get_char_width(char):
    status = unicodedata.east_asian_width(char)
    if status == 'W' or status == 'F':
        return 2
    else:
        return 1

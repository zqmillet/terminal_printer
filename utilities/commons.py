import unicodedata

def get_char_width(char):
    status = unicodedata(char)
    if status == 'W' or status == 'F':
        return 2
    else:
        return 1

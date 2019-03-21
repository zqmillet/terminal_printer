import subprocess
import fpdf
import re

from xterm_color_to_rgb import xterm_color_to_rgb

def get_panel_ascii_code(panel_name):
    command = ['tmux', 'capture-pane', '-t', panel_name, '-e', '-J', '-p']
    result = subprocess.Popen(command, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    return result.stdout.read().decode('utf8')

class FLAG:
    BEGIN = '\x1b'
    ENG = 'm'

class STATUS:
    IDEL = 0
    BEGIN = 1
    END = 2

class CONTROL:
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

class PDFFile(object):
    __file = None
    __default_fore_color = None
    __default_back_color = None
    __font_name = None
    __font_size = None

    def __init__(
        self,
        default_fore_color,
        default_back_color,
        font_name = 'Courier',
        font_size = 14 / 3
    ):
        self.__file = fpdf.FPDF()
        self.__file.add_page()
        self.__default_fore_color = default_fore_color
        self.__default_back_color = default_back_color
        self.set_font(font_name = font_name, font_size = font_size)

    def set_back_color(self, r, g, b):
        self.__file.set_fill_color(r, g, b)

    def set_fore_color(self, r, g, b):
        self.__file.set_text_color(r, g, b)

    def set_font(self, font_name, font_size):
        self.__file.set_font(font_name, '', font_size)
        self.__font_name = font_name
        self.__font_size = font_size

    def set_default_color(self):
        self.set_back_color(*self.__default_back_color)
        self.set_fore_color(*self.__default_fore_color)

    def add_char(self, char, end_line = False, fill = True, border = False, width = 1, height = 2, align = 'C'):
        border = 1  if border else 0
        end_line = 1 if end_line else 0
        self.__file.cell(width, height, char, border, end_line, fill = True, align = align)

    def write_line(self, ascii_code, maximum_line_length):
        status = STATUS.IDEL
        offset = 0
        control_sequence = ''

        for index, char in enumerate(ascii_code):
            if status == STATUS.IDEL:
                if char == FLAG.BEGIN:
                    status = STATUS.BEGIN
                    continue
                else:
                    if offset == maximum_line_length - 1:
                        self.add_char(char, end_line = True)
                        offset = 0
                    else:
                        self.add_char(char, end_line = False)
                        offset += 1
            elif status == STATUS.BEGIN:
                if char == FLAG.ENG:
                    status = STATUS.IDEL
                    self.execute(control_sequence)
                    control_sequence = ''
                else:
                    control_sequence += char
            else:
                import pdb; pdb.set_trace()

    def execute(self, control_sequence):
        control_sequence = [int(command) for command in control_sequence[1:].split(';')]

        index = 0
        while index < len(control_sequence):
            command = control_sequence[index]
            if command in CONTROL.SYSTEM_FORE_COLOR:
                self.set_fore_color(*CONTROL.SYSTEM_FORE_COLOR[command])
                index += 1
            elif command in CONTROL.SYSTEM_BACK_COLOR:
                self.set_back_color(*CONTROL.SYSTEM_BACK_COLOR[command])
                index += 1
            elif command == CONTROL.SET_FORE_COLOR:
                self.set_fore_color(*xterm_color_to_rgb(control_sequence[index + 2]))
                index += 3
            elif command == CONTROL.SET_BACK_COLOR:
                self.set_back_color(*xterm_color_to_rgb(control_sequence[index + 2]))
                index += 3
            elif command == CONTROL.SET_DEFAULT_FORE_COLOR:
                self.set_fore_color(*self.__default_fore_color)
                index += 1
            elif command == CONTROL.SET_DEFAULT_BACK_COLOR:
                self.set_back_color(*self.__default_back_color)
                index += 1
            else:
                index += 1

    def save(self, file_path):
        self.__file.output(file_path, 'F')

def get_maximum_length(ascii_code):
    regex = re.compile(r'\x1b\[[;\d]*[A-Za-z]')
    return max([len(regex.sub('', line)) for line in ascii_code])

def delete_blank_lines(ascii_code):
    for index in list(range(len(ascii_code)))[::-1]:
        if ascii_code[index].strip() == '':
            del ascii_code[index]
        else:
            break
    return ascii_code


def testcases():
    ascii_code = get_panel_ascii_code('zhangqi:0.0')
    with open('tmux.txt', 'w') as file:
        file.write(ascii_code)

    pdf_file = PDFFile(
        default_fore_color = (112, 130, 132),
        default_back_color = (10, 35, 44)
    )

    ascii_code = ascii_code.split('\n')
    maximum_line_length = get_maximum_length(ascii_code)
    ascii_code = delete_blank_lines(ascii_code)

    for line in ascii_code:
        pdf_file.write_line(line, maximum_line_length)

    pdf_file.save('./main.pdf')

if __name__ == '__main__':
    testcases()

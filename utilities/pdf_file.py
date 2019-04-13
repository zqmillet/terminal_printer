import os
import fpdf

from utilities import ColorMap
from utilities import get_maximum_length, delete_blank_lines
from utilities import FLAG, CONTROL, STATUS
from utilities import get_char_width

class PDFFile(object):
    __file = None
    __default_fore_color = None
    __default_back_color = None
    __bold_fore_color = None
    __bold_back_color = None
    __font_name = None
    __font_size = None
    __char_width = None
    __char_height = None
    __color_map = None
    __fore_color = None
    __back_color = None

    def __init__(
        self,
        ascii_code,
        default_fore_color,
        default_back_color,
        font_path,
        bold_fore_color = None,
        bold_back_color = None,
        font_size = 5,
        char_rate = 1
    ):
        ascii_code = ascii_code.split('\n')
        maximum_line_length = get_maximum_length(ascii_code)
        ascii_code = delete_blank_lines(ascii_code)
        line_number = len(ascii_code)

        font_name = os.path.basename(font_path)
        font_name = os.path.splitext(font_name)[0]

        self.__bold_fore_color = bold_fore_color if not bold_fore_color is None else default_back_color
        self.__bold_back_color = bold_back_color if not bold_back_color is None else default_fore_color

        self.__color_map = ColorMap()
        self.__color_map.set_black(default_back_color)

        self.__char_width = font_size / char_rate / 5
        self.__char_height = self.__char_width * 2

        self.__file = fpdf.FPDF(format = (maximum_line_length * self.__char_width, line_number * self.__char_height))
        self.__file.add_page()
        self.__file.set_xy(0, 0)
        self.__file.set_margins(0, 0, 0)
        self.__file.set_auto_page_break(False)
        self.__file.add_font(font_name, fname = font_path, uni = True)

        self.__default_fore_color = default_fore_color
        self.__default_back_color = default_back_color
        self.__fore_color = default_fore_color
        self.__back_color = default_back_color

        self.set_font(font_name = font_name, font_size = font_size)
        self.set_default_color()

        for line in ascii_code:
            self.write_line(line, maximum_line_length)

    def set_back_color(self, r, g, b):
        self.__file.set_fill_color(r, g, b)
        self.__back_color = (r, g, b)

    def set_fore_color(self, r, g, b):
        self.__file.set_text_color(r, g, b)
        self.__fore_color = (r, g, b)

    def set_font(self, font_name, font_size, style = ''):
        self.__file.set_font(font_name, style, font_size)
        self.__font_name = font_name
        self.__font_size = font_size

    def set_default_color(self):
        self.set_back_color(*self.__default_back_color)
        self.set_fore_color(*self.__default_fore_color)

    def add_char(self, char, end_line = False, fill = True, border = False, align = 'C'):
        border = 1  if border else 0
        end_line = 1 if end_line else 0
        self.__file.cell(self.__char_width * get_char_width(char), self.__char_height, char, border, end_line, fill = True, align = align)

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
                    # print(offset, maximum_line_length - 1)
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
                pass

        if offset == 0 and len(ascii_code) > 0:
            return

        fore_color = self.__fore_color
        back_color = self.__back_color
        self.set_default_color()
        for _ in range(maximum_line_length - offset - 1):
            self.add_char(' ', end_line = False)
        self.add_char(' ', end_line = True)
        self.set_fore_color(*fore_color)
        self.set_back_color(*back_color)

    @staticmethod
    def is_full_width_char(char):
        pass

    def execute(self, control_sequence):
        control_sequence = [int(command) for command in control_sequence[1:].split(';') if not len(command) == 0]

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
                self.set_fore_color(*self.__color_map[control_sequence[index + 2]])
                index += 3
            elif command == CONTROL.SET_BACK_COLOR:
                self.set_back_color(*self.__color_map[control_sequence[index + 2]])
                index += 3
            elif command == CONTROL.BOLD_ON:
                self.bold_on()
                index += 1
            elif command == CONTROL.SET_DEFAULT_FORE_COLOR:
                self.set_fore_color(*self.__default_fore_color)
                index += 1
            elif command == CONTROL.SET_DEFAULT_BACK_COLOR:
                self.set_back_color(*self.__default_back_color)
                index += 1
            elif command == CONTROL.CANCEL:
                self.set_font(self.__font_name, self.__font_size, '')
                self.set_default_color()
                index += 1
            elif command == CONTROL.UNDER_LINE:
                self.set_font(self.__font_name, self.__font_size, 'U')
                index += 1
            else:
                index += 1

    def bold_on(self):
        self.set_fore_color(*self.__bold_fore_color)
        self.set_back_color(*self.__bold_back_color)

    def save(self, file_path):
        self.__file.set_margins(0, 0, 0)
        self.__file.output(file_path, 'F')

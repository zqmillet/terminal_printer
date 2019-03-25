import subprocess
import fpdf
import re
import os
import sys

from utilities import ArgumentParser
from utilities import FLAG, CONTROL, STATUS

def get_panel_ascii_code(panel_name):
    command = ['tmux', 'capture-pane', '-t', panel_name, '-e', '-J', '-p']
    result = subprocess.Popen(command, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    return result.stdout.read().decode('utf8')

class ColorMap(dict):
    def __init__(self):
        map = {
            0:   (0, 0, 0),
            1:   (128, 0, 0),
            2:   (0, 128, 0),
            3:   (128, 128, 0),
            4:   (0, 0, 128),
            5:   (128, 0, 128),
            6:   (0, 128, 128),
            7:   (192, 192, 192),
            8:   (128, 128, 128),
            9:   (255, 0, 0),
            10:  (0, 255, 0),
            11:  (255, 255, 0),
            12:  (0, 0, 255),
            13:  (255, 0, 255),
            14:  (0, 255, 255),
            15:  (255, 255, 255),
            16:  (0, 0, 0),
            17:  (0, 0, 95),
            18:  (0, 0, 135),
            19:  (0, 0, 175),
            20:  (0, 0, 215),
            21:  (0, 0, 255),
            22:  (0, 95, 0),
            23:  (0, 95, 95),
            24:  (0, 95, 135),
            25:  (0, 95, 175),
            26:  (0, 95, 215),
            27:  (0, 95, 255),
            28:  (0, 135, 0),
            29:  (0, 135, 95),
            30:  (0, 135, 135),
            31:  (0, 135, 175),
            32:  (0, 135, 215),
            33:  (0, 135, 255),
            34:  (0, 175, 0),
            35:  (0, 175, 95),
            36:  (0, 175, 135),
            37:  (0, 175, 175),
            38:  (0, 175, 215),
            39:  (0, 175, 255),
            40:  (0, 215, 0),
            41:  (0, 215, 95),
            42:  (0, 215, 135),
            43:  (0, 215, 175),
            44:  (0, 215, 215),
            45:  (0, 215, 255),
            46:  (0, 255, 0),
            47:  (0, 255, 95),
            48:  (0, 255, 135),
            49:  (0, 255, 175),
            50:  (0, 255, 215),
            51:  (0, 255, 255),
            52:  (95, 0, 0),
            53:  (95, 0, 95),
            54:  (95, 0, 135),
            55:  (95, 0, 175),
            56:  (95, 0, 215),
            57:  (95, 0, 255),
            58:  (95, 95, 0),
            59:  (95, 95, 95),
            60:  (95, 95, 135),
            61:  (95, 95, 175),
            62:  (95, 95, 215),
            63:  (95, 95, 255),
            64:  (95, 135, 0),
            65:  (95, 135, 95),
            66:  (95, 135, 135),
            67:  (95, 135, 175),
            68:  (95, 135, 215),
            69:  (95, 135, 255),
            70:  (95, 175, 0),
            71:  (95, 175, 95),
            72:  (95, 175, 135),
            73:  (95, 175, 175),
            74:  (95, 175, 215),
            75:  (95, 175, 255),
            76:  (95, 215, 0),
            77:  (95, 215, 95),
            78:  (95, 215, 135),
            79:  (95, 215, 175),
            80:  (95, 215, 215),
            81:  (95, 215, 255),
            82:  (95, 255, 0),
            83:  (95, 255, 95),
            84:  (95, 255, 135),
            85:  (95, 255, 175),
            86:  (95, 255, 215),
            87:  (95, 255, 255),
            88:  (135, 0, 0),
            89:  (135, 0, 95),
            90:  (135, 0, 135),
            91:  (135, 0, 175),
            92:  (135, 0, 215),
            93:  (135, 0, 255),
            94:  (135, 95, 0),
            95:  (135, 95, 95),
            96:  (135, 95, 135),
            97:  (135, 95, 175),
            98:  (135, 95, 215),
            99:  (135, 95, 255),
            100: (135, 135, 0),
            101: (135, 135, 95),
            102: (135, 135, 135),
            103: (135, 135, 175),
            104: (135, 135, 215),
            105: (135, 135, 255),
            106: (135, 175, 0),
            107: (135, 175, 95),
            108: (135, 175, 135),
            109: (135, 175, 175),
            110: (135, 175, 215),
            111: (135, 175, 255),
            112: (135, 215, 0),
            113: (135, 215, 95),
            114: (135, 215, 135),
            115: (135, 215, 175),
            116: (135, 215, 215),
            117: (135, 215, 255),
            118: (135, 255, 0),
            119: (135, 255, 95),
            120: (135, 255, 135),
            121: (135, 255, 175),
            122: (135, 255, 215),
            123: (135, 255, 255),
            124: (175, 0, 0),
            125: (175, 0, 95),
            126: (175, 0, 135),
            127: (175, 0, 175),
            128: (175, 0, 215),
            129: (175, 0, 255),
            130: (175, 95, 0),
            131: (175, 95, 95),
            132: (175, 95, 135),
            133: (175, 95, 175),
            134: (175, 95, 215),
            135: (175, 95, 255),
            136: (175, 135, 0),
            137: (175, 135, 95),
            138: (175, 135, 135),
            139: (175, 135, 175),
            140: (175, 135, 215),
            141: (175, 135, 255),
            142: (175, 175, 0),
            143: (175, 175, 95),
            144: (175, 175, 135),
            145: (175, 175, 175),
            146: (175, 175, 215),
            147: (175, 175, 255),
            148: (175, 215, 0),
            149: (175, 215, 95),
            150: (175, 215, 135),
            151: (175, 215, 175),
            152: (175, 215, 215),
            153: (175, 215, 255),
            154: (175, 255, 0),
            155: (175, 255, 95),
            156: (175, 255, 135),
            157: (175, 255, 175),
            158: (175, 255, 215),
            159: (175, 255, 255),
            160: (215, 0, 0),
            161: (215, 0, 95),
            162: (215, 0, 135),
            163: (215, 0, 175),
            164: (215, 0, 215),
            165: (215, 0, 255),
            166: (215, 95, 0),
            167: (215, 95, 95),
            168: (215, 95, 135),
            169: (215, 95, 175),
            170: (215, 95, 215),
            171: (215, 95, 255),
            172: (215, 135, 0),
            173: (215, 135, 95),
            174: (215, 135, 135),
            175: (215, 135, 175),
            176: (215, 135, 215),
            177: (215, 135, 255),
            178: (215, 175, 0),
            179: (215, 175, 95),
            180: (215, 175, 135),
            181: (215, 175, 175),
            182: (215, 175, 215),
            183: (215, 175, 255),
            184: (215, 215, 0),
            185: (215, 215, 95),
            186: (215, 215, 135),
            187: (215, 215, 175),
            188: (215, 215, 215),
            189: (215, 215, 255),
            190: (215, 255, 0),
            191: (215, 255, 95),
            192: (215, 255, 135),
            193: (215, 255, 175),
            194: (215, 255, 215),
            195: (215, 255, 255),
            196: (255, 0, 0),
            197: (255, 0, 95),
            198: (255, 0, 135),
            199: (255, 0, 175),
            200: (255, 0, 215),
            201: (255, 0, 255),
            202: (255, 95, 0),
            203: (255, 95, 95),
            204: (255, 95, 135),
            205: (255, 95, 175),
            206: (255, 95, 215),
            207: (255, 95, 255),
            208: (255, 135, 0),
            209: (255, 135, 95),
            210: (255, 135, 135),
            211: (255, 135, 175),
            212: (255, 135, 215),
            213: (255, 135, 255),
            214: (255, 175, 0),
            215: (255, 175, 95),
            216: (255, 175, 135),
            217: (255, 175, 175),
            218: (255, 175, 215),
            219: (255, 175, 255),
            220: (255, 215, 0),
            221: (255, 215, 95),
            222: (255, 215, 135),
            223: (255, 215, 175),
            224: (255, 215, 215),
            225: (255, 215, 255),
            226: (255, 255, 0),
            227: (255, 255, 95),
            228: (255, 255, 135),
            229: (255, 255, 175),
            230: (255, 255, 215),
            231: (255, 255, 255),
            232: (8, 8, 8),
            233: (18, 18, 18),
            234: (28, 28, 28),
            235: (38, 38, 38),
            236: (48, 48, 48),
            237: (58, 58, 58),
            238: (68, 68, 68),
            239: (78, 78, 78),
            240: (88, 88, 88),
            241: (98, 98, 98),
            242: (108, 108, 108),
            243: (118, 118, 118),
            244: (128, 128, 128),
            245: (138, 138, 138),
            246: (148, 148, 148),
            247: (158, 158, 158),
            248: (168, 168, 168),
            249: (178, 178, 178),
            250: (188, 188, 188),
            251: (198, 198, 198),
            252: (208, 208, 208),
            253: (218, 218, 218),
            254: (228, 228, 228),
            255: (238, 238, 238)
        }

        for key, value in map.items():
            self[key] = value

    def set_black(self, color):
        # self[0] = color
        # self[16] = color
        pass

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
        bold_fore_color = None,
        bold_back_color = None,
        font_path = './fonts/consolas.ttf',
        font_size = 5.3,
        char_width = 1,
        char_height = 2
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

        self.__char_width = char_width
        self.__char_height = char_height

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
        self.__file.cell(self.__char_width, self.__char_height, char, border, end_line, fill = True, align = align)

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

def parse_arguments():
    argument_parser = ArgumentParser()
    argument_parser.add_argument(
        '-p', '--pane',
        type = str,
        action = 'store',
        required = True,
        help = 'specify the pane name of tmux'
    )
    argument_parser.add_argument(
        '-s', '--font_size',
        type = int,
        action = 'store',
        default = 5,
        help = 'specify the font size'
    )
    argument_parser.add_argument(
        '-f', '--default_fore_color',
        type = int,
        nargs = 3,
        action = 'store',
        default = [255, 255, 255],
        help = 'specify the default fore color'
    )
    argument_parser.add_argument(
        '-b', '--default_back_color',
        type = int,
        nargs = 3,
        action = 'store',
        default = [0, 0, 0],
        help = 'specify the default back color'
    )
    argument_parser.add_argument(
        '-n', '--font_name',
        type = int,
        action = 'store',
        default = './fonts/consolas.ttf',
        help = 'specify the font name'
    )
    argument_parser.add_argument(
        '-t', '--temporary_file',
        type = str,
        action = 'store',
        default = '{output_file_name}.tmux',
        help = 'specify the temporary file path'
    )
    argument_parser.add_argument(
        '-o', '--output',
        type = str,
        action = 'store',
        required = True,
        help = 'specify the output file path'
    )

    return argument_parser.parse_args(sys.argv[1:])

def testcases():
    arguments = parse_arguments()
    ascii_code = get_panel_ascii_code('zhangqi:0.0')
    with open('tmux.txt', 'w') as file:
        file.write(ascii_code)

    pdf_file = PDFFile(
        # default_fore_color = (112, 130, 132),
        # default_back_color = (10, 35, 44),
        default_fore_color = (255, 255, 255),
        default_back_color = (0, 0, 0),
        font_path = './fonts/consolas.ttf',
        ascii_code = ascii_code
    )

    pdf_file.save('./main.pdf')

if __name__ == '__main__':
    testcases()

import subprocess
import fpdf
import re
import os
import sys

from utilities import ArgumentParser
from utilities import PDFFile
from utilities import FLAG, CONTROL, STATUS

def get_pane_ascii_code(pane_name):
    command = ['tmux', 'capture-pane', '-t', pane_name, '-e', '-J', '-p']
    result = subprocess.Popen(command, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    return result.stdout.read().decode('utf8')

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

    ascii_code = get_panel_ascii_code(arguments.pane)
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

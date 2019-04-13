import subprocess
import fpdf
import re
import os
import sys

from utilities import ArgumentParser
from utilities import PDFFile
from utilities import FLAG, CONTROL, STATUS, FILE_MODE, ENCODE
from utilities import get_pane_ascii_code, get_maximum_length, delete_blank_lines, get_pane_list

def parse_arguments():
    argument_parser = ArgumentParser()
    argument_parser.add_argument(
        '-p', '--pane',
        type = str,
        action = 'store',
        default = None,
        help = 'specify the pane name of tmux'
    )
    argument_parser.add_argument(
        '-s', '--font_size',
        type = float,
        action = 'store',
        default = 8,
        help = 'specify the font size'
    )
    argument_parser.add_argument(
        '-c', '--char_rate',
        type = float,
        action = 'store',
        default = 1,
        help = 'specify the char rate'
    )
    argument_parser.add_argument(
        '-df', '--default_fore_color',
        type = int,
        nargs = 3,
        action = 'store',
        default = [255, 255, 255],
        help = 'specify the default fore color'
    )
    argument_parser.add_argument(
        '-db', '--default_back_color',
        type = int,
        nargs = 3,
        action = 'store',
        default = [0, 0, 0],
        help = 'specify the default back color'
    )
    argument_parser.add_argument(
        '-bf', '--bold_fore_color',
        type = int,
        nargs = 3,
        action = 'store',
        default = [0, 255, 255],
        help = 'specify the default fore color'
    )
    argument_parser.add_argument(
        '-bb', '--bold_back_color',
        type = int,
        nargs = 3,
        action = 'store',
        default = [0, 0, 0],
        help = 'specify the default back color'
    )
    argument_parser.add_argument(
        '-n', '--font',
        type = str,
        action = 'store',
        default = './fonts/consolas.ttf',
        help = 'specify the font'
    )
    argument_parser.add_argument(
        '-o', '--output',
        type = str,
        action = 'store',
        required = True,
        help = 'specify the output file path'
    )

    return argument_parser.parse_args(sys.argv[1:])

def get_temporary_file_path(output_file_path, extension = 'tmux'):
    output_file_name = os.path.split(output_file_path)[-1]
    temporary_file_name = os.path.splitext(output_file_name)[0] + '.' + extension
    output_directory = os.path.dirname(output_file_path)
    return os.path.join(output_directory, temporary_file_name)

def get_pane_name():
    print('panes:')
    pane_name_list = get_pane_list()
    for index, pane_name in enumerate(pane_name_list, start = 1):
        print('<{index}> {pane_name}'.format(pane_name = pane_name, index = index))

    choices = [str(item) for item in range(1, index + 1)]
    choice = get_choice(choices, hint = 'which pane do you want to print?')
    return pane_name_list[int(choice) - 1]

def get_choice(choices, hint):
    while True:
        print(hint + ' <{choices}>:'.format(choices = ', '.join(choices)), end = ' ')
        choice = input()

        if not choice in choices:
            continue

        return choice

def main():
    arguments = parse_arguments()

    pane_name = arguments.pane if not arguments.pane is None else get_pane_name()
    print('printing the pane {pane_name}'.format(pane_name = pane_name))

    output_file_path = arguments.output
    temporary_file_path = get_temporary_file_path(output_file_path)

    ascii_code = get_pane_ascii_code(pane_name)
    with open(temporary_file_path, FILE_MODE.WRITE, encoding = ENCODE.UTF8) as file:
        file.write(ascii_code)

    pdf_file = PDFFile(
        ascii_code = ascii_code,
        default_fore_color = tuple(arguments.default_fore_color),
        default_back_color = tuple(arguments.default_back_color),
        bold_fore_color = tuple(arguments.bold_fore_color),
        bold_back_color = tuple(arguments.bold_back_color),
        font_path = arguments.font,
        font_size = arguments.font_size,
        char_rate = arguments.char_rate
    )

    if os.path.exists(output_file_path):
        choice = get_choice(choices = ['y', 'n'], hint = 'the file {output_file_path} exist, do you want to replace it?'.format(output_file_path = output_file_path))

        if choice == 'n':
            return

    pdf_file.save(output_file_path)

if __name__ == '__main__':
    main()

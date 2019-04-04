import subprocess
import fpdf
import re
import os
import sys

from utilities import ArgumentParser
from utilities import PDFFile
from utilities import FLAG, CONTROL, STATUS, FILE_MODE, ENCODE

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
        type = float,
        action = 'store',
        default = 5.3,
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
        '-n', '--font,
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

def testcases():
    arguments = parse_arguments()

    output_file_path = arguments.output
    temporary_file_path = get_temporary_file_path(output_file_path)
    import pdb; pdb.set_trace()

    ascii_code = get_panel_ascii_code(arguments.pane)
    with open(arguments.temporary_file, FILE_MODE.READ, encoding = ENCODE.UTF8) as file:
        file.write(ascii_code)

    pdf_file = PDFFile(
        default_fore_color = tuple(arguments.default_fore_color),
        default_back_color = tuple(arguments.default_back_color),
        font_path = arguments.font,
        font_size = arguments.font_size,
        ascii_code = ascii_code
    )

    pdf_file.save('./main.pdf')

if __name__ == '__main__':
    testcases()

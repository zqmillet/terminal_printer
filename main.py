import subprocess
import fpdf

from xterm_color_to_rgb import xterm_color_to_rgb

def get_panel_ascii_code(panel_name):
    command = ['tmux', 'capture-pane', '-t', panel_name, '-e', '-J', '-p']
    result = subprocess.Popen(command, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    return result.stdout.read().decode('utf8')

class STATUS:
    IDEL = 0
    BEGIN = 1
    END = 2

def convert_ascii_code_to_latex(ascii_code, file_path):
    print(ascii_code)
    file = fpdf.FPDF()
    file.add_page()
    file.set_font('Courier', '', 14/3)

    BEGIN = '\x1b'
    END = 'm'

    latex_code = ''
    control = ''
    status = STATUS.IDEL
    for index, char in enumerate(ascii_code):
        if status == STATUS.IDEL:
            if char == BEGIN:
                status = STATUS.BEGIN
                control = ''
                continue
            else:
                if ascii_code[index] == '\n':
                    file.cell(1, 2, char, 0, 1, fill = True, align = 'C')
                else:
                    file.cell(1, 2, char, 0, 0, fill = True, align = 'C')
        elif status == STATUS.BEGIN:
            if char == END:
                status = STATUS.IDEL
                colors = parse_control(control)

                for color in colors:
                    if color[0] == 'fore':
                        file.set_text_color(*color[1])
                    elif color[0] == 'back':
                        file.set_fill_color(*color[1])
                continue
            else:
                control += char
        else:
            import pdb; pdb.set_trace()
    file.output('py3k.pdf', 'F')

def parse_control(control):
    FORE_COLOR = '38'
    BACK_COLOR = '48'

    if not control.startswith('['):
        return list()

    control = control[1:].split(';')

    if len(control) == 1:
        if control[0].startswith('3'):
            return [('back', xterm_color_to_rgb(control[0]))]
        else:
            return list()

    colors = list()
    index = 0
    while True:
        item = control[index]
        if item == FORE_COLOR:
            colors.append(('fore', xterm_color_to_rgb(control[index + 2])))
            index += 2
        elif item == BACK_COLOR:
            colors.append(('back', xterm_color_to_rgb(control[index + 2])))
            index += 2

        index += 1
        if index > len(control) - 1:
            break

    return colors

def testcases():
    ascii_code = get_panel_ascii_code('zhangqi:0.1')
    with open('tmux.txt', 'w') as file:
        file.write(ascii_code)
    latex_code = convert_ascii_code_to_latex(ascii_code, 333)

if __name__ == '__main__':
    testcases()

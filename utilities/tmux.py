import re
import subprocess

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

def get_pane_list():
    import pdb; pdb.set_trace()

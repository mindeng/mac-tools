#! /usr/bin/env python3

import os
import stat
from pathlib import Path

BASEDIR = os.path.dirname(os.path.realpath(__file__))
HOME_DIR = os.getenv('HOME')

home_dir_list = [
        'scripts',
        'envs',
        ]

CONFIGS_DIR = os.path.join(BASEDIR, 'configs')
TOOLS_DIR = os.path.join(BASEDIR, 'tools')

def confirm_overwrite(filename):
    prompt = 'Overwrite %s ? (y/N) ' % filename
    input_str = input(prompt)
    return input_str == 'y'

def check_file_exists(path):
    if os.path.isfile(path):
        return True
    else:
        print(('File not exists: %s' % path))
        exit(1)

def add_exec_perm(path):
    if not os.access(path, os.X_OK):
        st = os.stat(path)
        os.chmod(path, st.st_mode | stat.S_IEXEC)

def ln_file(src, dst):
    if os.path.lexists(dst):
        if not confirm_overwrite(dst):
            return
        else:
            os.unlink(dst)

    os.symlink(src, dst)
    print(("ln -s %s %s" % (src, dst)))

def setup_config(name, dst_dir = Path.home()):
    name_src = name
    if name.startswith('.'):
        name_src = name.replace('.', '_', 1)
    src = os.path.join(CONFIGS_DIR, name_src)
    dst = os.path.join(dst_dir, name)
    ln_file(src, dst)

def setup_configs():
    home = Path.home()
    zsh_config_dir = home.joinpath(".oh-my-zsh/custom")
    if zsh_config_dir.exists():
        setup_config('my.zsh', zsh_config_dir)
    else:
        print('Please install oh-my-zsh first!')

    setup_config('.vimrc')
    setup_config('.screenrc')

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def setup_tool(name):
    src = os.path.join(TOOLS_DIR, name)
    dst = Path.home().joinpath('scripts', name)
    check_file_exists(src)
    add_exec_perm(src)
    ln_file(src, dst)

def setup_tools():
    setup_tool('sw-env')
    setup_tool('showHideFiles')
    setup_tool('aes-tool.py')

def setup_dirs():
    for d in home_dir_list:
        ensure_dir(Path.home().joinpath(d))

def main():
    setup_dirs()
    setup_configs()

if __name__ == '__main__':
    main()

#! /usr/bin/env python

import os
import stat

BASEDIR = os.path.dirname(os.path.realpath(__file__))
HOME_DIR = os.getenv('HOME')
BIN_DIR = os.path.join(HOME_DIR, 'bin')

CONFIGS_DIR = os.path.join(BASEDIR, 'configs')
TOOLS_DIR = os.path.join(BASEDIR, 'tools')

def confirm_overwrite(filename):
    prompt = 'Overwrite %s ? (yes/no) ' % filename
    input_str = raw_input(prompt)
    return input_str == 'yes'

def check_file_exists(path):
    if os.path.isfile(path):
        return True
    else:
        print 'File not exists: %s' % path
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
    print "ln -s %s %s" % (src, dst)

def setup_config(name):
    if name.startswith('.'):
        name_src = name.replace('.', '_', 1)
    src = os.path.join(CONFIGS_DIR, name_src)
    dst = os.path.join(HOME_DIR, name)
    ln_file(src, dst)

def setup_configs():
    setup_config('.bashrc')
    setup_config('.vimrc')
    setup_config('.screenrc')

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def setup_tool(name):
    src = os.path.join(TOOLS_DIR, name)
    dst = os.path.join(BIN_DIR, name)
    check_file_exists(src)
    add_exec_perm(src)
    ensure_dir(BIN_DIR)
    ln_file(src, dst)

def setup_tools():
    #setup_tool('sw-env')
    setup_tool('showHideFiles')
    setup_tool('aes-tool.py')

def main():
    setup_configs()
    setup_tools()

if __name__ == '__main__':
    main()

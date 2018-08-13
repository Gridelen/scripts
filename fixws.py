#!/usr/bin/python3

import argparse
import os


# TODO: more customization, generalize with format.py
def parse_args():
    parser = argparse.ArgumentParser(description='''
Fixes whitespaces: transforms tab to space and use LF(\n) as EOL''')
    parser.add_argument('path', action='store',
                        help='directory where sources are located')
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
                        help='print more info')
    return parser.parse_args()


def remove_ignored(dirs, ignored_set):
    remove_set = set()
    for i, e in enumerate(dirs):
        if e in ignored_set:
            remove_set.add(i)
    for i in remove_set:
        dirs.pop(i)


def format(file_name_abs):
    lines = []
    # do not translate newline
    with open(file_name_abs, mode='r', newline='') as f:
        for line in f:
            lines.append(line.replace('\t', '  ').replace('\r\n', '\n'))
    with open(file_name_abs, mode='w', newline='') as f:
        f.writelines(lines)


def format_files(path, filenames, allowed_ext, verbose=False):
    for filename in filenames:
        prefix, ext = os.path.splitext(filename)
        if ext and ext in allowed_ext:
            abs_file_name = os.path.abspath(os.path.join(path, filename))
            if verbose:
                print('Format', abs_file_name)
            format(abs_file_name)


def main():
    allowed_ext = {'.c', '.cpp', '.hpp', '.h'}
    ignored_dirs = {'mac'}
    args = parse_args()
    if (args.verbose):
        print('args:', args)
    for dirpath, dirnames, filenames in os.walk(args.path, topdown=True):
        remove_ignored(dirnames, ignored_dirs)
        format_files(dirpath, filenames, allowed_ext, args.verbose)


if __name__ == '__main__':
    main()

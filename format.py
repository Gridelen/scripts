#!/usr/bin/python3

import argparse
import os
import subprocess

#TODO: add option for ignored dirs
#TODO: add option for allowed extensions
#TODO: add option to read config from file

def parse_args():
  parser = argparse.ArgumentParser(description='Format sources')
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
  subprocess.call(['clang-format', '-style={BasedOnStyle: google}', '-i', file_name_abs])

def format_files(path, filenames, allowed_ext, verbose=False):
  for filename in filenames:
    prefix, ext = os.path.splitext(filename)
    if ext in allowed_ext:
      abs_file_name = os.path.abspath(os.path.join(path, filename))
      if verbose:
        print('Format', abs_file_name)
      format(abs_file_name)

def main():
  allowed_ext = {'.c', '.cpp', '.hpp', '.h'}
  ignored_dirs = {'snappystream'}
  args = parse_args()
  for dirpath, dirnames, filenames in os.walk(args.path, topdown=True):
    remove_ignored(dirnames, ignored_dirs)
    format_files(dirpath, filenames, allowed_ext, args.verbose)

if __name__ == '__main__':
  main()
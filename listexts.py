#!/usr/bin/python3

import argparse
import os

# TODO: optimize, too slow on large dirs/hierarchies
# TODO: more customization, generalize with format.py
def parse_args():
  parser = argparse.ArgumentParser(description='''
Finds and prints a set of file extensions in specified directory''')
  parser.add_argument('path', action='store',
    help='directory where files are located')
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

def collect_exts(path, filenames, exts_set, verbose=False):
  for filename in filenames:
    prefix, ext = os.path.splitext(filename)
    if ext:
      exts_set.add(ext)
    elif verbose:
      print('No extension:', os.path.abspath(os.path.join(path, filename)))

def main():
  ignored_dirs = {'.git'}
  args = parse_args()
  if (args.verbose):
    print('args:', args)
  exts_set = set()
  for dirpath, dirnames, filenames in os.walk(args.path, topdown=True):
    remove_ignored(dirnames, ignored_dirs)
    if args.verbose:
      print('Process path:', dirpath)
    collect_exts(dirpath, filenames, exts_set, args.verbose)
  print('\n'.join(exts_set))

if __name__ == '__main__':
  main()
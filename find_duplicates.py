r"""
Finds duplicate files. Duplicates are a set of 2 or more files for which the hash value is the same.
"""

import os
import sys
import hashlib
import argparse
from pathlib import Path

# read in chunks not to overuse memory
BUF_SIZE = 65536


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('input_dir',
                        help='directory to scan')
    parser.add_argument('--min-size', type=int,
                        help='ignore files less than min size (bytes), default: %(default)s (2 MiB)', default=2 * 1024 * 1024)
    parser.add_argument('--exclude',
                        help="directories that shouldn't be analyzed, comma-separated")
    parser.add_argument('--name-only', help='search for the same names instead of contents hash', action='store_true')
    return parser.parse_args()


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def get_duplicates(file_info, input_dir, min_file_size):
    duplicates = []
    for k in file_info.keys():
        pairs = file_info[k]
        file_size = -1
        paths = []
        for p in pairs:
            if file_size >= 0:
                if type(k) is not str and p[1] != file_size:
                    print("Warning: Same hash but different size -",
                          pairs[0][0], p[0])
            else:
                file_size = p[1]
            paths.append(os.path.relpath(p[0], input_dir))
        if len(paths) > 1 and file_size >= min_file_size:
            duplicates.append((file_size, paths))
    return duplicates


def compute_hash(file_path):
    file_size = 0
    hasher = hashlib.sha1()
    try:
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    file_size = f.tell()
                    break
                hasher.update(data)
    except Exception as e:
        print(sys.stderr, 'Error:', e)
        return None, 0
    return hasher.hexdigest(), file_size


def main():
    args = parse_args()
    input_dir = args.input_dir
    file_info = {}
    total_files = 0
    only_duplicates = False
    exclude_dirs = []
    if args.exclude:
        exclude_dirs = args.exclude.split(',')
    for root, dirs, files in os.walk(args.input_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for name in files:
            file_path = os.path.join(root, name)
            file_size = 0
            print(f"\x1b[KAnalyzing file: {name}", end='\r', flush=True)
            if args.name_only:
                key = name
                file_size = Path(file_path).stat().st_size
            else:
                key, file_size = compute_hash(file_path)
            if key is None:
                continue
            if key not in file_info:
                file_info[key] = []
            file_info[key].append((file_path, file_size))
            total_files += 1

    print('\nProcessed', total_files, 'files.')
    duplicates = get_duplicates(file_info, input_dir, args.min_size)
    print('Duplicates:', len(duplicates))
    for file_size, paths in sorted(duplicates, key=lambda x: x[0], reverse=True):
        if not only_duplicates:
            print('', sizeof_fmt(file_size))
        start_pos = 1 if only_duplicates else 0
        [print('  ', path) for path in paths[start_pos:]]


if __name__ == '__main__':
    main()

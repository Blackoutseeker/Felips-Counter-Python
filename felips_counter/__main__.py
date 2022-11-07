#!/usr/bin/env python3

from sys import exit as system_exit
from argparse import ArgumentParser
from colorama import init as init_colorama, Fore, Style
from felips_counter import __version__ as version
from felips_counter.src.reader import Reader
from felips_counter.src.writer import Writer


def main():
    init_colorama()

    parser = ArgumentParser()
    parser.add_argument('-p', '--path', type=str, default='.\\', dest='path', help='the path')
    parser.add_argument('-i', '--init', dest='init', action='store_true', help='create a .counterignore file')
    parser.add_argument('-b', '--blank', dest='blank_lines', action='store_false', help='count blank lines')
    parser.add_argument('-e', '--encoding', type=str, default='UTF-8', dest='encoding', help='file(s) encoding')
    parser.add_argument('--version', dest='version', action='store_true', help='check version')
    args = parser.parse_args()

    if args.version:
        print(f'felips-counter {version}')
        system_exit()

    path = args.path
    if path == '.':
        path = '.\\'

    if args.init:
        writer: Writer = Writer()
        writer.create_ignore_file(path)
        print('.counterignore file created and initialized.')
        system_exit()

    blank_lines = args.blank_lines
    encoding = args.encoding
    reader: Reader = Reader(ignore_blank_lines=blank_lines, encoding=encoding)
    total_lines = reader.count_lines(path)

    print(Fore.LIGHTGREEN_EX, f'Total lines: {total_lines}')
    print(Style.RESET_ALL)


if __name__ == '__main__':
    main()

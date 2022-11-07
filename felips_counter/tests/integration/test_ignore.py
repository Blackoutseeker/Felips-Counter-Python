from unittest import TestCase, main
from os import path as os_path, makedirs
from shutil import rmtree
from sys import exit as system_exit
from felips_counter.src.reader import Reader
from felips_counter.src.writer import Writer
from felips_counter import default_ignore_patterns


class TestIgnoreFeature(TestCase):
    def __init__(self, *args, **kwargs):
        self.__reader: Reader = Reader()
        self.__writer: Writer = Writer()
        self.__dummy_path_name: str = 'dummy'
        self.__lines_range: int = 10
        self.__ignore = default_ignore_patterns
        super().__init__(*args, **kwargs)

    def __create_dummy_path(self):
        makedirs(self.__dummy_path_name)
        for ignore_pattern in self.__ignore:
            if ignore_pattern.startswith('/'):
                makedirs(f'{self.__dummy_path_name}\\{ignore_pattern}')
            elif ignore_pattern.startswith('*'):
                with open(f'{self.__dummy_path_name}\\test{ignore_pattern[1:]}', 'w') as file:
                    for number in range(self.__lines_range):
                        file.write(f'{number}\n')
            else:
                with open(f'{self.__dummy_path_name}\\{ignore_pattern}', 'w') as file:
                    for number in range(self.__lines_range):
                        file.write(f'{number}\n')

    def __create_path_in_dummy_path(self, path_name: str):
        if not os_path.exists(f'{self.__dummy_path_name}\\{path_name}'):
            makedirs(f'{self.__dummy_path_name}\\{path_name}')

    def __create_file_in_dummy_path(self, file_name: str):
        if file_name.startswith('*'):
            file_name = f'test{file_name[1:]}'
        elif file_name.startswith('.'):
            file_name = f'test{file_name}'

        if not os_path.exists(f'{self.__dummy_path_name}\\{file_name}'):
            with open(f'{self.__dummy_path_name}\\{file_name}', 'w') as file:
                for number in range(self.__lines_range):
                    file.write(f'{number}\n')

    def __add_to_ignore_file(self, ignore: str):
        if not os_path.exists(f'{self.__dummy_path_name}\\.counterignore'):
            self.__writer.create_ignore_file(self.__dummy_path_name)
        with open(f'{self.__dummy_path_name}\\.counterignore', 'a') as ignore_file:
            ignore_file.write(f'{ignore}\n')

    def __delete_dummy_path(self):
        if os_path.exists(self.__dummy_path_name):
            rmtree(self.__dummy_path_name)

    def setUp(self):
        self.__delete_dummy_path()
        self.__create_dummy_path()
        super().setUp()

    def tearDown(self):
        self.__delete_dummy_path()
        super().tearDown()

    def test_add_to_ignore_file(self):
        path_name: str = '/my_tests'
        file_name: str = 'test.js'
        self.__add_to_ignore_file(path_name)
        self.__add_to_ignore_file(file_name)
        ignore_patterns: [str] = []

        with open(f'{self.__dummy_path_name}\\.counterignore', 'r') as ignore_file:
            for line in ignore_file.readlines():
                ignore_patterns.append(line.strip())

        self.assertIn(path_name, ignore_patterns)
        self.assertIn(file_name, ignore_patterns)

    def test_files_and_paths_to_ignore(self):
        paths: [str] = ['/test1', '/test2', '/test3']
        files: [str] = ['*.js', '*.ts', 'test.cpp']
        ignore_patterns: [str] = paths + files

        for path in paths:
            self.__create_path_in_dummy_path(path)
        for file in files:
            self.__create_file_in_dummy_path(file)
        for path in paths:
            with open(f'{self.__dummy_path_name}\\{path}\\test.js', 'w') as file:
                for number in range(self.__lines_range):
                    file.write(f'{number}\n')
        for pattern in ignore_patterns:
            self.__add_to_ignore_file(pattern)

        files_to_count: [str] = ['file.txt', 'script.py', 'main.java']
        for file in files_to_count:
            self.__create_file_in_dummy_path(file)

        lines_from_files = len(files_to_count) * self.__lines_range
        total_lines = self.__reader.count_lines(self.__dummy_path_name)
        self.assertEqual(lines_from_files, total_lines)


if __name__ == '__main__':
    system_exit(main)

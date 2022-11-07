from unittest import TestCase, main
from os import remove, path as os_path
from sys import exit as system_exit
from felips_counter.src.writer import Writer
from felips_counter import default_ignore_patterns


class TestCounterIgnoreFile(TestCase):
    def __init__(self, *args, **kwargs):
        self.__writer: Writer = Writer()
        self.__ignore_file_name: str = '.counterignore'
        self.__default_ignore_patterns: [str] = default_ignore_patterns
        super().__init__(*args, **kwargs)

    def __delete_ignore_file(self):
        if os_path.exists(self.__ignore_file_name):
            remove(self.__ignore_file_name)

    def __create_ignore_file(self):
        self.__writer.create_ignore_file()

    def setUp(self):
        self.__delete_ignore_file()
        self.__create_ignore_file()
        super().setUp()

    def tearDown(self):
        self.__delete_ignore_file()
        super().tearDown()

    def test_ignore_file_creation(self):
        self.assertEqual(True, os_path.exists(self.__ignore_file_name))

    def test_default_ignore_patters(self):
        ignore_patterns: [str] = []
        with open(self.__ignore_file_name, 'r') as ignore_file:
            for line in ignore_file.readlines():
                ignore_patterns.append(line.strip())

        self.assertListEqual(self.__default_ignore_patterns, ignore_patterns)

    def test_ignore_file_override_lock(self):
        with self.assertRaises(FileExistsError):
            self.__create_ignore_file()


if __name__ == '__main__':
    system_exit(main())

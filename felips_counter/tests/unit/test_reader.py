from unittest import TestCase, main
from os import remove, path as os_path, open as os_open, O_WRONLY, O_CREAT, umask as os_umask, chmod
from stat import S_IWUSR
from sys import exit as system_exit
from felips_counter.src.reader import Reader


class TestReader(TestCase):
    def __init__(self, *args, **kwargs):
        self.__reader: Reader = Reader()
        self.__dummy_file_name: str = 'dummy.txt'
        self.__protected_dummy_file_name: str = 'protected-dummy.txt'
        self.__lines_range = 120
        super().__init__(*args, **kwargs)

    def __create_dummy_files(self):
        with open(self.__dummy_file_name, 'w') as dummy_file:
            for number in range(self.__lines_range):
                dummy_file.write(f'{number}\n\n')

        flags: int = O_WRONLY | O_CREAT
        mode: int = S_IWUSR
        umask: int = 0o666
        umask_original: int = os_umask(umask)

        try:
            protected_file = os_open(self.__protected_dummy_file_name, flags, mode)
        finally:
            os_umask(umask_original)

        with open(protected_file, 'w') as protected_dummy_file:
            for number in range(self.__lines_range):
                protected_dummy_file.write(f'{number}\n')

    def __delete_dummy_files(self):
        if os_path.exists(self.__dummy_file_name):
            remove(self.__dummy_file_name)

        if os_path.exists(self.__protected_dummy_file_name):
            mode: int = 0o666
            chmod(self.__protected_dummy_file_name, mode)
            remove(self.__protected_dummy_file_name)

    def setUp(self):
        self.__delete_dummy_files()
        self.__create_dummy_files()
        super().setUp()

    def tearDown(self):
        self.__delete_dummy_files()
        super().tearDown()

    def test_total_line_count(self):
        total_lines: int = self.__reader.count_lines(self.__dummy_file_name)
        self.assertEqual(self.__lines_range, total_lines)

    def test_total_line_count_with_blank_lines(self):
        self.__reader = Reader(ignore_blank_lines=False)
        total_lines = self.__reader.count_lines(self.__dummy_file_name)
        self.assertEqual(self.__lines_range * 2, total_lines)

    def test_decode_with_another_encoding(self):
        with open(self.__dummy_file_name, 'w', encoding='latin-1') as document:
            document.write('\xac')
        self.__reader: Reader = Reader(encoding='latin-1')
        total_lines: int = self.__reader.count_lines(self.__dummy_file_name)
        self.assertEqual(1, total_lines)

    def test_lookup_raise(self):
        with self.assertRaises(LookupError):
            self.__reader: Reader = Reader(encoding='DUMMY')
            self.__reader.count_lines(self.__dummy_file_name)

    def test_permission_raise(self):
        with self.assertRaises(PermissionError):
            self.__create_dummy_files()
            self.__reader.count_lines(self.__protected_dummy_file_name)

    def test_decode_raise(self):
        with self.assertRaises(UnicodeDecodeError):
            with open(self.__dummy_file_name, 'w', encoding='latin-1') as document:
                document.write('\xac')
            self.__reader.count_lines(self.__dummy_file_name)

    def test_not_directory_raise(self):
        with self.assertRaises(NotADirectoryError):
            self.__reader.count_lines('ABC:\\Documents')


if __name__ == '__main__':
    system_exit(main())

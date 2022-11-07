from os import path as os_path, listdir
from felips_counter import default_ignore_patterns


class Reader:
    def __init__(self, ignore_blank_lines: bool = True, encoding: str = 'UTF-8'):
        self.__ignore_blank_lines: bool = ignore_blank_lines
        self.__encoding: str = encoding
        self.__ignore: [str] = default_ignore_patterns

    def __count_document_lines(self, document_path: str) -> int:
        """
        Open a document and count its lines.

        :param document_path: The document path.
        :return: The number of lines of the document.
        """

        unicode_bytes: bytes = b'\x00'

        try:
            with open(document_path, encoding=self.__encoding) as document:
                document_lines: [str] = document.readlines()
                lines_length: int = len(document_lines)

                for line in document_lines:
                    if isinstance(line, bytes):
                        unicode_bytes = line
                    if self.__ignore_blank_lines and line == '\n':
                        lines_length -= 1
            return lines_length

        except PermissionError:
            raise PermissionError(f'The {document_path} file could not be opened because '
                                  f'permission to access it was denied.')

        except UnicodeDecodeError:
            raise UnicodeDecodeError(self.__encoding, unicode_bytes, 1, 1,
                                     f'{self.__encoding} can\'t decode {unicode_bytes} bytes.')

        except LookupError:
            raise LookupError(f'The {document_path} file has an unknown encoding.')

    @staticmethod
    def __get_ignore_config(ignore_file: str) -> [str]:
        ignore_patterns: [str] = ['.counterignore']
        with open(ignore_file) as document:
            document_lines: [str] = document.readlines()
            for line in document_lines:
                if line[0] == '/' or line[0] == '*':
                    line = line[1:]
                elif line[0] == '#' or line == '\n':
                    continue
                ignore_patterns.append(line.split('\n')[0])
        return ignore_patterns

    def count_lines(self, path: str = '.\\', total_lines: int = 0) -> int:
        """
        Opens a path to count its documents lines

        :param path: The path to open its documents
        :param total_lines: The number of lines
        :return: The total lines
        """

        ignore_patterns: [str] = []
        for ignore_pattern in self.__ignore:
            if ignore_pattern[0] == '/' or ignore_pattern[0] == '*':
                ignore_patterns.append(ignore_pattern[1:])
            ignore_patterns.append(ignore_pattern)
        self.__ignore = ignore_patterns

        isdir: bool = os_path.isdir(path)
        isfile: bool = os_path.isfile(path)

        if isdir:
            documents = listdir(path)
            if '.counterignore' in documents:
                ignore_file: str = path + '\\.counterignore'
                self.__ignore = self.__get_ignore_config(ignore_file)
            for document in documents:
                document_path = os_path.join(path, document)
                if os_path.isdir(document_path):
                    if os_path.split(document_path)[-1] in self.__ignore:
                        continue
                    total_lines += self.count_lines(document_path)
                elif os_path.isfile(document_path):
                    if os_path.split(document_path)[-1] in self.__ignore:
                        continue
                    if os_path.splitext(document_path)[-1] in self.__ignore:
                        continue
                    total_lines += self.__count_document_lines(document_path)
        elif isfile:
            total_lines += self.__count_document_lines(path)
        else:
            raise NotADirectoryError(f'"{path}" is not a valid directory.')

        return total_lines

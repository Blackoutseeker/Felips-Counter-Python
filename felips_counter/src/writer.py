from os import path as os_path
from felips_counter import default_ignore_patterns


class Writer:
    @staticmethod
    def create_ignore_file(ignore_file_path: str = '.\\') -> None:
        """
        Creates a ".counterignore" file at the given path

        :param ignore_file_path: The path to create the ".counterignore" file
        """

        if os_path.exists(f'{ignore_file_path}\\.counterignore'):
            raise FileExistsError('.counterignore file has already been created.')

        with open(f'{ignore_file_path}\\.counterignore', 'w', encoding='UTF-8') as ignore_file:
            for ignore_pattern in default_ignore_patterns:
                ignore_file.write(f'{ignore_pattern}\n')

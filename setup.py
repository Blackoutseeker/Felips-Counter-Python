#!/usr/bin/env python3

from setuptools import setup, find_packages
from felips_counter import __version__ as version

if __name__ == '__main__':
    with open('README.md', 'r') as readme:
        LONG_DESCRIPTION = readme.read()

    setup(
        name='felips-counter',
        version=version,
        author='Blackoutseeker (Felipe Pereira)',
        author_email='felipsdev@gmail.com',
        url='https://github.com/Blackoutseeker/Felips-Counter-Python',
        project_urls={
            'Source': 'https://github.com/Blackoutseeker/Felips-Counter-Python',
            'Funding': 'https://www.paypal.com/donate/?hosted_button_id=NEXQJS4U5HGC6',
            'Tracker': 'https://github.com/Blackoutseeker/Felips-Counter-Python/issues',
        },
        license='MIT',
        packages=find_packages(exclude='tests'),
        python_requires='>=3.7',
        install_requires=['colorama~=0.4.6'],
        description='Count your project lines easily!',
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Topic :: Utilities',
            'Topic :: Terminals',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3 :: Only',
            'Operating System :: Microsoft :: Windows'
        ],
        keywords=['blackoutseeker', 'felips', 'counter'],
        entry_points={
            'console_scripts': [
                'counter=felips_counter.__main__:main'
            ]
        }
    )

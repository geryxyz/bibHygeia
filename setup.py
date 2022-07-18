import os

import setuptools


def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'requirements.txt'), 'r') as f:
    REQUIRES = f.read().splitlines()

VERSION = get_version('src/__init__.py')

setuptools.setup(
    name='bibhygeia',
    version=VERSION,
    packages=setuptools.find_packages(),
    package_data={'src.report_generator': ['resources/*']},
    entry_points={
        'console_scripts': [
            'bibhygeia=src.__main__:main'
        ]
    },
    setup_requires=['setuptools>=46.4.0'],
    install_requires=REQUIRES,
    python_requires='>=3.9',
    url='https://github.com/sznorbert07/bibHygeia',
    license='GNU General Public License v3.0',
    author='Norbert Szekely',
    author_email='',
    description=''
)

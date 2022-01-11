
import os
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install


setup(
    data_files = [
        (os.path.join('latex', 'invoice'), [
            'latex/constants.tex',
            'latex/main.tex',
            'latex/preambule.tex',
        ]),
    ],
    packages=['time_monitor'],
    package_dir={'time_monitor': 'src/time_monitor'},
    python_requires='>=3.6',
)

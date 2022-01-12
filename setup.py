"""Setup file"""
import os
from setuptools import setup


setup(
    data_files=[
        (os.path.join('latex', 'invoice'), [
            'latex/constants.tex',
            'latex/main.tex',
            'latex/preambule.tex',
        ]),
    ],
    packages=['time_monitor'],
    package_dir={'time_monitor': 'src/time_monitor'},
    python_requires='>=3.6',
    setup_requires=[
        'flake8',
        'pytest-runner'
    ],
    tests_require=['pytest'],
)

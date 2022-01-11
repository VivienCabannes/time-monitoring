
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install


def init_buffers():
    import csv
    import os
    from pathlib import Path
    import shutil

    CODE_PATH = Path.home() / 'time-monitoring'
    DATA_PATH = CODE_PATH / 'data'
    LATEX_PATH = CODE_PATH / 'latex'
    BUFFER_FILE = CODE_PATH / '.activity'
    REPORT_FILE = CODE_PATH / '.current_report.csv'

    if not CODE_PATH.exists():
        os.mkdir(CODE_PATH)
    if not DATA_PATH.exists():
        os.mkdir(DATA_PATH)
    if not BUFFER_FILE.exists():
        with open(BUFFER_FILE, 'w', newline='') as f:
            pass
    if not REPORT_FILE.exists():
        header = ['activity' , 'begin' , 'end' , 'length' , 'message',]
        with open(REPORT_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
    if not (DATA_PATH / '.report_numbers').exists():
        header = ['year' , 'month' , 'number']
        with open(DATA_PATH / '.report_numbers', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)

    latex_src = str(Path(__file__).resolve().parents[0] / 'latex')
    shutil.copytree(latex_src, LATEX_PATH, symlinks=True)


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        init_buffers()

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        init_buffers()


setup(
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    packages=['time_monitor'],
    package_dir={'time_monitor': 'src/time_monitor'},
    python_requires='>=3.6',
)

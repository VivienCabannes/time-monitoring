
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install


def init_buffers():
    import csv
    import os
    import src.time_monitor.config as cf

    if not cf.BUFFER_FILE.exists():
        with open(cf.BUFFER_FILE, 'w', newline='') as f:
            pass
    if not cf.REPORT_FILE.exists():
        header = ['activity' , 'begin' , 'end' , 'length' , 'message',]
        with open(cf.REPORT_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
    if not cf.DATA_PATH.exists():
        os.mkdir(cf.DATA_PATH)
    if not (cf.DATA_PATH / '.report_numbers').exists():
        header = ['year' , 'month' , 'number']
        with open(cf.DATA_PATH / '.report_numbers', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)

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

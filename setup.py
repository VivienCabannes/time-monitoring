
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install


def init_buffers():
    import csv
    import os
    import time_monitor.config as cf

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
    name='time-monitor',
    description='Time monitoring with shell command',
    keywords='time monitoring invoice',
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    packages=['time_monitor'],
    scripts=[
        'bin/begin',
        'bin/message',
        'bin/stop',
        'bin/time_report',
        'bin/check_activity',
        'bin/check_stats',
        'bin/geninv',
    ],
    author='Vivien Cabannes',
    author_email='vivien.cabannes@gmail.com',
    version='0.0.1',
    license='MIT',
)


from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install


def init_buffers(bf, rf):
    import csv
    if not bf.exists():
        with open(bf, 'w', newline='') as f:
            pass
    if not rf.exists():
        header = ['year', 'month', 'number']
        with open(rf, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        import time_monitor.config as cf
        init_buffers(cf.BUFFER_FILE, cf.REPORT_FILE)

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        import time_monitor.config as cf
        init_buffers(cf.BUFFER_FILE, cf.REPORT_FILE)


setup(
    name='time-monitor',
    description='Time monitoring with shell command',
    keywords='time monitoring invoice',
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    package=['time_monitor'],
    scripts=[
        'bin/begin',
        'bin/message',
        'bin/stop',
        'bin/geninv',
    ],
    author='Vivien Cabannes',
    author_email='vivien.cabannes@gmail.com',
    version='0.0.1',
    license='MIT',
)

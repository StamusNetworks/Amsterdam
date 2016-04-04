#!/usr/bin/env python
from setuptools import setup
from src.amsterdam import AMSTERDAM_VERSION
import os

data_files = []
dir_list = ['docker', 'config', 'templates']
os.chdir('src')
for directory in dir_list:
    for (dir, _, files) in os.walk(directory):
        for f in files:
            if not f.startswith('.') and not f.endswith('pyc'):
                path = os.path.join(dir, f)
                data_files.append(path)
os.chdir('..')


setup(name='amsterdam',
      version=AMSTERDAM_VERSION,
      description='Suricata, ELK, Scirius on Docker',
      author='Stamus Networks',
      author_email='oss@stamus-networks.com',
      url='https://github.com/StamusNetworks/amsterdam',
      scripts=['amsterdam'],
      packages=['amsterdam'],
      package_dir={'amsterdam':'src'},
      package_data={'amsterdam': data_files},
      provides=['amsterdam'],
      install_requires=['argparse', "docker-compose", 'pyOpenSSL'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Security',
          ],
      )

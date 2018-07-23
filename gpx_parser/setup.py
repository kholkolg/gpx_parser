from setuptools import setup

setup(
   name='gpx-parser',
   version='0.1',
   description='Parser for simple gpx data',
   author='Olga',
   author_email='',
   license='MIT',
   packages=['gpx_parser'],
   url = 'https://github.com/aicenter/roadmap-processing',
   download_url = 'https://github.com/aicenter/roadmap-processing/archive/0.2.5.tar.gz',
   install_requires=['typing','setuptools','xml'],
)

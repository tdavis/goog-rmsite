import sys
from setuptools import setup


version = '1.0'
pyversion = sys.version_info[0:2]
dependencies = [
    'PyVirtualDisplay==0.0.6',
    'selenium==2.7.0',
]
if pyversion[0] == 2 and pyversion[1] < 7:
    dependencies.append('argparse')


setup(name='goog-rmsite',
      install_requires=dependencies,
      version=version,
      description='Selenium (Python) script for deleting Google Sites',
      author='Tom Davis',
      author_email='tom@recursivedream.com',
      url='http://recursivedream.com',
      license='MIT',
      py_modules = ['sites_delete'],
      entry_points = { 'console_scripts': [ 'rmsite = sites_delete:main', ] },
     )

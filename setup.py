"""
Setup
-----

This compiles all the Fortran extensions.
"""
from __future__ import absolute_import

import os
import setuptools  # Must be imported before numpy.distutils to build binary wheels

from distutils.command.sdist import sdist
from numpy.distutils.core import Extension, setup, Command, numpy_cmdclass

import versioneer


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys, subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)

foo = {'sdist': sdist}
my_cmdclass = versioneer.get_cmdclass(foo)
my_cmdclass['test'] = PyTest
#my_cmdclass['sdist'] = sdist # Make sure the sdist includes everything

setup(
    name='fc',
    version=versioneer.get_version(),
    cmdclass=my_cmdclass,
    description='Geoscience Australia - Fractional Cover for Digital Earth Australia',
    long_description=open('README.rst', 'r').read(),
    license='Apache License 2.0',
    url='https://github.com/GeoscienceAustralia/fc',
    maintainer='Geoscience Australia',
    maintainer_email='earth.observation@ga.gov.au',
    packages=['fc', 'fc.unmix'],
    data_files=[('fc/config/', ['config/ls5_fc_albers.yaml', 'config/ls7_fc_albers.yaml', 'config/ls8_fc_albers.yaml'])],
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'numpy',
        'numexpr',
        'datacube',
        'click>=5.0',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'datacube-fc = fc.fc_app:cli',
        ]
    },
    ext_modules=[
        Extension(
            name='fc.unmix.unmiximage',
            sources=[
                'fc/unmix/unmiximage.f90',
                'fc/unmix/constants_NSWC.f90',
                'fc/unmix/nnls.f90',
                'fc/unmix/unmiximage.pyf',
            ],
        )
    ],
)

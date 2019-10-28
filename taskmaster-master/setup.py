#!/usr/bin/python

from setuptools import setup, find_packages

setup(
    name="taskmaster",
    license='Apache License 2.0',
    version="0.8.2",
    description=("A simple distributed queue designed for "
                 "handling one-off tasks with large sets of tasks"),
    author="David Cramer",
    author_email="dcramer@gmail.com",
    url="https://github.com/dcramer/taskmaster",
    packages=find_packages("src"),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'tm-master = taskmaster.cli.master:main',
            'tm-slave = taskmaster.cli.slave:main',
            'tm-spawn = taskmaster.cli.spawn:main',
            'tm-run = taskmaster.cli.run:main',
        ],
    },
    install_requires=[
        'progressbar',
        'gevent',
        'gevent_zeromq',
        # 'pyzmq-static',
    ],
    tests_require=[
        'unittest2',
        'Nose>=1.0',
    ],
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Utilities",
    ])

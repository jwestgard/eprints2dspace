from setuptools import find_packages, setup

setup(
    name='eprints2dspace',
    version='0.1',
    description='ETL script for migrating data from Eprints to Dspace.',
    author='Joshua A. Westgard',
    author_email="westgard@umd.edu",
    platforms=["any"],
    license="BSD",
    url="http://github.com/jwestgard/eprints2dspace",
    packages=find_packages(),
    entry_points = {
        'console_scripts': ['eprints2dspace=e2d.__main__:main']
        },
    install_requires=[i.strip() for i in open("requirements.txt").readlines()]
)
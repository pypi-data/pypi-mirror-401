from setuptools import setup, find_packages

setup(
    name='tanzania_locations',
    version='1.2.0',
    author='Cornel Mtavangu',
    packages = find_packages(),
    install_requires=[],
    description='A package for managing Tanzania locations data',
    
    # enable CLI commands
    entry_points={
        'console_scripts': [
            'tanzania_locations = tanzania_locations.cli:main',
        ],
    },
)
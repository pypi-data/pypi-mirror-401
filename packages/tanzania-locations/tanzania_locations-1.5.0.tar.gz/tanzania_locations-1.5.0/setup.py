
from setuptools import setup, find_packages
from pathlib import Path

here = Path(__file__).parent

# Read README.md
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="tanzania-locations",            # Package name on PyPI
    version="1.5.0",
    description="Tanzania regions and districts package",
    long_description=long_description,   # This is the key part
    long_description_content_type="text/markdown",  # Markdown support
    url="https://github.com/yourusername/tanzania-locations",  # Optional
    author="Cornel Mtavangu",
    author_email="mtavangucornel@gmail.com",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[],                  # Add dependencies if needed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
    # enable CLI commands
    entry_points={
        'console_scripts': [
            'tanzania_locations = tanzania_locations.cli:main',
        ],
    },
)
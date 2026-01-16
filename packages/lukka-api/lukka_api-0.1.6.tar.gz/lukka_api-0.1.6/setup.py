"""
Setup configuration for lukka-api package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = (this_directory / "requirements.txt").read_text().splitlines()

setup(
    name="lukka-api",
    version="0.1.6",
    author="KENOT-IO",
    author_email="your-email@example.com",  # Update with your email
    description="Python client for Lukka cryptocurrency data API with distributed caching",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KENOT-IO/lukka-api",
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.13",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
            "bandit>=1.7.0",
        ],
        "redis": [
            "redis>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            # Add CLI commands here if needed in the future
            # "lukka-cli=lukka_api.cli:main",
        ],
    },
    keywords="lukka cryptocurrency bitcoin ethereum crypto api data finance",
    project_urls={
        "Bug Reports": "https://github.com/KENOT-IO/lukka-api/issues",
        "Source": "https://github.com/KENOT-IO/lukka-api",
        "Documentation": "https://github.com/KENOT-IO/lukka-api#readme",
    },
)

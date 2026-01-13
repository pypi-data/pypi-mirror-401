from setuptools import setup, find_packages
from pathlib import Path

VERSION = "1.0.1"
DESCRIPTION = "ght: Github CLI Tool"
this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="githubclitool",
    version=VERSION,
    author="Trần Hạo Nguyên || Bugdev",
    author_email="haonguyen2100hn@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["requests"],
    entry_points={"console_scripts": ["ght=githubclitool.cli:Main"]}
,
    keywords=["github", "cli", "tool", "repo", "security"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires=">=3.9",
)
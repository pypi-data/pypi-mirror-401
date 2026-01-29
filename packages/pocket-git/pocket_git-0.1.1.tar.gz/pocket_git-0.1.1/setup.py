from setuptools import setup, find_packages

with open("README.md", "r",
encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pocket-git",
    version="0.1.1",
    author="Jainil Dadhaniya",
    author_email="jdadhaniya6@gmail.com",
    description="A minimal git implementation that fits in your pocket",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vibey19/pocket-git",
    packages=find_packages(),
    classifiers=[
        "Intended Audience :: Education"
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "pocket-git=pocket_git.__main__:main",
            "pgit=pocket_git.__main__:main",
        ],
    },
)
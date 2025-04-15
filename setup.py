from setuptools import setup, find_packages

setup(
    name="mr. Jozef",
    version="1.0.0",
    author="Team Oldies",
    author_email="grachovdev@gmail.com",
    description="A CLI assistant bot for managing contacts and notes.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/EugenGrachov/mr.-Jozef",
    packages=find_packages(),
    install_requires=[
        "prettytable",
    ],
    entry_points={
        "console_scripts": [
            "mrjozef=mrjozef.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)

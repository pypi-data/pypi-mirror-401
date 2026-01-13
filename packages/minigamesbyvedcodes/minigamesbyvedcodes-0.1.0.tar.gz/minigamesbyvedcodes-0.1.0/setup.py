from setuptools import setup, find_packages

setup(
    name="minigamesbyvedcodes",
    version="0.1.0",
    author="Ved Vyas (aka Ved Codes)",
    author_email="vedcodes2312.dev@gmail.com",
    description="A simple Python games library (Tic Tac Toe, RPS, Maths Quiz)",
    long_description=open("README.md",encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

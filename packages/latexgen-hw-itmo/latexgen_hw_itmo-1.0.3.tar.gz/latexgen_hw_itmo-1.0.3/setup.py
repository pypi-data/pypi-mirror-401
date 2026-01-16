from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = {}
with open("latexgen/__version__.py", "r", encoding="utf-8") as fh:
    exec(fh.read(), version)

setup(
    name="latexgen-hw-itmo",
    version=version["__version__"],
    author="sudokushifter",
    author_email="zanid227@yandex.ru",
    description="LaTeX table and image generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ваш-username/latexgen",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Markup :: LaTeX",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    keywords="latex, generator, table, image, pdf",
    install_requires=[],
)

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="spark-cli",
    version="0.4.1",
    author="zeroequalsone",
    author_email="hi@sgoetze.de",
    description="Your intelligent code snippet manager for developers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zeroequalsone/spark-cli",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.0.0",
        "pyperclip>=1.8.0",
    ],
    entry_points={
        "console_scripts": [
            "spark=spark.cli:app",
        ],
    },
    python_requires=">=3.8",
)

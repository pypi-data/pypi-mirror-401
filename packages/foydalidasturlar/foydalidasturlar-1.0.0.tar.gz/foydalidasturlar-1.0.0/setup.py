from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="foydalidasturlar",
    version="1.0.0",
    author="Sizning ismingiz",
    author_email="sizning_emailingiz@gmail.com",
    description="Turli xil tasodifiy ma'lumotlar generatori",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sizning_username/foydalidasturlar",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    install_requires=[],
    keywords="generator, fake data, random, uzbekistan, test data",
)
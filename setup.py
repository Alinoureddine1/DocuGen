from setuptools import setup, find_packages
import subprocess
import sys
from setuptools.command.develop import develop
from setuptools.command.install import install

def download_nltk_data():
    subprocess.check_call([sys.executable, "-m", "nltk.downloader", "punkt", "averaged_perceptron_tagger", "wordnet"])

class PostDevelopCommand(develop):
    def run(self):
        develop.run(self)
        download_nltk_data()

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        download_nltk_data()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="docugen",
    version="0.1.0",
    author="AliNoureddine1",
    author_email="docugen@example.com",
    description="A tool to generate files from Wikipedia articles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Alinoureddine1/DocuGen",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "nltk",
        "wikipedia",
        "python-docx",
        "reportlab",
        "tqdm",
        "names",
        "beautifulsoup4",
    ],
    extras_require={
        "dev": [
            "pytest",
            "flake8",
        ],
    },
    entry_points={
        "console_scripts": [
            "docugen=docugen.docugen:main",
        ],
    },
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
)
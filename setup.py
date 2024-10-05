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

setup(
    name="docugen",
    version="0.1.0",
    author="AliNoureddine1",
    author_email="docugen@example.com",
    description="A tool to generate files from Wikipedia articles",
    packages=find_packages(),
    install_requires=[
        "nltk",
        "wikipedia",
        "python-docx",
        "reportlab",
        "tqdm",
        "names",
        "beautifulsoup4",
    ],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    entry_points={
        "console_scripts": [
            "docugen=docugen.docugen:main",
        ],
    },
)
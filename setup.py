from setuptools import setup, find_packages
import subprocess
import sys
import os
from setuptools.command.develop import develop
from setuptools.command.install import install

def run_nltk_downloader():
    downloader_path = os.path.join('scripts', 'nltk_downloader.py')
    subprocess.check_call([sys.executable, downloader_path])

class PostDevelopCommand(develop):
    def run(self):
        develop.run(self)
        run_nltk_downloader()

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        run_nltk_downloader()

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
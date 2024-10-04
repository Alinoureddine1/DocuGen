from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="docugen",
    version="0.1.0",
    author="AliNoureddine1",
    author_email="docugen@example.com",
    description="A tool to files from Wikipedia articles",
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
)
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="docugen",
    version="0.1.0",
    author="Ali Noureddine",
    author_email="noureddine.ali@outlook.com.com",
    description="A tool to generate files from Wikipedia articles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Alinoureddine1/DocuGen",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
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
    entry_points={
        "console_scripts": [
            "docugen=docugen.docugen:main",
        ],
    },
)
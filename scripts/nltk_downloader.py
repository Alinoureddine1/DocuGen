import nltk
import ssl
import sys
import subprocess

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def download_nltk_data():
    nltk_resources = [
        "punkt",
        "averaged_perceptron_tagger",
        "wordnet",
        "punkt_tab",
        "averaged_perceptron_tagger_eng"
    ]
    for resource in nltk_resources:
        try:
            nltk.download(resource, quiet=True)
            print(f"Successfully downloaded {resource}")
        except Exception as e:
            print(f"Failed to download {resource}: {str(e)}")

if __name__ == "__main__":
    download_nltk_data()
    print("NLTK data download process completed.")
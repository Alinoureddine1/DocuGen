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
    nltk_resources = ["punkt", "averaged_perceptron_tagger", "wordnet", "punkt_tab"]
    for resource in nltk_resources:
        subprocess.check_call([sys.executable, "-m", "nltk.downloader", resource])

if __name__ == "__main__":
    download_nltk_data()
    print("NLTK data downloaded successfully.")
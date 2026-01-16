from setuptools import setup, find_packages

setup(
    name="nececv",
    version="0.2.6",   # bump version
    description="NECECV – LLMs, Computer Vision, and Enterprise Semantic Cache",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Singhai Kshitij Jain",
    author_email="singhaikshitij143@gmail.com",
    url="https://github.com/singhaikshitijjain/nececv",
    packages=find_packages(),   # auto-includes semantic_cache
    install_requires=[
        "numpy",
        "Pillow",
        "tensorflow",
        "opencv-python",
        "matplotlib",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
from setuptools import setup, find_packages

setup(
    name="nececv",
    version="0.2.3",   # bump version
    description="NECECV – LLMs, Computer Vision, and Enterprise Semantic Cache",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Singhai Kshitij Jain",
    author_email="singhaikshitij143@gmail.com",
    url="https://github.com/singhaikshitijjain/nececv",
    packages=find_packages(),   # auto-includes semantic_cache
    install_requires=[
        "numpy",
        "Pillow",
        "tensorflow",
        "opencv-python",
        "matplotlib",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

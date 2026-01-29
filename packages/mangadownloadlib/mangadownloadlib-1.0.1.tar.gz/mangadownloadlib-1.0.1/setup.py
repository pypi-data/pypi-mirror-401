from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

with open("requirements.txt", "r", encoding="utf8") as f:
    requirements = f.read().splitlines()

setup(
    name="mangadownloadlib",
    version="1.0.1",
    description="Python library to parse and download manga from the web",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NikitaVolya/MangaDownloader",
    author="NikitaVolia",
    author_email="volanskkijnikita2@gmail.com",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
    install_requires=requirements,
)
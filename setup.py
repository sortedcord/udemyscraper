from setuptools import setup

metadata={}
with open("udemyscraper/metadata.py",encoding='utf-8') as fp:
    exec(fp.read(), metadata)

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name= metadata['__package_name__'],
    version=metadata['__version__'],
    author = metadata['__author__'],
    author_email = metadata['__author_email__'],
    description= metadata['__description__'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url= "https://github.com/sortedcord/udemyscraper",
    project_urls={
        "Bug Tracker": "https://github.com/sortedcord/udemyscraper/issues",
    },
    package_dir = {
            'udemyscraper.export': 'udemyscraper/export'},
    packages=['udemyscraper', 'udemyscraper.export'],
    entry_points = {
        'console_scripts': ['udemyscraper=udemyscraper.udscraperscript:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    install_requires = [
        "alive-progress==1.6.2",
        "appdirs==1.4.4",
        "beautifulsoup4==4.9.3",
        "bs4==0.0.1",
        "certifi==2021.5.30",
        "charset-normalizer==2.0.4",
        "colorama==0.4.4",
        "configparser==5.0.2",
        "crayons==0.4.0",
        "cssselect==1.1.0",
        "fake-useragent==0.1.11",
        "idna==3.2",
        "lxml==4.6.5",
        "pyee==8.2.2",
        "pyquery==1.4.3",
        "requests==2.26.0",
        "selenium==3.141.0",
        "soupsieve==2.2.1",
        "tqdm==4.62.2",
        "urllib3==1.26.6",
        "webdriver-manager==3.4.2",
        "msedge-selenium-tools==3.141.3",
        "dict2xml==1.7.0",
        "dicttoxml==1.7.4"
    ],
    extras_require = {
        "dev": [
            "pytest>=3.7",
        ],
    },

)

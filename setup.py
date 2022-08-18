from setuptools import setup

"""
:authors: ymoth
:copyright (c) 2022 ymoth
"""

version = "1.0.0"

setup(
    name="quote_manager",
    version=version,
    author="ymoth",
    author_email="tophanbig@gmail.com",
    url="https://github.com/ymoth/quote-manager",
    download_url="https://github.com/ymoth/quote-manager/archives/main.zip",
    packages=["aiohttp", "requests", "Pillow"]
)

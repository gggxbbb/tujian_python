# -*- coding: utf-8 -*-  

import setuptools

with open("README.md", "r" , encoding='UTF-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="tu",
    version="0.0.4",
    author="gggxbbb",
    author_email="gamegxb@163.com",
    description="A simlpe tool for Tujian",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gggxbbb/tujian_python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
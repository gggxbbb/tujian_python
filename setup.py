# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyTujian",
    version="0.0.31",
    author="gggxbbb",
    author_email="gamegxb@163.com",
    description="A simlpe tool for Tujian",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gggxbbb/tujian_python",
    packages=setuptools.find_packages(),
    python_requires='>=3',
    install_requires=[
        #'qrcode>=6.0',
        #'pillow>=6.0.0',
        #'image>=1.5.0',
        'PyYAML>=5.1.2',
        #'dhash>=1.3'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': [
            'PyTujian = PyTujian.__main__:main'
        ]
    }
)

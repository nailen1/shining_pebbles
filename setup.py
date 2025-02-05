import os
from setuptools import setup, find_packages, Extension
import numpy


extensions = [
    Extension(
        "shining_pebbles.some_extension",  # 확장 모듈 이름
        sources=["shining_pebbles/some_extension.c"],  # 소스 파일
        include_dirs=[numpy.get_include()],  # NumPy 헤더 포함
    ),
]

setup(
    name='shining_pebbles',
    version='0.2.73',
    packages=find_packages(),
     install_requires=[
        'numpy>=1.21.0',  # NumPy 1.x와 2.x 모두 지원
        'pandas',
        'python-dateutil',
        'pybind11>=2.12',
    ],
    setup_requires=[
        'numpy>=1.21.0',  # 빌드 시 NumPy 헤더 사용
    ],
    author='June Young Park',
    author_email='juneyoungpaak@gmail.com',
    description='A collection of utility functions that enable treating a file system of multiple files as a pseudo-database, facilitating maintenance and operations across the large-scale file system. My shining pebbles.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nailen1/shining_pebbles',
    project_urls={
        'Source': 'https://github.com/nailen1/shining_pebbles',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

from setuptools import setup, find_packages

setup(
    name='shining_pebbles',
    version='0.5.2',
    packages=find_packages(),
     install_requires=[
        'numpy>=1.21.0',  # NumPy 1.x와 2.x 모두 지원
        'pandas',
        'python-dateutil',
        'pybind11>=2.12',
        'aws-s3-controller>=0.7.3',
        'openpyxl>=3.1.5',
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

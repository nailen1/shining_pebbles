from setuptools import setup, find_packages

setup(
    name='shining_pebbles',
    version='0.1.9',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'python-dateutil'
    ],
    author='June Young Park',
    author_email='juneyoungpaak@gmail.com',
    description='A collection of utility functions that enable treating a file system of multiple files as a pseudo-database, facilitating maintenance and operations across the large-scale file system. My shining pebbles.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nailen1/shining_pebbles.git',  # URL of your package source code
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

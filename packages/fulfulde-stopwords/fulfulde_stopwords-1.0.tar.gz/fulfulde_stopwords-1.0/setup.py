"""
Setup script for fulfulde-stopwords package.
"""

from setuptools import setup, find_packages
import os


def read_file(filename):
    """Read a file and return its contents."""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


# Read the long description from README
try:
    long_description = read_file('README.md')
    long_description_content_type = 'text/markdown'
except FileNotFoundError:
    long_description = 'Fulfulde stopwords for Natural Language Processing'
    long_description_content_type = 'text/plain'


setup(
    name='fulfulde-stopwords',
    version='1.0.0',
    author='Research Team',
    author_email='contact@example.com',
    description='Stopwords for the Fulfulde language (Adamawa variant)',
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    url='https://github.com/2zalab/fulfulde-stopwords',
    project_urls={
        'Bug Tracker': 'https://github.com/2zalab/fulfulde-stopwords/issues',
        'Documentation': 'https://github.com/2zalab/fulfulde-stopwords#readme',
        'Source Code': 'https://github.com/2zalab/fulfulde-stopwords',
    },
    packages=find_packages(exclude=['tests', 'examples', 'paper']),
    package_data={
        'fulfulde_stopwords': ['stopwords.txt'],
    },
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords=[
        'nlp',
        'natural-language-processing',
        'stopwords',
        'fulfulde',
        'african-languages',
        'low-resource-languages',
        'text-processing',
        'computational-linguistics',
    ],
    python_requires='>=3.7',
    install_requires=[
        # No external dependencies required
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=22.0.0',
            'flake8>=5.0.0',
            'mypy>=0.990',
        ],
    },
    license='MIT',
    zip_safe=False,
)

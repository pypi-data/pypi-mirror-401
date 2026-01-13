"""
FeatureExpand - Automatic Feature Engineering Library

This setup.py is provided for backward compatibility.
For modern installations, use pyproject.toml.
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='featureexpand',
    version='0.1.0',
    packages=find_packages(exclude=['tests', 'tests.*', 'examples', 'examples.*', 'docs']),
    install_requires=[
        'numpy>=1.19.0',
        'pandas>=1.1.0',
        'scikit-learn>=0.24.0',
        'requests>=2.25.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=3.0.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
            'mypy>=0.950',
            'build>=0.8.0',
            'twine>=4.0.0',
        ],
        'docs': [
            'mkdocs>=1.4.0',
            'mkdocs-material>=8.5.0',
            'mkdocstrings[python]>=0.19.0',
        ],
    },
    author='Juan Carlos Lopez Gonzalez',
    author_email='jlopez1967@gmail.com',
    description='A powerful Python library for automatic feature engineering using logical formula simplification',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jlopezCell/featureexpand',
    project_urls={
        'Documentation': 'https://featureexpand.readthedocs.io',
        'Bug Tracker': 'https://github.com/jlopezCell/featureexpand/issues',
        'Source Code': 'https://github.com/jlopezCell/featureexpand',
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.8',
    keywords='machine-learning feature-engineering boolean-logic optimization scikit-learn',
    include_package_data=True,
    zip_safe=False,
)

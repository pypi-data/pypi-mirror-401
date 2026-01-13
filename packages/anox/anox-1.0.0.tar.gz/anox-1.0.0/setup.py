#!/usr/bin/env python3
"""Setup script for ANOX - AI Development Assistant."""

import os
from setuptools import setup, find_packages

# Read README for long description
def read_file(filename):
    """Read file contents."""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

# Read requirements
def read_requirements(filename):
    """Read requirements from file."""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    requirements = []
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                requirements = [
                    line.strip() for line in f
                    if line.strip() and not line.startswith('#')
                ]
    except (IOError, OSError) as e:
        print(f"Warning: Could not read {filename}: {e}")
        print("Using minimal requirements...")
        # Fallback to minimal core requirements
        requirements = [
            'fastapi>=0.115.0',
            'uvicorn[standard]>=0.24.0',
            'pydantic>=2.0.0',
            'python-dotenv>=1.0.0',
        ]
    return requirements

setup(
    name='anox',
    version='1.0.0',
    description='ANOX — AI-Powered Development Assistant',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author='HakunoKun',
    url='https://github.com/HakunoKun/Ai-Brain',
    python_requires='>=3.8',
    packages=find_packages(),
    install_requires=read_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'anox=main:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='ai assistant development cli chat',
)

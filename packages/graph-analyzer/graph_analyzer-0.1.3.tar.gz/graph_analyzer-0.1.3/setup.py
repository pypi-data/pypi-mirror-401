from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = [
    'numpy>=1.21.0',
    'opencv-python>=4.5.0',
    'Pillow>=8.0.0',
]

dev_requirements = [
    'pytest>=7.0.0',
    'pytest-cov>=3.0.0',
    'black>=22.0.0',
    'flake8>=4.0.0',
    'mypy>=0.950',
    'build>=0.7.0',
    'twine>=4.0.0',
]

setup(
    name='graph-analyzer',
    version='0.1.3',
    author='Hafiz Muhammad Mujadid Majeed',
    author_email='mujadid2001@gmail.com',
    description='A Python package for analyzing hand-drawn graphs from images',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mujadid2001/graph-analyzer',
    project_urls={
        'Bug Reports': 'https://github.com/mujadid2001/graph-analyzer/issues',
        'Source': 'https://github.com/mujadid2001/graph-analyzer',
    },
    packages=find_packages(exclude=['tests', 'tests.*', 'examples']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Education',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=requirements,
    extras_require={
        'dev': dev_requirements,
    },
    keywords='graph-theory, computer-vision, image-processing, education, mathematics',
    include_package_data=True,
    zip_safe=False,
)

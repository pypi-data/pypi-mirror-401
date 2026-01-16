from setuptools import setup, find_namespace_packages

with open 'README.md', 'r') as f:
    description = f.read()

setup(
    name='image_aesthetic_maps',
    version='0.2.0-alpha',
    python_requires = '>=3',
    package_dir = {'' : 'image_aesthetic_maps'},
    packages=find_namespace_packages(where = 'image_aesthetic_maps'),  # Automatically discover and include all packages
    
    # Other metadata
    author='Maarten Leemans',
    author_email='maarten.leemans@kuleuven.be',
    description='A short description of your package',
    long_description='A longer description if needed',
    url='https://github.com/yourusername/mypackage',
    classifiers=[
        # Specify trove classifiers (https://pypi.org/classifiers/)
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],

    long_description = description,
    long_description_content_type = 'text/markdown',
)
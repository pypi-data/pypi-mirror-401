from setuptools import setup, find_packages

setup(
    name='bamnet',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.18.0',
    ],
    author='Daniel Tayade',
    author_email='danieltayade2004@gmail.com',
    description='A small Python library for BAM (Bidirectional Associative Memory) networks',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dandan-077/bamnet',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)

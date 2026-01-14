from setuptools import setup, find_packages

setup(
    name='greko',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'rawpy>=0.17.0',
        'pillow>=9.0.0',
        'numpy>=1.21.0',
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='A package to process raw camera data into 1-bit bitmap images',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/bitmap',  # Update with your repo
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

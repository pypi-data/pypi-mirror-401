from setuptools import setup, find_packages

setup(
    name='DummyCalculatorPackage',
    version='0.1.0',
    author='Shiva Yadav',
    description='A sample Python Calculator package',
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    package = find_packages(),
    entry_points={
        'console_scripts': [
            'calculator=Calculator.calculator:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)


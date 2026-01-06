from setuptools import setup, find_packages

setup(
    name='chasse_express',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pygame',
    ],
    entry_points={
        'console_scripts': [
            'chasse-express=main:main'
        ]
    }
)

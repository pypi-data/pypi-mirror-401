from setuptools import setup, find_packages

setup(
    name='Topsis-Yashika-102317089', # Naming convention as per instructions
    version='1.0.0',
    packages=find_packages(),
    install_requires=['pandas', 'numpy'],
    entry_points={
        'console_scripts': [
            'topsis=102317089:main',
        ],
    },
)
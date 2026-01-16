from setuptools import setup, find_packages

setup(
    name='Topsis-Yashika-102317089',
    version='1.0.1', # Version badal diya hai
    packages=find_packages(),
    py_modules=['topsis_pkg'], # Humne file ka naya naam yahan bataya hai
    install_requires=['pandas', 'numpy'],
    entry_points={
        'console_scripts': [
            'topsis=topsis_pkg:main', # Ab ye 'topsis_pkg.py' ke main function ko call karega
        ],
    },
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
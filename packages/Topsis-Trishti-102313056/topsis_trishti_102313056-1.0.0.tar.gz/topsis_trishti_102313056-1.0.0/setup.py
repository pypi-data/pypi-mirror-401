from setuptools import setup, find_packages

setup(
    name='Topsis-Trishti-102313056',
    version='1.0.0',
    author='Trishti',
    author_email='trishti1110@gmail.com',
    description='TOPSIS implementation',
    packages=find_packages(),
    install_requires=['pandas', 'numpy'],
    entry_points={
        'console_scripts': [
            'topsis=topsis_trishti_10155792.topsis:topsis'
        ]
    },
)

from setuptools import setup

setup(
    name='pratica-1',
    description='Pratica 1 de SD, 2021.2',
    author='Allana Campos',
    install_requires=['fastapi', 'uvicorn'],
    packages=['app'],
    entry_points={
        'console_scripts': [
            'pratica-1=app.app:main',
        ]
    }
)

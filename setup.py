from setuptools import setup

setup(
    name='pratica1',
    description='Pratica 1 de SD, 2021.2',
    author='Allana Campos',
    install_requires=['fastapi', 'uvicorn'],
    packages=['app'],
    entry_points={
        'console_scripts': [
            'pratica1-sd=app.app:main',
        ]
    }
)

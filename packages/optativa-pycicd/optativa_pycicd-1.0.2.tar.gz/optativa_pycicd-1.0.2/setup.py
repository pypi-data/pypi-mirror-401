from setuptools import setup, find_packages


setup(
    name="optativa_pycicd",
    version="1.0.2",
    author="Román Martínez",
    author_email="rgmf@riseup.net",
    description="Descripción de tu proyecto",
    packages=find_packages(),
    install_requires=[
        "pytest",
        "flake8",
    ],
)

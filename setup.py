from setuptools import setup, find_packages

setup(
    name="icid-backend",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "psycopg[binary]>=3.2",
        "python-dotenv>=1.0",
        "tabulate>=0.9",
    ],
)

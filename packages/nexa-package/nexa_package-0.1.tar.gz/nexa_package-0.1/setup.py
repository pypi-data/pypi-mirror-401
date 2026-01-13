from setuptools import setup, find_packages

setup(
    name="nexa_package",
    version="0.1",
    author="Harshit Verma",
    author_email="harshitvermami4i@gmail.com",
    description="A package for speech to text conversion using selenium",
    packages=find_packages(include=["nexa_stt", "nexa_stt.*"]),
    include_package_data=True,
    install_requires=[
        "selenium",
        "webdriver-manager"
    ],
)

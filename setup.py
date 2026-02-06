from setuptools import setup, find_packages

setup(
    name="robot_sdk",
    version="0.1.0",
    description="Robotics for Good Robot SDK",
    author="Vlad Isuf",
    packages=find_packages(),
    install_requires=[
        "numpy",
    ],
)

from setuptools import setup, find_packages

setup(
    packages=find_packages(include=["dearning", "dearning.*"]),
    package_data={
        "dearning": ["*.txt", "*.json", "*.md", "*.pdf"],
        "Memory": ["*.json", "*.txt", "*.dat"]
    },
    include_package_data=True,
)
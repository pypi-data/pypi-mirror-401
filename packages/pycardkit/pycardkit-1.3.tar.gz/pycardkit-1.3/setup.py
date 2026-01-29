from setuptools import setup, find_packages

with open("README.md", "r") as f:
    desc = f.read()

setup(
    name="pycardkit",
    version="1.3",
    packages=find_packages(),
    long_description=desc,
    long_description_content_type="text/markdown"
)
from setuptools import setup, find_packages

setup(
    name="watchup-py",  # pip install watchup-py
    version="0.1.0",
    description="Python SDK / error boundary for Watchup.site",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Raphael Tomiwa",
    author_email="devtomiwa9@gmail.com",
    url="https://github.com/tomurashigaraki22/watchup-py",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "Flask>=2.0.0"
    ],
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
)

from setuptools import setup

setup(
    name="indotime",
    version="0.1.2",
    author="Gemini",
    author_email="gemini@google.com",
    description="A simple Python library for Indonesian time (WIB).",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gemini/indotime", # Replace with actual URL if you have one
    packages=['indotime'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
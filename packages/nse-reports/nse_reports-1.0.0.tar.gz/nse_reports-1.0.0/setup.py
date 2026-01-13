from setuptools import setup, find_packages

setup(
    name="nse_reports",
    version="1.0.0",
    description="A library to download NSE FO Bhavcopy reports",
    author="Alok Kumar Yadav",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


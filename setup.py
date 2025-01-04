from setuptools import setup, find_packages

setup(
    name="flip-clock-desktop",
    version="1.0.0",
    author="ckxkx",
    author_email="colors0874@gmail.com",
    description="A modern desktop flip clock with timezone and calendar support",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ckxkx/flip-clock",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyQt6>=6.6.1",
        "pytz>=2023.3",
    ],
    entry_points={
        "console_scripts": [
            "flip-clock=flip_clock:main",
        ],
    },
) 
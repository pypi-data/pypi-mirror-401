from setuptools import setup, find_packages

setup(
    name="ace-concurrency",
    version="0.1.0",
    description="Adaptive Concurrency Engine - Automatic concurrency management for Python applications",
    author="ACE Team",
    packages=find_packages(),
    install_requires=[
        "psutil>=5.9.0",
        "kafka-python>=2.0.2",
    ],
    extras_require={
        "examples": [
            "aiohttp>=3.8.0",
            "requests>=2.28.0",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)

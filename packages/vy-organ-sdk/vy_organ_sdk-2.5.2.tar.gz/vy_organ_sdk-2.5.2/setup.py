from setuptools import setup, find_packages
from pathlib import Path

readme_path = Path(__file__).parent / "README.md"
long_description = ""
if readme_path.exists():
    with open(readme_path, encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="vy-organ-sdk",
    version="2.5.2",
    author="VY-AGI",
    description="Python SDK for building VY organs with Protocol v2 support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "eclipse-zenoh>=1.7.2",
        "msgpack>=1.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="vy organs protocol zenoh microservices",
    project_urls={
        "Source": "https://github.com/vinver-labs/vy-organ-sdk",
        "Documentation": "https://github.com/vinver-labs/vy-organ-sdk#readme",
    },
)

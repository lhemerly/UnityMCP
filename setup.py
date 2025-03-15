from setuptools import setup, find_packages

setup(
    name="unity-mcp",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    author="Luiz Hemerly",
    author_email="lechemerly@gmail.com",
    description="Python client for Unity MCP server",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lhemerly/mcp-client",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)

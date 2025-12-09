"""Setup script for LawMode."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lawmode",
    version="0.1.0",
    author="LawMode.ai",
    author_email="team@lawmode.ai",
    description="Always-on AI lawyer for developers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lawmode/lawmode",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "langgraph>=0.2.0",
        "langchain>=0.3.0",
        "langchain-core>=0.3.0",
        "langchain-openai>=0.2.0",
        "langchain-community>=0.3.0",
        "pydantic>=2.0.0",
        "pyyaml>=6.0",
        "requests>=2.31.0",
        "gitpython>=3.1.40",
        "click>=8.1.7",
        "rich>=13.7.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "lawmode=lawmode.cli:main",
        ],
    },
)


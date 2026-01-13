"""
Setup script for AI Terminal package.
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="flawhunt",
    version="1.0.8",
    author="GAMKERS",
    author_email="gamkers@example.com",
    description="Natural language to shell with explanations & confirmations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gamkers/GAMKERS_CLI.git",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.8",
    install_requires=[
        "google-generativeai>=0.3.0",
        "langchain>=0.3.0",
        "langchain-google-genai>=2.0.0",
        "langchain-groq>=0.1.0",
        "prompt-toolkit>=3.0.0",
        "typer>=0.9.0",
        "rich>=13.0.0",
        "faiss-cpu>=1.7.0",
        "sentence-transformers>=2.2.0",
        "requests>=2.28.0",
        "beautifulsoup4>=4.11.0",
        "pycryptodome>=3.15.0",
        "cryptography>=3.4.0",
        "supabase>=2.0.0",
        "watchdog>=4.0.0",
        "langgraph>=0.0.10",
    ],
    entry_points={
        "console_scripts": [
            "flawhunt=ai_terminal.cli:main",
        ],
    },
)
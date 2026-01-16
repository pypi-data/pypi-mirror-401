from setuptools import setup, find_packages

# Read README.md for PyPI long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="councillm",
    version="1.0",
    author="Raktim Kalita",
    author_email="raktmxx@gmail.com",
    description="A local LLM Council framework using Ollama with multi-model deliberation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rktim/councillm",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[
        "ollama>=0.3.0",
        "duckduckgo-search>=4.1.0",
        "httpx>=0.25.0",
    ],
    entry_points={
        "console_scripts": [
            "councillm=councillm.cli:run",
        ],
    },
)

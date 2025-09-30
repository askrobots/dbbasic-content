from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dbbasic-content",
    version="0.1.0",
    author="Dan Quellhorst",
    description="Unix-foundation content management for web apps - WordPress escape toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/askrobots/dbbasic-content",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "dbbasic-tsv>=0.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
        ],
        "wordpress": [
            "pymysql>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "dbcontent=dbbasic_content.cli:main",
        ],
    },
)

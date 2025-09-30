from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dbbasic-content",
    version="0.1.3",
    author="Dan Quellhorst",
    author_email="dan@quellhorst.com",
    description="Unix-foundation content management for web apps - WordPress escape toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/askrobots/dbbasic-content",
    project_urls={
        "Bug Tracker": "https://github.com/askrobots/dbbasic-content/issues",
        "Documentation": "https://github.com/askrobots/dbbasic-content#readme",
        "Source Code": "https://github.com/askrobots/dbbasic-content",
    },
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
    ],
    keywords="cms content-management wordpress unix blocks json",
    python_requires=">=3.8",
    install_requires=[
        "dbbasic-tsv>=1.0.0",
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

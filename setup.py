from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sipnav-client",
    use_scm_version={
        "write_to": "src/sipnav/_version.py",
        "write_to_template": '__version__ = "{version}"\n',
        "version_scheme": "python-simplified-semver",
        "local_scheme": "no-local-version",
    },
    author="Sam Ware",
    author_email="samuel@waretech.services",
    maintainer="Sam Ware",
    maintainer_email="samuel@waretech.services",
    description="Python client library for SIPNAV REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/werebear73/sipnav-client",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    setup_requires=[
        "setuptools>=45",
        "setuptools_scm[toml]>=6.2",
    ],
    install_requires=[
        "requests>=2.28.0",
        "urllib3>=1.26.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.991",
            "types-requests>=2.28.0",
        ],
        "docs": [
            "mkdocs>=1.5.0",
            "mkdocs-material>=9.4.0",
            "mkdocstrings[python]>=0.24.0",
            "pymdown-extensions>=10.5.0",
            "mkdocs-awesome-pages-plugin>=2.9.0",
        ],
    },
)

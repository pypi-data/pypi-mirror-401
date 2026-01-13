from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="polygon-identity",
    version="0.1.0",
    author="Usama Tahir",
    author_email="usama.tahir.choudhary@gmail.com",
    description="Polygon-based identity management system for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Usamatahir23/polygon_identity_py",
    project_urls={
        "Bug Reports": "https://github.com/Usamatahir23/polygon_identity_py/issues",
        "Source": "https://github.com/Usamatahir23/polygon_identity_py",
        "Documentation": "https://github.com/Usamatahir23/polygon_identity_py#readme",
    },
    keywords="polygon blockchain identity ethereum web3 social-recovery zk-proof decentralized",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "web3>=6.0.0",
        "cryptography>=41.0.0",
        "PyJWT>=2.8.0",
        "requests>=2.31.0",
        "PyNaCl>=1.5.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "django": ["django>=4.0.0"],
        "fastapi": ["fastapi>=0.100.0", "uvicorn>=0.23.0"],
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
    },
)


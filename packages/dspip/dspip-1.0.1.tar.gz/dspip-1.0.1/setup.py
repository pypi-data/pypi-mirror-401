from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dspip",
    version="0.9.0b1",  # Beta version notation
    author="Andy Boell",
    author_email="contact@midwestcyber.com",  # Update with your email
    description="Digital Signing of Physical Items Protocol (DSPIP) implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/midwestcyber/dspip-python",
    project_urls={
        "Bug Tracker": "https://github.com/midwestcyber/dspip-python/issues",
        "Documentation": "https://dspip.io/docs",
        "Source Code": "https://github.com/midwestcyber/dspip-python",
        "Internet-Draft": "https://datatracker.ietf.org/doc/draft-midwestcyber-dspip/",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords="dspip, cryptography, shipping, logistics, qr-code, authentication, digital-signature",
    python_requires=">=3.8",
    install_requires=[
        "cryptography>=41.0.0",
        "qrcode>=7.4.0",
        "Pillow>=10.0.0",  # Required by qrcode
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
)
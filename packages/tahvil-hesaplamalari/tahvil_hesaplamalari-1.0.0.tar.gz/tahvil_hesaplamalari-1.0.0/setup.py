"""
Setup dosyası - PyPI'ye yayınlama için hazırlanmıştır
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tahvil-hesaplamalari",
    version="1.0.0",
    author="Aktüeryal Hesaplamalar Öğrencisi",
    description="Tahvil değerleme ve risk analizi için Python kütüphanesi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ASLI06121/tahvil-hesaplamalari",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[],
)


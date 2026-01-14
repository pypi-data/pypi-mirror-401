from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    README = f.read()

setup(
    name="Vho",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "torch",
        "diffusers",
        "transformers",
        "accelerate",
        "safetensors",
        "deep-translator"
        ],
    description="Vho: İşlevsel ve kolaylaştırılmış görsel oluşturma kütüphanesi",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Bedirhan",
    author_email="bedirhan.oytpass@gmail.com",
    license="MIT",
    keywords=["görsel", "kolay", "basitleştirilmiş"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ],
)

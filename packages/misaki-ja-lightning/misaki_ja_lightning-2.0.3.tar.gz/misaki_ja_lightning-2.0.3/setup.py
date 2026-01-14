from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="misaki-ja-lightning",
    version="2.0.3",
    author="Your Name",
    author_email="your.email@example.com",
    description="Lightweight Japanese text-to-IPA phoneme converter with cutlet support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/misaki-ja-lightning",
    packages=find_packages(),
    package_data={
        "misaki_ja_lightning": ["data/*.txt"],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fugashi==1.4.0",
        "mecab-python3",
        "jaconv==0.4.0",
        "mojimoji==0.0.13",
        "pyopenjtalk-somniumism>=0.1.dev0",
    ],
    extras_require={
        "unidic": [
            "unidic-lite",
        ],
    },
    keywords="japanese nlp tts phoneme ipa g2p text-to-speech cutlet fugashi",
)

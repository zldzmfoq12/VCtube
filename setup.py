import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="audio, caption crawler and processor", # Replace with your own username
    version="0.0.1",
    author="Seugnhun Jeong",
    author_email="zldzmfoq12@naver.com",
    description="A pakage for crawling and processing audio, caption from Youtube",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zldzmfoq12/aud_crawler",
    download_url="https://github.com/zldzmfoq12/aud_crawler/archive/0.0.tar.gz",
    keywords=['aud_crawler'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
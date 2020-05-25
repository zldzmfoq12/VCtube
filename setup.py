import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="vctube", # Replace with your own username
    version="1.2",
    author="Seugnhun Jeong",
    author_email="zldzmfoq12@naver.com",
    description="A pakage for crawling and processing audio, caption from Youtube",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zldzmfoq12/aud-crawler",
    download_url="https://github.com/zldzmfoq12/aud-crawler/archive/1.2.tar.gz",
    keywords=['aud_crawler'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
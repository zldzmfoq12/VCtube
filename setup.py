import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="vctube",
    version="1.3",
    author="Seugnhun Jeong",
    author_email="zldzmfoq12@naver.com",
    description="A package for crawling and processing audio, caption from Youtube",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zldzmfoq12/aud-crawler",
    keywords=['aud_crawler'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pandas", "pydub", "tqdm", "youtube_dl", "youtube_transcript_api"],
    python_requires='==3.6',
)

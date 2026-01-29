from setuptools import setup, find_packages

setup(
    name="nano-banana-pro-prompt",
    version="1768559.175.715",
    description="High-quality integration for https://supermaker.ai/blog/nano-banana-pro-prompt-use-cases-ready-to-copy-paste/",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="SuperMaker",
    url="https://supermaker.ai/blog/nano-banana-pro-prompt-use-cases-ready-to-copy-paste/",
    packages=find_packages(),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)

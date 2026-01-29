from setuptools import setup, find_packages

setup(
    name="grok-image-generator",
    version="1768531.555.964",
    description="High-quality integration for https://supermaker.ai/blog/-grok-image-generator-model-on-supermaker-ai-twitterready-images-made-simple/",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="SuperMaker",
    url="https://supermaker.ai/blog/-grok-image-generator-model-on-supermaker-ai-twitterready-images-made-simple/",
    packages=find_packages(),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)

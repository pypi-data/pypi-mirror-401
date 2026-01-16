from setuptools import setup, find_packages

setup(
    name="kling-motio-control",
    version="1768444.568.616",
    description="High-quality integration for https://supermaker.ai/blog/what-is-kling-motion-control-ai-how-to-use-motion-control-ai-free-online/",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="SuperMaker",
    url="https://supermaker.ai/blog/what-is-kling-motion-control-ai-how-to-use-motion-control-ai-free-online/",
    packages=find_packages(),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)

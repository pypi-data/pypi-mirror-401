from setuptools import setup, find_packages

setup(
    name="3d-camera-control",
    version="1768471.24.681",
    description="High-quality integration for https://supermaker.ai/blog/qwen-image-multiple-angles-3d-camera-alibabas-breakthrough-in-ai-camera-control/",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="SuperMaker",
    url="https://supermaker.ai/blog/qwen-image-multiple-angles-3d-camera-alibabas-breakthrough-in-ai-camera-control/",
    packages=find_packages(),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)

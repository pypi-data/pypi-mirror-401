from setuptools import setup, find_packages

setup(
    name="ai-twerk-generator",
    version="1768544.455.937",
    description="High-quality integration for https://supermaker.ai/blog/how-to-make-ai-twerk-video-with-supermaker-ai-free-online/",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="SuperMaker",
    url="https://supermaker.ai/blog/how-to-make-ai-twerk-video-with-supermaker-ai-free-online/",
    packages=find_packages(),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)

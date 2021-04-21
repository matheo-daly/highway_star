import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="highway_star",
    version="0.0.2",
    author="Mathéo Daly",
    author_email="matheodaly.md@gmail.com",
    description="A library to scrap content from wikipedia categories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matheo-daly/highway_star",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

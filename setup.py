import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = []
with open('requirements.txt', 'r') as fh:
    for line in fh:
        requirements.append(line.strip())

setuptools.setup(
    name="highway_star",
    version="0.0.6.1",
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
    install_requires=requirements,
    python_requires=">=3.6",
)

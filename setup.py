import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bootstrap_interval",
    version="0.0.4",
    author="Alexander Neshitov",
    author_email="alexander.neshitov@gmail.com",
    description="A small package for bootstrap confidence intervals",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/neshitov/bootstrap",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

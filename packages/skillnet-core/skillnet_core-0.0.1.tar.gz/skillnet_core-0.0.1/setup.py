from setuptools import setup, find_packages

setup(
    name="skillnet-core",
    version="0.0.1",
    author="liangyuan",
    author_email="liangyuannnnn@gmail.com",
    description="The skillnet-core library.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="log2csv",
    version="0.0.1",
    author="Rui Zhou",
    author_email="quicksort@outlook.com",
    description="A tool to parse log files into csv, using a grok-like pattern",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/quick-sort/log2csv",
    include_package_data=True,
    install_requires=['regex'],
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    entry_points= {
        'console_scripts': ['log2csv = log2csv:main']
        }
)

import setuptools

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="QVAR",
    version="1.1.0",
    author="Alessandro Poggiali",
    packages=["QVAR"],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="musx",
    version="2.0.5",
    author="Rick Taube",
    author_email="taube@illinois.edu",
    description="An algorithmic music composition package based in part on the author's Common Music and Grace systems.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/musx-admin/musx",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)

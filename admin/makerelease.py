"""
This script prepares a release of musx without executing the build or upload
steps. To run the script first make sure your musx virtual environment is 
running and that your working directory is the top-level of the musx repo. Then
execute this makerelease script and pass it the software's new version number:

    (venv) $ cd /path/to/musx
    (venv) $ python3 scripts/makerelease.py 1.2.3

To upload the release to the pip repository after executing the script do:

    (venv) $ cd /tmp/musx-release
    (venv) $ python3 -m build
    (venv) $ python3 -m twine upload dist/*
"""

# instructions:
# https://packaging.python.org/tutorials/packaging-projects/
# https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56

import sys, os, shutil

top_dir = os.getcwd()
src_dir = f"{top_dir}/musx"
rel_dir = "/tmp/musx-release"

# the working directory must be the top-level musx directory.
if not (top_dir.endswith("/musx") and os.path.isdir(src_dir)):
    sys.exit("Call this script from the top-level musx directory.")

# script help
helpstr = '''
    Creates a release of musx without executing the build or upload steps.
    Takes one required argument, the release tag, a string of three ints
    separated by periods.

    Example: $ python3 admin/makerelease.py 1.2.3
'''


# The contents of the setup.py file. The version=N.N.N line
# gets replaced with the actual version release number.
setup_py = """import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="musx",
    version="N.N.N",
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
"""

# The contents of the toml file needed by build.
pyproject_toml = """[build-system]
requires = [
    "setuptools>=42",
    "wheel"
]
build-backend = "setuptools.build_meta"
"""


def exit(text):
    if text: print(text)
    sys.exit(0)


def replace_in_string(string, target, repl):
    return "".join(line.replace(target, repl) + "\n" for line in string.splitlines())


if __name__ == '__main__':
    # first check argv for a valid version number string, e.g. 1.2.3
    argv = sys.argv[1:]
    if not argv or argv in ["-h", "--help", "help"]:
        exit(helpstr)
    if len(argv) != 1:
        exit(f"{argv} is not a release version string in the format '1.2.3'")
    argv = argv[0] # ["1.2.3"] => "1.2.3"
    nums = argv.split(".") # "1.2.3" => ["1","2","3"]
    if len(nums) != 3:
        exit(f"{argv} is not a release version string in the format '1.2.3'")
    if not "".join(nums).isdigit():  # allow only digits
        exit(f"{argv} is not a release version string in the format '1.2.3'")        
    #-------------------------------------------------------------------------
    # create the new release materials in tmp/musx-release
    if os.path.isdir(rel_dir):
        shutil.rmtree(rel_dir)
    # copy musx/ source tree to /tmp/musx-release/musx/
    shutil.copytree(src_dir, f"{rel_dir}/musx", ignore=shutil.ignore_patterns(".*", "__pycache__"))
    # copy the readmes from source directory into the release directory
    for f in ["LICENSE.md", "INSTALL.md", "README.md"]:
        shutil.copy(f"{top_dir}/{f}", rel_dir)
    # create the pyproject.toml file
    with open(f"{rel_dir}/pyproject.toml", 'w') as file:
        file.write(pyproject_toml)
    # create the setup.py file that uses the current release number
    text = replace_in_string(setup_py, "N.N.N", argv)
    with open(f"{rel_dir}/setup.py", 'w') as f:
        f.write(text)
    # open /tmp/musx-release/musx/__init__.py and replace the version="N.N.N" with the 
    with open(f"{rel_dir}/musx/__init__.py",'r') as file:
        text = file.read()
        text = text.replace("N.N.N", argv)
    with open(f"{rel_dir}/musx/__init__.py",'w') as file:
        file.write(text)
    # printout the next steps
    print(f"""
To upload to pip do:
    $ cd {rel_dir}
    $ python3 -m build
    $ python3 -m twine upload dist/*
""")

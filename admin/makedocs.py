"""
This script uses pdoc3 to generate musx documentation. To run the script do:
    $ cd /path/to/musx
    $ python admin/makedocs.py
"""

import sys, os, shutil

# the working directory must be the top-level musx directory.
if not (os.getcwd().endswith("/musx") and os.path.isdir("musx") and os.path.isdir("docs")):
    sys.exit("Call this script from the top-level musx directory.")

src_dir = "musx"
doc_dir = "docs"
tmp_src = "/tmp/musx"
tmp_doc = "/tmp/docs"
tmp_old = "/tmp/docs_old"

def exclude():
    """Returns the list of files to ignore."""
    patterns = set([".*", "*.md", "__pycache__", "musicxml.py"])
    return shutil.ignore_patterns(*patterns) 

# The documentation for the stub musicxml.py file.
contents = """
'A module that implements the complete MusicXml schema. This file was created using generateDS and is too large to include in the documentation.'

def parse(inFileName, silence=False, print_warnings=True):
    pass

"""

def make_docs():
    for d in [tmp_src, tmp_doc, tmp_old]:
        if os.path.isdir(d):
            shutil.rmtree(d)
    shutil.copytree(src_dir, tmp_src, ignore=shutil.ignore_patterns(".*", "*.md", "__pycache__", "musicxml.py"))
    with open(tmp_src + '/mxml/musicxml.py', 'w') as f:
        f.write(contents)
    os.system(f"pdoc --html -o {tmp_doc} {tmp_src}")
    # move the current musx/docs directory to /tmp/docs_old
    shutil.move(doc_dir, tmp_old)
    # move the root of the new doc tree back as musx/docs: /tmp/docs/musx -> musx/docs
    shutil.move(f"{tmp_doc}/musx", doc_dir)
    # # copy the .yml file back to musx/docs
    # shutil.copy(f"{tmp_old}/_config.yml", doc_dir)

make_docs()

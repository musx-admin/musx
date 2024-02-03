# Change Log

## musx 3.1.0

### Added

* New musx.audio module adds support for working with Todd Ingall's [pysndlib](https://pypi.org/project/pysndlib/) and musx together. This module is not automatically loaded into the musx namespace, use an explict `import musx.audio` to access it.
* New jupyter notebook tutorial 'audio.ipynb' introduces working with pysndlib and musx. The notebook starts with basic instrument design and moves up thru more advanced concepts.
* New jupyter notebook tutorial 'cython.ipynb' explains how to optimize "pure Python" pysndlib instruments using Python's Cython compiler.
* New jupyter notebook demo 'birds.ipynb' features Bill Schottstaedt's bird calls. For each bird you can access its python code, play the bird at reduced speeds to better hear the transients, and visit a Cornell website page to learn about the critter.
* New function `exp_env()` returns an exponential envelope with a specified number of segments.
* New function `rescale_env()` rescales an x,y envelope list in various ways.
* New function `segment_env()` returns an envelope with specified durations for attack and decay segments.
* New function `interp()` interpolates values from an x,y envelope or variadic sequence of x,y pairs.
* New function `shuffle()` returns a randomly reordered vaersion of a list, tuple or variadic sequence of values.

### Changed

* Incompatible change: note expansions in the pitch(), keynum() and hertz() functions have 
switched from repeating commas to expansion factors, e.g.:   'C4*3 D E*2' -> C4 C4 C4 D4 E4 E4
* The musx.env module is no longer auto-loaded. To get it add an explicit 'import musx.env' statement.
* Updated all .md files.
* Added missing function _notes_to_midi() in rtmidi.ipynb.

## musx 3.0.0

### Added

* musx demo scripts have been converted from .py files into Jupiter Notebooks (.ipynb) to better facilitate interactive exploration. 
* A new tutorials directory contains a number of Jupyter Notebooks adapted from my CS+Music classes at UIUC. The topics are wide ranging, from basic data representation to spectral composition and 'real time' extensions.
* Support for loading data from MusicXML files into data structures that can be easily mapped for analysis.  The MusicXML support is located in the musx.mxml module and contains notation  classes (enumerations), parts and scores.
* A new pattern.py module provides a base Pattern class, support for subpatterns (patterns inside patterns), a new Range pattern, a new Graph pattern, "dynamic values" (values that can be constants or lambda expressions of zero arguments), and dynamic weighting in the Choose pattern. The new patterns.py module replaces the older gens.py module, which can be still loaded using the explicit command 'import musx.gens'.
* New module frac.py adds methods to Python's Fraction class for working with tuples and other mensural quantities.

### Changed
* INSTALL.md provides an easy, step by step process for installing musx and its demo and tutorial directors.
* The Interval class is now immutable, as are Pitches and PCSets.
* Moved drunk() to the ran.py module.
* Fixed bug in Spectrum.keynums(): hertz values outside keynum range 0-127 are ignored.
* Added str() and repr() methods to the event class, simplified str() method for Notes.

### Removed
* The original pattern generators (gens.py) are no longer auto-loaded but remain available for user to import.

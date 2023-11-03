# Change Log

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


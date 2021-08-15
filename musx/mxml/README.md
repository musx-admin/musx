MusicXml Schema:
	https://github.com/w3c/musicxml/releases/download/v4.0/musicxml-4.0.zip

MusicXml Documentation:
	https://www.musicxml.com/for-developers/musicxml-xsd/

GenerateDS (installs lxml package):
	$ pip install generateDS

Useful lxml etree tutorial:
	https://lxml.de/tutorial.html

Converting MusicXlm.xsd to Python code using generateDS:
	$ generateDS -o musicxml.py --root-element "score_partwise" schema/musicxml.xsd
OR:
	$ python3 generateDS.py -o musicxml.py --root-element "score_partwise" schema/musicxml.xsd 

Importing a MusicXmlDocument using musicxml.py:
	>>> import musicxml
	>>> root = musicxml.parse("/Users/taube/Classes/MUS105/Scores/001-2s.xml")

========================================================

import musx.mxml.notation as notation
notation.load("scores/HelloWorld.musicxml")


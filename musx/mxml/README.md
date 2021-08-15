##### MusicXml Schema:

​	https://github.com/w3c/musicxml/releases/download/v4.0/musicxml-4.0.zip

##### MusicXml Documentation:

​	https://www.musicxml.com/for-developers/musicxml-xsd/

##### GenerateDS (installs lxml package):

​	`$ pip install generateDS`

##### Useful lxml etree tutorial:

​	https://lxml.de/tutorial.html

##### Converting MusicXlm.xsd to Python code using generateDS:

​	`$ generateDS -o musicxml.py --root-element "score_partwise" schema/musicxml.xsd`
OR:
​	`$ python3 generateDS.py -o musicxml.py --root-element "score_partwise" schema/musicxml.xsd` 

##### Lowlevel loading of  MusicXml using just musicxml.py:

```
$ cd musx/mxml
$ python3
>> import musicxml
>> root = musicxml.parse("scores/HelloWorld.musicxml")
```

##### Loading a MusicXml notation:

```
$ cd musx
$ python3
>> import musx.mxml.notation as notation
>> score = notation.load("scores/HelloWorld.musicxml")
```


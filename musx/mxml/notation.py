from musx.tools import parse_string_sequence
import re
from lxml import etree
from enum import Enum, auto
from . import musicxml
from .barline import Barline
from .clef import Clef
from .key import Key
from .measure import Measure
from .mode import Mode
from .meter import Meter
from .part import Part
from ..pitch import Pitch
from ..note import Note

"""
# creating the MusicXml python file:
(venv) $ generateDS.py -o musicxml.py --root-element "score_partwise" schema/musicxml.xsd 

# Working directly with generateDS code:
import musx.mxml.musicxml as musicxml
musicxml.parse("Scores/001-2s.xml") 

# Working with notation classes
import musx.mxml.mxmlfile
musx.mxml.mxmlfile.read("scores/HelloWorld.musicxml")
"""

class Notation():
    def __init__(self, metadata={}, parts=[]):
        self.metadata = metadata
        self.parts = []
        for p in parts:
            self.add_part(p)

    def __iter__(self):     
        return iter(self.parts)
    
    def __repr__(self):
        title = self.metadata.get('work-title', None)
        if title is None:
            title = self.metadata.get('movement-title', '(untitled)')
        return f'<Notation: "{title}" {hex(id(self))}>'

    __str__ = __repr__

    def add_part(self, part):
        part.score = self  # back link from part to its score
        self.parts.append(part)
    
    def print(self):
        pad = "  "
        print(pad*0, self, sep=None)
        for p in self:
            print(pad*1, p, sep=None)
            for m in p:
                print(pad*2, m)
                for e in m:
                    print(pad*3, e)

    def add_element(self, element):
        #element.measure = self  # back link from element to its measure
        self.elements.append(element)

##############################################################################

"""
import musx.mxml.mxmlfile
x=musx.mxml.mxmlfile.read("scores/HelloWorld.musicxml")
x.parts[0].measures[0].elements
"""

def parse_barline(elem, data):
    """
    tag=barline, attrs={'location': 'right'}, text='', children=2
    tag=bar-style, attrs={}, text='light-heavy', children=0
    tag=repeat, attrs={'direction': 'backward'}, text='', children=0
    """
    text = None
    repeat = None
    barline = None
    location = elem.get('location', 'right') # right, left or middle
    for s in iter(elem): # alterates: elem.getchildren() OR list(elem)
        if s.tag == 'bar-style':
            text = s.text
        elif s.tag == 'repeat':
            repeat = s.get('direction')
    #print("text=", text, ", repeat=", repeat)
    if text == 'regular': barline = Barline.Regular(location)
    elif text == "light-light": barline = Barline.InteriorDouble(location)
    elif text == "light-heavy":
        if repeat == 'backward': barline = Barline.BackwardRepeat(location)
        else: barline = Barline.FinalDouble(location)
    elif text == "dotted": barline = Barline.Dotted(location)
    elif text == "dashed": barline = Barline.Dashed(location)
    elif text == "heavy": barline = Barline.Heavy(location)
    elif text == "heavy-light":
        if repeat == 'forward': barline = Barline.ForwardRepeat(location)
        else: barline = Barline.HeavyLight(location)
    elif text == "heavy-heavy": barline = Barline.HeavyHeavy(location)
    elif text == "tick": barline = Barline.Tick(location)
    elif text == "short": barline = Barline.Short(location)
    elif text == 'none': barline = Barline.Regular(location) #Barline.INVISIBLE
    elif text == None: barline = Barline.Regular(location) #Barline.INVISIBLE
    assert barline, f"MusicXml: Invalid barline value: '{text}'."
    data['measure'].barlines.append(barline)

def parse_part(elem, data):
    # create a new part and add it to the score
    part = Part()
    part.id = elem.get('id')
    data['part'] = part
    data['score'].add_part(part)
    data['divisions'] = 1
    data['measure'] = None

def parse_measure(elem, data):
    # create a new measure and add it to the part
    measure = Measure(elem.get('number'))
    if elem.get('implict') == 'yes':
        measure.partial = True
    data['measure'] = measure
    data['part'].add_measure(measure)

def parse_attributes(elem, data):
    measure = data['measure']
    isempty = measure.num_voices() == 0

    for s in elem.iter(): 
        if s.tag == 'divisions':
            divs = s.text
            data['divisions'] = int(divs)
        elif s.tag == 'clef':
            sign = s.findtext('sign')
            line = s.findtext('line')
            staff = int(s.get('number', "1"))
            clef = None
            if sign == 'G':
                clef = {'1': Clef.FrenchViolin(staff), '2': Clef.Treble(staff)}[line]
            elif sign == 'F':
                clef = {'3': Clef.BaritoneF(staff), '4': Clef.Bass(staff), '5': Clef.SubBass(staff)}[line]
            elif sign == 'C':
                clef = {'1': Clef.Soprano(staff), '2': Clef.MezzoSoprano(staff),
                        '3': Clef.Alto(staff), '4': Clef.Tenor(staff),'5': Clef.Baritone(staff)}[line]
            elif sign == 'percussion':
                clef = Clef.Percussion(staff)
            assert clef, f"No clef for sign '{sign}' and line '{line}'"
            measure.clefs.append(clef)
        elif s.tag == 'time':
            num = s.findtext('beats')
            den = s.findtext('beat-type')
            staff = int(s.get("number", "0")) # 0=all staffs
            meter = Meter(int(num), int(den), staff)
            measure.meters.append(meter)
        elif s.tag == 'key':
            fifths = s.findtext('fifths')
            text = s.findtext('mode', "major")
            staff = int(s.get('number', "0")) # 0=all staffs
            mode = {'major': Mode.MAJOR, 'minor': Mode.MINOR, 'dorian': Mode.DORIAN, 'phrygian': Mode.PHRYGIAN, 
            'lydian': Mode.LYDIAN, 'mixolydian': Mode.MIXOLYDIAN, 'aeolian': Mode.AEOLIAN, 'ionian': Mode.IONIAN, 
            'locrian': Mode.LOCRIAN}[text]
            key = Key(int(fifths), mode, staff)
            measure.keys.append(key)

def parse_note(elem, data):
    first = elem[0].tag
    if first in ['grace', 'cue']:
        return
    if first == 'chord':
        # elem is a chord tone
        pass
    else:
        # elem is a non-chord tone
        pass
    for e in elem.iter(): 
        print("***", element_info(e))

        if e.tag == 'pitch':
            step = e.findtext('step')
            alter = e.findtext('alter')
            if alter:
                alter = {-2: 'bb', -1: 'b', 0: '', 1: '#', 2: '##'}.get(int(alter), '')
            octave = e.findtext('octave')
            pitch = Pitch(step + alter + octave)
            print("***", pitch)
        elif e.tag == 'rest':
            pass
        elif e.tag == 'chord':
            pass

def parse_rest(elem, data):
    pass


def element_info(e):
    return f"tag={e.tag}, attrs={e.attrib}, text='{e.text.strip() if e.text else ''}', children={len(e)}"


element_parsers = {
    'part': parse_part, 
    'measure': parse_measure, 
    'attributes': parse_attributes, 
    'barline': parse_barline,
    'note': parse_note,
    'rest': parse_rest
    }
"""
To parse an xml element add its tag as a key and its parser function as
its value to the dictionary. The parsing function accepts two arguments:
(element, datadict), where element is the lxml Element to parse and datadict
is a dictionary that includes the running status of the parser, e.g. the
score, current part, current measure, and the arser functions added or update
whatever they want in the dictionary. Elements whose tags are not in 
dictionary will not parsed.  If a parser performs subelement parsing, dont 
add those subelement tags to element_parser else they will be parsed twice...
"""
    
def load(path):
    document = musicxml.parse(path, silence=True) 
    assert isinstance(document, musicxml.score_partwise), f"not a partwise musicxml file: '{path}'."
    root = getattr(document, 'gds_elementtree_node_') # root element of document
    assert isinstance(root, etree._Element) and root.tag == 'score-partwise', f"not a score-partwise element: {root}."
    parsed = {"score": Notation(), "part": None, "measure": None, "divisons": 1,
    }
    # a depth-first traversal of all elements in the document.
    for x in root.iter():
        #print(f"tag={x.tag}, attrs={x.attrib}, text='{x.text.strip() if x.text else ''}', children={len(x)}")
        func = element_parsers.get(x.tag)
        if func:
            #print(element_info(x))
            func(x, parsed)

    return parsed['score']



if __name__ == "__main__":
    pass

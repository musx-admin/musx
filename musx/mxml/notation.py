"""
A module for loading and saving MusicXml scores. As of Aug '21 loading is fully
implemented .
"""

# creating the MusicXml python file:
# (venv) $ generateDS.py -o musicxml.py --root-element "score_partwise" schema/musicxml.xsd 
#
# Working with low-level lxml Element trees (musicxml.py):
# $ python3
# >>> import musx.mxml.musicxml as musicxml
# >>> musicxml.parse("Scores/001-2s.xml") 
#
# Working with high-level Notation objects:
# $ python3
# >>> import musx.mxml.notation as notation
# >>> score = notation.load("scores/HelloWorld.musicxml")
# >>> score.print()
#
# >>> from musx.note import Note; from fractions import Fraction; from musx.pitch import Pitch
# >>> n=Note(time=Fraction(0,1), duration=Fraction(1,4), pitch=Pitch("C4"))
# >>> n.add_child(Note(time=Fraction(0,1), duration=Fraction(1,4), pitch=Pitch("Fs5")))
# >>> n.add_child(Note(time=Fraction(0,1), duration=Fraction(1,4), pitch=Pitch("E1")))

import re, os
from lxml import etree
from enum import Enum, auto
from fractions import Fraction
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

# A template dictionary defining the 'running status' of MusicXml parsing. The
# load() method copies the template for each score it parses and passes it to
# the parsing routines so they can access and store relevant data:
#   score: The Notation being created
#   part: The current Part. This value resets for every new part.
#   measure: The current measure. This value resets for every new measure and every part.
#   divisions: The current division. This value resets for every new division and every part
#   note: The current note. This value changes for every new note, measure, and part.
#   meter: The most recent meter encountered in the score.
#   key: The most recent key encountered in the score.
#   onset: The Fraction onset time for the next note. This value is reset to 0 for each
#          measure, (or to measureDur - noteDur for partial measures) and incremented
#          by the duration of notes, forwards and backups.
_DATA = {
        "score": None, "part": None, "measure": None, "divisions": None,
        "note": None, "meter:": None, "key": None, "onset": None
    }


class Notation():
    """
    A class representing a MusicXml score. A Notation contains Part objects and
    metadata. 

    Parameters
    ----------
    metadata : dict
        A dictionary of metadata about the MusicXml score, e.g. title,
        copyright, etc.
    parts : list
        A list of Parts parsed from the MusicXml file.

    Given a Notation you can iterate all its elements like this:

        for part in notation:
            for measure in part:
                for element in measure:
                    print(element)

    To access vertical note structures in the score's measures you can iterate the
    score's timepoints like this:

        for measure in notation.timepoints():
            for timepoint in measure:
                print(timepoint)
    """
    def __init__(self, metadata={}, parts=[]):
        self.metadata = metadata
        """A dictionary of MusicXml score metadata."""
        self.parts = []
        """A list containing the score's musical parts."""
        for p in parts:
            self.add_part(p)

    def __iter__(self):
        """
        Iterates the Part objects in the Notation.
        """     
        return iter(self.parts)
    
    def __repr__(self):
        title = self.metadata.get('work-title', None)
        if title is None:
            title = self.metadata.get('movement-title', '(untitled)')
        return f'<Notation: "{title}" {hex(id(self))}>'

    __str__ = __repr__

    def add_part(self, part):
        """
        Appends a Part to the Notation's part list.
        """
        part.score = self  # back link from part to its score
        self.parts.append(part)
    
    def print(self):
        """
        Recursively prints the contents of the Notation.
        """
        pad = "  "
        print(pad*0, self, sep=None)
        for p in self:
            print(pad*1, p, sep=None)
            for m in p:
                print(pad*2, m)
                for e in m:
                    print(pad*3, e)
    
    def timepoints(self, trace=False):
        """
        Returns a list of Timepoint objects grouped in measures. See: Timepoint.
        """
        # Flop the part measures so all measures with the same id are grouped
        # together, e.g.: [[1,2,3],[1,2,3]] => [[1,1],[2,2],[3,3]]
        groups = [measures for measures in zip(*[part.measures for part in self])]
        # iterate each group of measures
        timepoints = []
        for group in groups:
            # iterate each measure in the group combining their timepoints
            measurepoints = []
            for measure in group:
                for element in measure:
                    if isinstance(element, Note):
                        ident = f"{measure.part.id}.{measure.id}.{element.get_mxml('voice')}"
                        onset = element.time
                        try: 
                            have = next((x for x in measurepoints if x.onset == onset))
                            have.notemap[ident] = element
                        except StopIteration:
                            tp = Timepoint(onset)
                            tp.notemap[ident] = element
                            measurepoints.append(tp)
                
            # sort the measure timepoints by their onsets
            measurepoints.sort()
            if trace:
                for tp in measurepoints:
                    print(str(tp))
                    print('----------------------------------------------------------------')
            timepoints.append(measurepoints)
        return timepoints

 
class Timepoint():
    """
    A Timepoint is an analytical structure containing an onset beat in a
    measure and the vertical 'slice' of all the notes that begin at that beat
    irrespective of which part, staff or voice they belong to. The note 
    entries within each Timepoint are maintained in a dictionary whose keys
    are part.measure.voice identifiers and whose values are the notes that
    begin at the Timepoint's beat.
    
    Parameters
    ----------
    onset : Fraction
        The metric onset of the timepoint in the measure.
    """
    def __init__(self, onset):
        self.onset = onset
        """The ratio start time of the timepoint in its measure."""
        self.notemap = {}
        """The note map dictionary. Its keys are part.measure.voice identifiers
        and its values are `musx.note.Note` objects tagged as either notes, chords or rests."""

    def __lt__(self, other):
        """
        Returns true if self.beat is less than other, otherwise returns false.
        """
        return self.onset < other.onset

    def __str__(self):
        """
        Returns a string contains the class name, the self.index attribute,
        and a hexidecimal id.
        """
        #return f"<Timepoint {str(self.onset)} {len(self.notemap)}>"
        pstr = ", ".join([n._tagged_pitch_str() for n in self.notemap.values()])
        return f"<Timepoint: {str(self.onset)} ({pstr})>"

    __repr__ = __str__


##############################################################################


def _elementinfo(e):
    """
    Helper function prints Element info
    """
    return f"tag={e.tag}, attrs={e.attrib}, text='{e.text.strip() if e.text else ''}', children={len(e)}"


def _parse_barline(elem, DATA):
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
    #DATA['measure'].barlines.append(barline)
    DATA['measure'].add_element(barline)


def _parse_part(elem, DATA):
    # create a new part and add it to the score
    part = Part(elem.get('id'))
    DATA['part'] = part
    DATA['score'].add_part(part)
    # initialize DATA for the new part.
#    DATA['divisions'] = 1
    DATA['measure'] = None
    DATA['note'] = None
    # added these
    # DATA['onset'] = None
    # DATA['meter'] = None
    # DATA['key'] =  None
    # DATA['onset'] = None


def _parse_measure(elem, DATA):
    # create a new measure and add it to the part
    measure = Measure(elem.get('number'))
    if elem.get('implicit') == 'yes':
        measure.partial = True
    DATA['measure'] = measure
    # add the new measure to the part
    DATA['part'].add_measure(measure)
    # initialize data that resets each measure
    DATA['note'] = None
    DATA['onset'] = Fraction(0,1)


def _parse_attributes(elem, DATA):
    measure = DATA['measure']
    for s in elem.iter(): 
        if s.tag == 'divisions':
            divs = s.text
            DATA['divisions'] = int(divs)
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
            #measure.clefs.append(clef)
            measure.add_element(clef)
        elif s.tag == 'time':
            num = s.findtext('beats')
            den = s.findtext('beat-type')
            staff = int(s.get("number", "0")) # 0=all staffs
            meter = Meter(int(num), int(den), staff)
            #measure.meters.append(meter)
            measure.add_element(meter)
            DATA['meter'] = meter
        elif s.tag == 'key':
            fifths = s.findtext('fifths')
            text = s.findtext('mode', "major")
            staff = int(s.get('number', "0")) # 0=all staffs
            mode = {'major': Mode.MAJOR, 'minor': Mode.MINOR, 'dorian': Mode.DORIAN, 'phrygian': Mode.PHRYGIAN, 
            'lydian': Mode.LYDIAN, 'mixolydian': Mode.MIXOLYDIAN, 'aeolian': Mode.AEOLIAN, 'ionian': Mode.IONIAN, 
            'locrian': Mode.LOCRIAN}[text]
            key = Key(int(fifths), mode, staff)
#            measure.keys.append(key)
            measure.add_element(key)
            DATA['key'] = key


def _parse_note(elem, DATA):
    first = elem[0].tag
    # first can be 'grace', 'cue', 'chord', 'rest'
    if first in ['grace', 'cue']:
        return
    type = 'note'
    duration = None
    pitch = None
    voice = 1    # ??? default?
    staff = None # ??? default?
    dots = 0
    note = None
    for e in elem.iter(): 
        if e.tag == 'pitch':
            step = e.findtext('step')
            alter = e.findtext('alter', "")
            if alter:
                alter = {-2: 'bb', -1: 'b', 0: '', 1: '#', 2: '##'}.get(int(alter), '')
            octave = e.findtext('octave')
            pitch = Pitch(step + alter + octave)
        elif e.tag == 'rest':
            type = e.tag
            pitch = Pitch()
        elif e.tag == 'chord':
            type = e.tag
        elif e.tag == 'duration':
            duration = int(e.text.strip())
        elif e.tag == 'dot':
            dots += 1
        elif e.tag == 'type':
            pass
        elif e.tag == 'stem':
            pass
        elif e.tag == 'voice':
            voice = int(e.text)
        elif e.tag == 'staff':
            pass
        elif e.tag == 'notations':
            pass
    # duration == dur/div * 1/4 == dur/(div*4)
    duration = Fraction(duration, DATA['divisions'] * 4)
    if DATA['measure'].partial:
        onset = DATA['meter'].measure_dur() - duration
        #print("*****", "measnum=", DATA['measure'].id, "measuredur=", DATA['meter'].measure_dur(), "duration=", duration)
    else:
        onset = DATA['onset']
    #print("part=", DATA['part'].id, "measure=", DATA['measure'].id, " onset=", onset, " pitch=", pitch)
    note = Note(time=onset, duration=duration, pitch=pitch) #, instrument=voice
    note.set_mxml('voice', voice)
    if type == 'chord':
        # if chording add note as a child of the previous note
        DATA['note'].add_child(note)
    else:
        # if note or rest add it to the current measure and update onset time.
        DATA['note'] = note
        DATA['measure'].add_element(note)
        DATA['onset'] += duration
    #print("***", "type:", type, "onset:", onset, "dur:", duration, "dots:", dots, "pitch:", pitch, "voice:", voice)
    # score time: if this is a partial measure then the onset time of the note
    # is calcuated as measuredur - duration
    # create the note and fill its attributes. if it is a chord, then update the
    # measure to contain a Chord instead of a Note.


def _parse_backup(elem, DATA):
    duration = int(elem.findtext('duration'))
    duration = Fraction(duration, DATA['divisions'] * 4)
    DATA['onset'] -= duration
    

def _parse_forward(elem, DATA):
    duration = int(elem.findtext('duration'))
    duration = Fraction(duration, DATA['divisions'] * 4)
    DATA['onset'] += duration
    # FIXME: what to do with these?
    #elem.findtext('staff')
    #elem.findtext('voice')


def _parse_work_title(elem, DATA):
    DATA['score'].metadata['title'] = elem.text


def _parse_work_creator(elem, DATA):
    DATA['score'].metadata['creator'] = elem.text


def _parse_work_rights(elem, DATA):
    DATA['score'].metadata['rights'] = elem.text


# Dictionary of parsing functions accessed by the corresponding MusicXml tag
# name.  Tags that are not in this dictionary are either not parsed or parsed
# by a function that is in the dictionary.
_PARSERS = {
    'part': _parse_part, 
    'measure': _parse_measure, 
    'attributes': _parse_attributes, 
    'barline': _parse_barline,
    'note': _parse_note,
    'backup': _parse_backup,
    'forward': _parse_forward,
    'work-title': _parse_work_title,
    'creator': _parse_work_creator,
    'rights': _parse_work_rights
    }


def load(path, trace=False):
    """
    Returns a `Notation` containing the contents of a MusicXml file.

    Parameters
    ----------
    path : string
        The pathname of the MusicXml file to load.
    trace : bool
        If true the raw MusicXml elements are printed to the terminal
        during the loading process.
    """
    global _DATA
    document = musicxml.parse(path, silence=True) 
    assert isinstance(document, musicxml.score_partwise), f"not a partwise musicxml file: '{path}'."
    root = getattr(document, 'gds_elementtree_node_') # root element of document
    assert isinstance(root, etree._Element) and root.tag == 'score-partwise', f"not a score-partwise element: {root}."
    # a dictionary maintaining the running status of parsing.
    DATA = _DATA.copy()
    DATA['score'] = Notation(metadata={'file': os.path.abspath(path)})
    DATA['divisions'] = 1 # default MusicXml divisions is 1 quarter note.
    # a depth-first traversal of all elements in the document.
    for x in root.iter():
        if trace:
            print(f"tag={x.tag}, attrs={x.attrib}, text='{x.text.strip() if x.text else ''}', children={len(x)}")
        parser = _PARSERS.get(x.tag)
        if parser:
            parser(x, DATA)
    return DATA['score']


if __name__ == "__main__":
    pass

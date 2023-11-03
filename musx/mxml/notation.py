"""
A module for loading and saving MusicXml scores.
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
from copy import copy
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
from collections import OrderedDict

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
#          measure and incremented by the duration of notes, forwards and backups.
#   tempo: A tempo map in score beats.
_DATA = {
    "score": None, "part": None, "measure": None, "divisions": None,
    "note": None, "meter:": None, "key": None, "onset": None, "tempo": None
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
        self.metadata = copy(metadata)
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
    
    def print(self, metadata=False):
        """
        Recursively prints the contents of the Notation. If metadata is True
        then only the contents of the metadata dictionary is printed.
        """
        pad = "  "

        if metadata:
            if self.metadata:
                print("{")
                for i in list(self.metadata):
                    print(f"{pad}{repr(i)}: {repr(self.metadata[i])}")
                print("}")
            return
        print(pad*0, self, sep=None)
        for p in self:
            print(pad*1, p, sep=None)
            for m in p:
                print(pad*2, m)
                for e in m:
                    print(pad*3, e)
    
    def timepoints(self, trace=False, spanners=False, flatten=False):
        """
        Returns a list of Timepoint objects grouped in measures. See: Timepoint.
        Parameters
        ----------
        trace : bool
            If true then the time points are displayed.
        spanners : bool
            If true then notes that began earlier than the current timepoint
            but are still sounding during the timepoint are added to the
            timepoint. A spanner is  disinguishable from other notes in
            the timepoint by virtue of its earlier start time than the timepoint
            and its inclusion in the Timepoint.spanners list. A spanners will
            appear as a 'repeat sign' :: in the trace output.
        flatten : bool
            If flatten is true then the timepoint list is flat , i.e. it does 
            not organizes measures as sublists in the list.
        """

        def _addspans(measure):
            # measure is a list of timepoints sorted by time.
            if len(measure) < 2: # need at least 2 timepoints to span...
                return
            for tp1,tp2 in zip(measure, measure[1:]):
                #print(f"beat: {tp1.onset} {tp1.notemap}")
                #print(f"beat: {tp2.onset} {tp2.notemap}")
                added = False
                for (pid, note) in tp1.notemap.items():
                    if note.time + note.duration > tp2.onset:
                        # add note from left timepoint into the right timepoint.
                        tp2.notemap[pid] = note
                        # register note as a spanner in this timepoint.
                        tp2.spanners.append(note )
                        added = True
                # if spanners were added (re)sort the notemap by part id.
                if added:
                    tp2.notemap = {id:tp2.notemap[id] for id in sorted(tp2.notemap)}

        # Flop the part measures so all measures with the same id are grouped
        #                   p1        p2            m1     m2     m3
        #                   m1 m2 m3  m1 m2 m3      p1  p2 p1 p2  p1 p2
        # together, e.g.: [[1, 2, 3],[1, 2, 3]] => [[1, 1],[2, 2],[3, 3]]
        groups = [measures for measures in zip(*[part.measures for part in self])]
        # iterate each group of measures
        timepoints = []
        for group in groups:
            # iterate each measure in the group combining their timepoints
            measurepoints = []
            for measure in group:
                for element in measure:
                    if isinstance(element, Note):
#                        ident = f"{measure.part.id}.{measure.id}.{element.get_mxml('voice')}"
                        ident = f"{measure.part.id}.{element.get_mxml('voice')}"
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
            if spanners:
                _addspans(measurepoints)
            if trace:
                for tp in measurepoints:
                    print(str(tp))
                print()
            if flatten:
                timepoints.extend(measurepoints)
            else:
                timepoints.append(measurepoints)
        return timepoints

    # def seq(self, applytempo=True):
    #     """
    #     Returns a sequence of copied notes for playback or writing to midi files.
    #     Parameters
    #     ----------
    #     tempocurve : bool
    #         If true the timepoints 
    #     """
    #     pass
    #     # tpoints = self.timepoints()
    #     # tempomap = self.metadata['tempo-map']
    #     # for measlist in tpoints:
    #     #     for point in measlist:

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

    def partids(self):
        """
        Returns the (sorted) list of part.measure.voice identifiers 
        active in this timepoint.
        """
        return self.notemap.keys()
    
    def notes(self, spanners=True):
        """
        Returns the notes in the timepoint sorted by voice id.
        If spanners is true then notes currently sounding
        from previous timepoints (if any) are included.
        """
        if spanners:
            return [self.notemap[id] for id in sorted(self.notemap)]
        return [self.notemap[id] for id in sorted(self.notemap) 
                if self.notemap[id] not in self.spanners]
        
    # def spanners(self):
    #     """
    #     Returns any notes that are currently sounding from previous timepoints.
    #     See: `timepoints(spanners=True)`
    #     """
    #     return self.spanners
    
    def __init__(self, onset):
        self.onset = onset
        """The ratio start time of the timepoint in its measure."""
        self.notemap = {}
        """The note map dictionary. Its keys are part.measure.voice identifiers
        and its values are `musx.note.Note` objects. Notes may be further tagged
        as being either pitches, chords or rests."""
        self.spanners = []
        """A list of notes that began in earlier timepoints but are still
            sounding during this timepoint."""

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
        #pstr = ", ".join([n._tagged_pitch_str() for n in self.notemap.values()])
        #return f"<Timepoint: {str(self.onset)} ({pstr})>"
        #return f"<Timepoint: {str(self.onset)}>"
        strs = []
        for id in self.notemap:
            note = self.notemap[id]
            info = f'{note._tagged_pitch_str()}, {note.duration}'
            if note.time < self.onset:
                info = "!" + info + "!"
            else:
                info = "(" + info + ")"
            info = id + ": " + info
            strs.append(info)
        text = ', '.join(strs)
        return f"<Timepoint: {str(self.onset):<5} {text}>"

    __repr__ = __str__


class Tempo():
    """
    Creates a tempo marking.
    Parameters
    ----------
    tempo : int
        The tempo expressed as quarter notes per minute.
    beat : Fraction
        The beat value for the tempo change, defaults to Fraction(1,4) or a quarter note.
    """
    def __init__(self, tempo, beat=Fraction(1,4)):
        self.tempo = tempo
        self.beat = beat

    def scale_to_tempo(self, value):
        return value/self.beat * 60 / self.tempo
    
    def __str__(self):
        return f"<Tempo: {self.tempo} {str(self.beat)}>"
    
    def __repr__(self):
        return f"Tempo({self.tempo}, {repr(self.beat)})"


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
    # cache the starting beat of this measure in the score. all
    # note times in the measure will be relative to this onset.
    if not DATA['measure']:
        measure.onset = 0  # onset 0 for first measure in each part
    else:
        # access the last note of the previous measure to calculate
        # the onset time of this (new) measure
        for e in DATA['measure'].elements[::-1]:
            if isinstance(e, Note):
                measure.onset = DATA['measure'].onset + e.time + e.duration
                break
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
    #tupa,tupn = None,None
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
    # duration == dur/div * 1/4 == dur/(div*4)
    duration = Fraction(duration, DATA['divisions'] * 4)
    onset = DATA['onset']
    # if DATA['measure'].partial:
    #     onset = DATA['meter'].measure_dur() - duration
    #     #print("*****", "measnum=", DATA['measure'].id, "measuredur=", DATA['meter'].measure_dur(), "duration=", duration)
    # else:
    #     onset = DATA['onset']
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
    DATA['score'].metadata['work-title'] = elem.text


def _parse_work_number(elem, DATA):
    DATA['score'].metadata['work-number'] = elem.text


def _parse_movement_title(elem, DATA):
    DATA['score'].metadata['movement-title'] = elem.text


def _parse_movement_number(elem, DATA):
    DATA['score'].metadata['movement-number'] = elem.text


def _parse_work_creator(elem, DATA):
    DATA['score'].metadata['creator'] = elem.text


def _parse_work_rights(elem, DATA):
    DATA['score'].metadata['rights'] = elem.text


def _parse_score_part(elem, DATA):
    # elem is 'score-part'
    metadata = DATA['score'].metadata
    try:
        partdata = metadata['partdata']
    except KeyError:
        partdata = {}
        metadata['partdata'] = partdata
    # add an empty info dictionary for the new part id.
    id = elem.get('id')
    partdata[id] = {'name': "", 'channel': 0, 'program': 0, 'volume': 90/127}
    info = partdata[id]
    for e in elem.iter():
        if e.tag == 'part-name':
            if e.text: # apparently this can be empty! (chopin_prelude_op28_no20.xml)
                info['name'] = e.text.strip()
        elif e.tag == 'midi-channel':
            info['channel'] = int(e.text)
        elif e.tag == 'midi-program':
            info['program'] = int(e.text)
        elif e.tag == 'volume':
            info['volume'] = float(e.text)


def _parse_sound(elem, DATA):
    tempo=elem.get("tempo", None)
    if tempo: 
        # add next tempo to map: [<scoretime> <tempo>]
        scoretime = DATA['measure'].onset + DATA['onset']
        thistempo = [ scoretime*1.0, int(tempo) ]
        DATA['score'].metadata['tempo-map'].extend(thistempo)

# def _parse_sound(elem, DATA):
#     tempo=elem.get("tempo", None)
#     if tempo:
#         print("**** TEMPO measure=", DATA['measure'].id, ", tempo=", tempo)
#         DATA['measure'].add_element(Tempo(int(tempo)))

# Dictionary of parsing functions accessed by the corresponding MusicXml tag
# name.  Tags that are not in this dictionary are either not parsed or parsed
# by a function that is in the dictionary.
_PARSERS = {
    'score-part': _parse_score_part,
    'part': _parse_part, 
    'measure': _parse_measure, 
    'attributes': _parse_attributes, 
    'barline': _parse_barline,
    'note': _parse_note,
    'backup': _parse_backup,
    'forward': _parse_forward,
    'work-title': _parse_work_title,
    'work-number': _parse_work_number,
    'movement-title': _parse_movement_title,
    'movement-number': _parse_movement_number,
    'creator': _parse_work_creator,
    'rights': _parse_work_rights,
    'sound': _parse_sound
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
    DATA['score'] = Notation(metadata={'file': os.path.abspath(path), 'tempo-map': []})
    DATA['divisions'] = 1 # default MusicXml divisions is 1 quarter note.
    DATA['tempo'] = [] # list of [score_time tempo ..]
    # a depth-first traversal of all elements in the document.
    for x in root.iter():
        if trace:
            print(f"tag={x.tag}, attrs={x.attrib}, text='{x.text.strip() if x.text else ''}', children={len(x)}")
        parser = _PARSERS.get(x.tag)
        if parser:
            parser(x, DATA)
    # # default tempo is 120 ??
    # if not DATA['score']['tempo-map']:
    #     DATA['score']['tempo-map'].extend([Fraction(0,1), Tempo(120)])
    return DATA['score']


if __name__ == "__main__":
    pass

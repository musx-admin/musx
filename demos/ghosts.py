################################################################################
"""
A main composer creates a mid-range melody and accompanies it by adding other
decorative composers that create high tones, low thumps, and strums that spread
out over longer and longer timepoints in the future.

To run this script cd to the parent directory of demos/ and do:
```bash
python3 -m demos.ghosts
```
"""


from random import choice
from musx.generators import steps
from musx.ran import between
from musx.tools import playfile, setmidiplayer
from musx.score import Score
from musx.midi import MidiNote, MidiSeq, MidiFile
from musx.midi.gm import Flute, Clarinet, Cello, OrchestralHarp


def flute(sco, knum, dur):
    """
    Creates the flute part on channel 0.
    
    Parameters
    ----------
    sco : Score
        The musical score to add events to.
    knum : int
        The midi keynumber of the clarinet.
    dur : int | float
        The duration of the note.
    """
    sco.add(MidiNote(time=sco.now, dur=dur, key=knum+24, amp=.2, chan=0))
    yield -1


def cello(sco, knum):
    """
    Creates the cello part on channel 2.
    
    Parameters
    ----------
    sco : Score
        The musical score to add events to.
    knum : int
        The midi key number of the clarinet.
    """
    sco.add(MidiNote(time=sco.now, dur=.05, key=knum-18, amp=.9, chan=2))
    sco.add(MidiNote(time=sco.now, dur=.05, key=knum-23, amp=.9, chan=2))
    yield -1


def harp(sco, knum, rate):
    """
    Creates an arpeggiating harp part on channel 3.
    
    Parameters
    ----------
    sco : Score
        The musical score to add events to.
    knum : int
        The midi keynumber of the clarinet.
    rate : int | float
        The rhythm of the arpeggio.
    """
    for k in steps(39 + (knum % 13),  13, 5):
        m = MidiNote(time=sco.now, dur=10, key=k, amp=.5, chan=3)
        sco.add(m)
        yield rate


def ghosts(sco):
    """
    Creates mid-range clarinet line and decorates it with
    calls to the other instrument composers.
    
    Parameters
    ----------
    sco : Score
        The musical score to add events to.
    """
    for _ in range(12):
        here = sco.elapsed
        ahead = (here + 1/2) * 2
        melody = between(53, 77)
        high = (melody >=  65)
        amp = .2 if high else .4
        rhy = choice([1/4, 1/2, 3/4])
        # the clarinet line
        midi = MidiNote(time=sco.now, dur=rhy + .2, key=melody, amp=amp, chan=1)
        sco.add(midi)
        # add decorations to the clarinet melody
        if high:
            sco.compose([ahead, flute(sco, melody, ahead)])
            sco.compose([ahead * 2, harp(sco, melody, rhy / 4)])
        elif (rhy == 3/4):
            sco.compose([1/2, cello(sco, melody)])
        yield rhy


if __name__ == '__main__':
    # It's good practice to add any metadata such as tempo, midi instrument
    # assignments, micro tuning, etc. to track 0 in your midi file.
    inst = {0: Flute, 1: Clarinet, 2: Cello, 3: OrchestralHarp}
    tr0 = MidiSeq.metaseq(ins=inst)
    # Track 1 will hold the composition.
    tr1 = MidiSeq()
    # Create a score and give it tr1 to hold the score event data.
    sco = Score(out=tr1)
    # Start our composer in the scheduler, this creates the composition.
    sco.compose(ghosts(sco))
    # Write a midi file with our track data.
    file = MidiFile("ghosts.mid", [tr0, tr1]).write()
    print(f"Wrote '{file.pathname}'.")

    # To automatially play demos use setmidiplayer() and playfile().
    # Example:
    #     setmidiplayer("fluidsynth -iq -g1 /usr/local/sf/MuseScore_General.sf2")
    #     playfile(file.pathname)



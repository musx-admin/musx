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
from musx.scheduler import Scheduler
from musx.midi import MidiNote, MidiSeq, MidiFile
from musx.midi.gm import Flute, Clarinet, Cello, OrchestralHarp


def flute(q, knum, dur):
    """
    Creates the flute part on channel 0.
    
    Parameters
    ----------
    q : Scheduler
        The scheduling queue.
    knum : int
        The midi keynumber of the clarinet.
    dur : int | float
        The duration of the note.
    """
    q.out.addevent(MidiNote(time=q.now, dur=dur, key=knum+24, amp=.2, chan=0))
    yield -1


def cello(q, knum):
    """
    Creates the cello part on channel 2.
    
    Parameters
    ----------
    q : Scheduler
        The scheduling queue.
    knum : int
        The midi key number of the clarinet.
    """
    q.out.addevent(MidiNote(time=q.now, dur=.05, key=knum-18, amp=.9, chan=2))
    q.out.addevent(MidiNote(time=q.now, dur=.05, key=knum-23, amp=.9, chan=2))
    yield -1


def harp(q, knum, rate):
    """
    Creates an arpeggiating harp part on channel 3.
    
    Parameters
    ----------
    q : Scheduler
        The scheduling queue.
    knum : int
        The midi keynumber of the clarinet.
    rate : int | float
        The rhythm of the arpeggio.
    """
    for k in steps(39 + (knum % 13),  13, 5):
        m = MidiNote(time=q.now, dur=10, key=k, amp=.5, chan=3)
        q.out.addevent(m)
        yield rate


def ghosts(q):
    """
    Creates mid-range clarinet line and decorates it with
    calls to the other instrument composers.
    
    Parameters
    ----------
    q : Scheduler
        The scheduling queue.
    """
    for _ in range(12):
        here = q.elapsed
        ahead = (here + 1/2) * 2
        melody = between(53, 77)
        high = (melody >=  65)
        amp = .2 if high else .4
        rhy = choice([1/4, 1/2, 3/4])
        # the clarinet line
        midi = MidiNote(time=q.now, dur=rhy + .2, key=melody, amp=amp, chan=1)
        q.out.addevent(midi)
        # add decorations to the clarinet melody
        if high:
            q.compose([ahead, flute(q, melody, ahead)])
            q.compose([ahead * 2, harp(q, melody, rhy / 4)])
        elif (rhy == 3/4):
            q.compose([1/2, cello(q, melody)])
        yield rhy


if __name__ == '__main__':
    # It's good practice to add any metadata such as tempo, midi instrument
    # assignments, micro tuning, etc. to track 0 in your midi file.
    inst = {0: Flute, 1: Clarinet, 2: Cello, 3: OrchestralHarp}
    t0 = MidiSeq.metaseq(ins=inst)
    # Track 1 will hold the composition.
    t1 = MidiSeq()
    # Create a scheduler and give it t1 as its output object.
    q = Scheduler(t1)
    # Start our composer in the scheduler, this creates the composition.
    q.compose(ghosts(q))
    # Write a midi file with our track data.
    f = MidiFile("ghosts.mid", [t0, t1]).write()
    # To automatially play demos use setmidiplayer() to assign a shell
    # command that will play midi files on your computer. Example:
    #   setmidiplayer("fluidsynth -iq -g1 /usr/local/sf/MuseScore_General.sf2")
    print(f"Wrote '{f.pathname}'.")
    playfile(f.pathname)


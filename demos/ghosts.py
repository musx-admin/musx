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


from musx import Score, Note, Seq, MidiFile, between, pick, steps
from musx.midi.gm import Flute, Clarinet, Cello, OrchestralHarp


def flute(score, knum, dur):
    """
    Creates the flute part on channel 0.
    
    Parameters
    ----------
    score : Score
        The musical score to add events to.
    knum : int
        The midi keynumber of the clarinet.
    dur : int | float
        The duration of the note.
    """
    score.add(Note(time=score.now, duration=dur, pitch=knum+24, amplitude=.2, instrument=0))
    yield -1


def cello(score, knum):
    """
    Creates the cello part on channel 2.
    
    Parameters
    ----------
    score : Score
        The musical score to add events to.
    knum : int
        The midi key number of the clarinet.
    """
    score.add(Note(time=score.now, duration=.05, pitch=knum-18, amplitude=.9, instrument=2))
    score.add(Note(time=score.now, duration=.05, pitch=knum-23, amplitude=.9, instrument=2))
    yield -1


def harp(score, knum, rate):
    """
    Creates an arpeggiating harp part on channel 3.
    
    Parameters
    ----------
    score : Score
        The musical score to add events to.
    knum : int
        The midi keynumber of the clarinet.
    rate : int | float
        The rhythm of the arpeggio.
    """
    for k in steps(39 + (knum % 13),  13, 5):
        m = Note(time=score.now, duration=10, pitch=k, amplitude=.5, instrument=3)
        score.add(m)
        yield rate


if __name__ == '__main__':
    # It's good practice to add any metadata such as tempo, midi instrument
    # assignments, micro tuning, etc. to track 0 in your midi file.
    insts = {0: Flute, 1: Clarinet, 2: Cello, 3: OrchestralHarp}
    track0 = MidiFile.metatrack(ins=insts)
    # Track 1 will hold the composition.
    track1 = Seq()
    # Create a score and give it tr1 to hold the score event data.
    score = Score(out=track1)
    # Start our composer in the scheduler, this creates the composition.
    score.compose(ghosts(score))
    # Write a midi file with our track data.
    file = MidiFile("ghosts.mid", [track0, track1]).write()
    print(f"Wrote '{file.pathname}'.")

    # To automatially play demos use setmidiplayer() and playfile().
    # Example:
    #     setmidiplayer("fluidsynth -iq -g1 /usr/local/sf/MuseScore_General.sf2")
    #     playfile(file.pathname)



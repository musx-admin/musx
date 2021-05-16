################################################################################
"""
This example uses two copies of the same composer to generate the two
piano parts in Steve Reich's Piano Phase.

To run this script cd to the parent directory of demos/ and do:
```bash
python3 -m demos.reich
```
"""


from musx.midi import MidiNote, MidiSeq, MidiFile
from musx.scheduler import Scheduler
from musx.generators import cycle
from musx.scales import keynum
from musx.tools import setmidiplayer, playfile


def piano_phase(q, end, keys, rate):
    """
    Composes a piano part for Steve Reich's Piano Phase.

    Parameters
    ----------
    q : Scheduler
        The scheduling queue to run the composer in.
    end : int | float
        The total duration of the piece.
    keys : list
        A list of midi key numbers to play in a loop.
    rate : int | float
        The rhythm to use.    
    """
    # Create a cyclic pattern to produce the key numbers.
    pattern = cycle(keys)
    # Stop playing when the scheduler's score time is >= end.
    while q.now < end:
        # Get the next key number.
        knum = next(pattern)
        # Create a midi note to play it.
        note = MidiNote(time=q.now, dur=rate, key=knum, amp=.9)
        # Add the midi note to the output midi sequence.
        q.out.addevent(note)
        # Return the amount of time until this composer runs again.
        yield rate


if __name__ == '__main__':
    # It's good practice to add any metadata such as tempo, midi instrument
    # assignments, micro tuning, etc. to track 0 in your midi file.
    t0 = MidiSeq.metaseq()
    # Track 1 will hold the composition.
    t1 = MidiSeq()
    # Create a scheduler and give it t1 as its output object.
    q = Scheduler(t1)
    # Convert Reich's notes to a list of midi key numbers to phase.
    keys = keynum("e4 f# b c#5 d f#4 e c#5 b4 f# d5 c#")
    # Create two composer generators that run at slightly different 
    # rates and cause the phase effect.
    pianos = [piano_phase(q, 20, keys, .167), 
              piano_phase(q, 20, keys, .170)]
    # Start our composer in the scheduler, this creates the composition.
    q.compose(pianos)
    # Write the seq to a midi file in the current directory.
    f=MidiFile("reich.mid", [t0, t1]).write()
    # To automatially play demos use setmidiplayer() to assign a shell
    # command that will play midi files on your computer. Example:
    #   setmidiplayer("fluidsynth -iq -g1 /usr/local/sf/MuseScore_General.sf2")
    print(f"Wrote '{f.pathname}'.")
    playfile(f.pathname)

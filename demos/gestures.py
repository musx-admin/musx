################################################################################
"""
Gestures demonstrates how small units of code can serve as building blocks for
creating larger musical structures.

To run this script cd to the parent directory of demos/ and do:
```bash
python3 -m demos.gestures
```
"""


import random
from musx.generators import jumble
from musx.midi import MidiNote, MidiSeq, MidiFile
from musx.midi.gm import AcousticGrandPiano, Marimba, OrchestralHarp
from musx.scheduler import Scheduler
from musx.ran import odds, between
from musx.tools import quantize, playfile, setmidiplayer
from musx.envelopes import interp


def motive1(q, octave, limit, chan):
    """
    Motive1 generates three notes in random order but always with a
    whole step and minor seventh sounding. The motive can be randomly
    transposed within limit half-steps.

    Parameters
    ----------
    q : Scheduler
        The scheduling queue.
    octave : int
        The octave to play the notes in.
    limit : int
        The maximum transposition in half steps.
    chan : int
        The midi channel to assign to the notes.
    """
    # the basic pitches to transpose and jumble e.g. [F#4 E4 D5].
    pitches = jumble([6, 4, 14])
    # one of the three pitches will be louder than the others.
    amps = jumble([.75, .5, .5])
    # randomly chosen transpostion within a limit
    offset = random.randrange(limit)
    for _ in range(3):
        knum = next(pitches) + (octave * 12) + offset
        note = MidiNote(time=q.now, dur=.1, key=knum, amp=next(amps), chan=chan)
        q.out.addevent(note)
        yield .2
    

def motive2(q, octave, limit, chan):
    """Motive2 generates a repeated tone with one tone accented."""
    amps = jumble([.75, .5, .5])
    rhys = jumble([.2, .2, .4])
    offset = random.randrange(limit)
    for _ in range(3):
        knum = 0 + (octave * 12) + offset
        note = MidiNote(time=q.now, dur=.1, key=knum, amp=next(amps), chan=chan)
        q.out.addevent(note)
        yield next(rhys)


def gesture1(q, numtimes, o, chan):
    for _ in range(numtimes):
        if (odds(o)):
            q.compose(motive1(q, 5, 1, chan))
        else:
            q.compose(motive2(q, 6, 1, chan))
        yield 2


def gesture2(q, numtimes, o, limit, chan):
    """The same as gesture1 but with transposition upto limit."""
    for _ in range(numtimes):
        if (odds(o)):
            q.compose(motive1(q, 5, limit, chan))
        else:
            q.compose(motive2(q, 6, limit, chan))
        yield 2


def qtime(n, total, start, end, quant):
    """
    Over total time move from start to end by quant step size. The
    end value is reached half-way through and sticks thereafter.
    """
    return quantize(interp(n / total, 0, start, .5, end), quant)


def gesture3(q, numtimes, o, limit, chan, hiwait, lowwait):
    """Like gesture2 but takes smaller amounts of time between motives."""
    for i in range(numtimes):
        if (odds(o)):
            q.compose(motive1(q, 5, limit, chan))
        else:
            q.compose(motive2(q, 6, limit, chan))
        yield qtime(i, numtimes, 2, .2, .2)


def gesture4(q, numtimes, lowoctave, highoctave, limit, chan, hiwait, lowwait):
    """
    Gesture4 is similar to gesture3 but chooses octaves and gradually
    prefers motive2 over motive1.
    """
    for i in range(numtimes):
        if odds(qtime(i, numtimes, 1.0, 0.0, .01)):
            q.compose(motive1(q, between(lowoctave, highoctave), limit, chan))
        else:
            q.compose(motive2(q, between(lowoctave, highoctave), limit, chan))
        yield qtime(i, numtimes, hiwait, lowwait, .2)


if __name__ == '__main__':
    # It's good practice to add any metadata such as tempo, midi instrument
    # assignments, micro tuning, etc. to track 0 in your midi file.
    t0 = MidiSeq.metaseq(ins={0: AcousticGrandPiano, 1: Marimba, 2: OrchestralHarp})
    # Track 1 will hold the composition.
    t1 = MidiSeq()
    # Create a scheduler and give it t1 as its output object.
    q = Scheduler(t1)

    #play = motive1(q, 5, 4, 0)
    #play = motive2(q, 5,5,1)
    #play = gesture1(q, 10, .5, 0)
    #play = gesture2(q, 10, .5, 5, 0)
    #play = gesture3(q, 20, .5, 5, 0, 3, .2)
    #play = gesture4(q, 30, 2, 7, 11, 0, 1.6,.2)

    # The gesture to play
    play = [gesture4(q, 60, 2, 7, 11, 0, 1.0, .2),
            gesture4(q, 40, 5, 7, 11, 1, 1.6, .2),
            gesture4(q, 34, 3, 6, 11, 2, 2.0, .2)]
    # Start our composer in the scheduler, this creates the composition.
    q.compose(play)
    # Write a midi file with our track data.
    f = MidiFile("gestures.mid", [t0, t1]).write()
    # To automatially play demos use setmidiplayer() to assign a shell
    # command that will play midi files on your computer. Example:
    #   setmidiplayer("fluidsynth -iq -g1 /usr/local/sf/MuseScore_General.sf2")
    print(f"Wrote '{f.pathname}'.")
    playfile(f.pathname)


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
from musx import Score, Note, Seq, MidiFile, jumble, odds, between, quantize, interp
from musx.midi.gm import AcousticGrandPiano, Marimba, OrchestralHarp


def motive1(score, octave, limit, chan):
    """
    Motive1 generates three notes in random order but always with a
    whole step and minor seventh sounding. The motive can be randomly
    transposed within limit half-steps.

    Parameters
    ----------
    score : Score
        The score.
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
        note = Note(time=score.now, duration=.1, pitch=knum, amplitude=next(amps), instrument=chan)
        score.add(note)
        yield .2
    

def motive2(score, octave, limit, chan):
    """Motive2 generates a repeated tone with one tone accented."""
    amps = jumble([.75, .5, .5])
    rhys = jumble([.2, .2, .4])
    offset = random.randrange(limit)
    for _ in range(3):
        knum = 0 + (octave * 12) + offset
        note = Note(time=score.now, duration=.1, pitch=knum, amplitude=next(amps), instrument=chan)
        score.add(note)
        yield next(rhys)


def gesture1(score, numtimes, o, chan):
    for _ in range(numtimes):
        if (odds(o)):
            score.compose(motive1(score, 5, 1, chan))
        else:
            score.compose(motive2(score, 6, 1, chan))
        yield 2


def gesture2(score, numtimes, o, limit, chan):
    """The same as gesture1 but with transposition upto limit."""
    for _ in range(numtimes):
        if (odds(o)):
            score.compose(motive1(score, 5, limit, chan))
        else:
            score.compose(motive2(score, 6, limit, chan))
        yield 2


def qtime(n, total, start, end, quant):
    """
    Over total time move from start to end by quant step size. The
    end value is reached half-way through and sticks thereafter.
    """
    return quantize(interp(n / total, 0, start, .5, end), quant)


def gesture3(score, numtimes, o, limit, chan, hiwait, lowwait):
    """Like gesture2 but takes smaller amounts of time between motives."""
    for i in range(numtimes):
        if (odds(o)):
            score.compose(motive1(score, 5, limit, chan))
        else:
            score.compose(motive2(score, 6, limit, chan))
        yield qtime(i, numtimes, 2, .2, .2)


def gesture4(score, numtimes, lowoctave, highoctave, limit, chan, hiwait, lowwait):
    """
    Gesture4 is similar to gesture3 but chooses octaves and gradually
    prefers motive2 over motive1.
    """
    for i in range(numtimes):
        if odds(qtime(i, numtimes, 1.0, 0.0, .01)):
            score.compose(motive1(score, between(lowoctave, highoctave), limit, chan))
        else:
            score.compose(motive2(score, between(lowoctave, highoctave), limit, chan))
        yield qtime(i, numtimes, hiwait, lowwait, .2)


if __name__ == '__main__':
    # It's good practice to add any metadata such as tempo, midi instrument
    # assignments, micro tuning, etc. to track 0 in your midi file.
    track0 = MidiFile.metatrack(ins={0: AcousticGrandPiano, 1: Marimba, 2: OrchestralHarp})
    # Track 1 will hold the composition.
    track1 = Seq()
    # Create a score and give it tr1 to hold the score event data.
    score = Score(out=track1)

    #play = motive1(q, 5, 4, 0)
    #play = motive2(q, 5,5,1)
    #play = gesture1(q, 10, .5, 0)
    #play = gesture2(q, 10, .5, 5, 0)
    #play = gesture3(q, 20, .5, 5, 0, 3, .2)
    #play = gesture4(q, 30, 2, 7, 11, 0, 1.6,.2)

    # The gesture to play
    play = [gesture4(score, 60, 2, 7, 11, 0, 1.0, .2),
            gesture4(score, 40, 5, 7, 11, 1, 1.6, .2),
            gesture4(score, 34, 3, 6, 11, 2, 2.0, .2)]
    # Create the composition.
    score.compose(play)
    # Write the seqs to a midi file in the current directory.
    file = MidiFile("gestures.mid", [track0, track1]).write()
    print(f"Wrote '{file.pathname}'.")
    
    # To automatially play demos use setmidiplayer() and playfile().
    # Example:
    #     setmidiplayer("fluidsynth -iq -g1 /usr/local/sf/MuseScore_General.sf2")
    #     playfile(file.pathname)

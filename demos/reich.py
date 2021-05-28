################################################################################
"""
This example uses two copies of the same composer to generate the two
piano parts in Steve Reich's Piano Phase.

To run this script cd to the parent directory of demos/ and do:
```bash
python3 -m demos.reich
```
"""


from musx import Score, Note, MidiSeq, MidiFile, cycle, keynum


def piano_phase(sco, end, keys, rate):
    """
    Composes a piano part for Steve Reich's Piano Phase.

    Parameters
    ----------
    sco : Score
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
    while sco.now < end:
        # Get the next key number.
        knum = next(pattern)
        # Create a midi note to play it.
        note = Note(time=sco.now, dur=rate, key=knum, amp=.9)
        # Add the midi note to the score.
        sco.add(note)
        # Return the amount of time until this composer runs again.
        yield rate


if __name__ == '__main__':
    # It's good practice to add any metadata such as tempo, midi instrument
    # assignments, micro tuning, etc. to track 0 in your midi file.
    tr0 = MidiSeq.metaseq()
    # Track 1 will hold the composition.
    tr1 = MidiSeq()
    # Create a score and give it tr1 to hold the score event data.
    sco = Score(out=tr1)
    # Convert Reich's notes to a list of midi key numbers to phase.
    keys = keynum("e4 f# b c#5 d f#4 e c#5 b4 f# d5 c#")
    # Create two composer generators that run at slightly different 
    # rates and cause the phase effect.
    pianos = [piano_phase(sco, 20, keys, .167), 
              piano_phase(sco, 20, keys, .170)]
    # Create the composition.
    sco.compose(pianos)
    # Write the tracks to a midi file in the current directory.
    file=MidiFile("reich.mid", [tr0, tr1]).write()
    print(f"Wrote '{file.pathname}'.")
    
    # To automatially play demos use setmidiplayer() and playfile().
    # Example:
    #     setmidiplayer("fluidsynth -iq -g1 /usr/local/sf/MuseScore_General.sf2")
    #     playfile(file.pathname)

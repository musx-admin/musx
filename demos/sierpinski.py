###############################################################################
"""
A musical hommage to the Sierpinski triangle using a recursive process to
generate a self-similar melodies based on a set of tones representing the
"sides" of a triangle.  The duration of each note is the process duration
divided by the number of intervals in the melody. Thus, the entire melody
in the next level will occupy the same mount of time as one tone in the
current level. When the process starts running it outputs each note in the
melody transposed to the current tone. If levels is greater then 1 then the
process sprouts recursive copies of itself for each note in the melody
transposed up trans intervals. The value for levels is decremented by 1,
which will cause the recursive process to stop when the value reaches 0.

To run this script cd to the parent directory of demos/ and do:
```bash
python3 -m demos.sierpinski
```
"""


from musx import Score, Note, Seq, MidiFile, keynum


def sierpinski(sco, tone, shape, trans, levels, dur, amp):
    """
    Generates a melodic shape based on successive transpositions (levels) of
    itself. 
    
    Parameters
    ----------
    sco : Score
        The musical score to add events to.
    tone : keynum
        The melodic tone on which to base the melody for the current level.
    shape : list
        A list of intervals defining the melodic shape. 
    levels : int
        The number of levels the melody should be reproduced on. 
    dur : int | float
        The duration of the process.
    amp : float
        The amplitude of the process.
    """
    num = len(shape)
    for i in shape:
        k = tone + i
        # play current tone in melody
        m = Note(time=sco.now, dur=dur, key=min(k,127), amp=amp, chan=0)
        sco.add(m)
        if (levels > 1):
            # sprout melody on tone at next level
            sco.compose(sierpinski(sco, (k + trans), shape,
                        trans, levels - 1, dur / num,  amp))
        yield dur
    

if __name__ == "__main__":
    # It's good practice to add any metadata such as tempo, midi instrument
    # assignments, micro tuning, etc. to track 0 in your midi file.
    tr0 = Seq.metaseq()
    # Track 1 will hold the composition.
    tr1 = Seq()
    # Create a scheduler and give it t1 as its output object.
    sco = Score(out=tr1)
    # Create the composition. Specify levels and melody length with care!
    # The number of events that are generateed is exponentially related to
    # the length of the melody and the number of levels. For example the
    # first compose() generates 120 events, the second 726, and the third 2728!
    sco.compose(sierpinski(sco, keynum('a0'), [0, 7, 5], 12, 4, 3, .5))
    # sco.compose(sierpinski(q, keynum('a0'), [0, 7, 5], 8, 5, 7, .5))
    # sco.compose(sierpinski(q, keynum('a0'), [0, -1, 2, 13], 12, 5, 24, .5))
 
    # Write the tracks to a midi file in the current directory.
    file = MidiFile("sierpinski.mid", [tr0, tr1]).write()
    print(f"Wrote '{file.pathname}'.")
    
    # To automatially play demos use setmidiplayer() and playfile().
    # Example:
    #     setmidiplayer("fluidsynth -iq -g1 /usr/local/sf/MuseScore_General.sf2")
    #     playfile(file.pathname)



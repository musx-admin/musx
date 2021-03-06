###############################################################################
"""
Ring modulation generates pairwise sum and difference tones of two input 
spectra. This little etude utilizes both the input and output spectra 
simultaneously to create a funky two part composition.

To run this script cd to the parent directory of demos/ and do:
```bash
python3 -m demos.rm
```
"""


from musx import Score, Note, Seq, MidiFile, rmspectrum, choose, jumble,\
     cycle, hertz, scale, pick, intempo
from musx.midi.gm import Clarinet, Marimba


def accompaniment(score, reps, dur, set1, set2):
    """
    Creates the accompanyment part from the ring modulation input specta.

    Parameters
    ----------
    score : Score
        The musical score.
    reps : int
        The number of sections to compose.
    dur : int
        The surface rhythm
    set1 : list
        Ring modulation input 1.
    set2 : list
        Ring modulation input 2.
    """
    # Create a cycle of the two inputs
    pat = cycle([set1, set2])
    for _ in range(reps*2):
        # Get the next set.
        keys = next(pat)
        # Iterate the keys, play as a chord.
        for k in keys:
            # Create a midi note at the current time.
            n = Note(time=score.now, duration=dur, pitch=k, amplitude=.3, instrument=0)
            # Add it to our output seq.
            score.add(n)
        # Wait till the next chord.
        yield dur


def melody(score, reps, dur, set3):
    """
    Creates the melodic part out of the ring modulated output specta.
 
    Parameters
    ----------
    score : Score
        The musical score.
    reps : int
        The number of sections to compose.
    dur : int
        The surface rhythm
    keys : list
        List of keynums from ring modulation output.
    """
    # Create a cycle of the two inputs
    pat = cycle(set3)
    for _ in range(2 * reps):
        n = Note(time=score.now, duration=dur/2, pitch=next(pat), amplitude=.7, instrument=1)
        score.add(n)
        # Wait till the next note
        yield dur


def rmfunky(score, reps, dur, keys):
    """
    Main composer chooses input spectra , creates a ring modulated
    output spectrum and plays them using two parts.

    Parameters
    ----------
    score : Score
        The musical score.
    reps : int
        The number of sections to compose.
    dur : int
        The surface rhythm
    keys : list
        List of keynums for ring modulation input.
    """
    num = choose([1,2,3])
    # scramble the cycle of fourths
    pat = jumble(keys)
    for _ in range(reps):
        # input1 is 1, 2 or 3 notes from cycle of 4ths
        keys1 = [next(pat) for _ in range(next(num))]
        # input2 is same
        keys2 = [next(pat) for _ in range(next(num))]
        # ring modulate the inputs
        spect = rmspectrum([hertz(k) for k in keys1], [hertz(k) for k in keys2])
        # convert to keynums
        keys3 = spect.keynums(quant=1, unique=True, minkey=21, maxkey=108)
        # sprout composers to play inputs and output
        playn = pick(3,4,5)
        score.compose(accompaniment(score, playn, dur, keys1, keys2))
        score.compose(melody(score, playn, dur, keys3))        # do it again after composers finish
        yield (dur * playn * 2)


if __name__ == '__main__':
    # It's good practice to add any metadata such as tempo, midi instrument
    # assignments, micro tuning, etc. to track 0 in your midi file.
    track0 = MidiFile.metatrack(ins={0: Marimba, 1: Clarinet})
    # Track 1 will hold the composition.
    track1 = Seq()
    # Create a score and give it tr1 to hold the score event data.
    score = Score(out=track1)
    # Musical material is the cycle of fourths.
    keys = scale(40, 12, 5)
    # Surface rhythm
    rhy = intempo(.25, 74)
    # Create the composition.
    score.compose(rmfunky(score, 24, rhy, keys))
    # Write the tracks to a midi file in the current directory.
    file = MidiFile("rm.mid", [track0, track1]).write()
    print(f"Wrote '{file.pathname}'.")

    # To automatially play demos use setmidiplayer() and playfile().
    # Example:
    #     setmidiplayer("fluidsynth -iq -g1 /usr/local/sf/MuseScore_General.sf2")
    #     playfile(file.pathname)





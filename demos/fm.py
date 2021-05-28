###############################################################################
"""
FM is a powerful algorithm that generates a wide variety of spectra, both 
harmonic and inharmonic, from just three input parameters:
a carrier (center frequency), a carrier/modulator ratio, and an FM 
index that controls the density, or width, of the spectrum.

To run this script cd to the parent directory of demos/ and do:
```bash
python3 -m demos.fm
```
"""


import random
from musx import Note, Score, MidiSeq, MidiFile, Spectrum, fmspectrum, keynum, hertz, odds, between, pick


def fm_chords(sco, reps, cen, cm1, cm2, in1, in2, rhy):
    """
    Generates a series of FM chords with random fluctuations in its
    C/M ratios and indexes to yield variations of chordal notes.
    """
    for _ in reps:
        spec = fmspectrum(hertz(cen), between(cm1, cm2), between(in1, in2)) 
        for k in spec.keynums(minkey=48, maxkey=72):
            m = Note(time=sco.now, dur=rhy, key=k, amp=.5)
            sco.add(m)
    yield rhy


contour = keynum("a4 g f e a4 b c d gs b c5 ef fs g a5 bf g f e a5 b c d \
                  gs3 f e cs c bf5 gs5 as3 cs5 e6 f4 gs5 d6 e f g c5 b a \
                  g bf c5 cs e4 f gs d4 c b a4 e5 f g a5")


def fm_improv(sco, line, beat):
    """
    Uses a contour line of carrier frequencies (specified as midi keynums)
    to produces fm spectra that creates both melodic and harmoinc gestures.
    The inputs and outputs of the fmspectrum() calls are printed during the
    improvisation.
    """
    amp = .7
    dur = beat
    for knum in line:
        ismel = odds(.7)
        rhy = pick(dur, dur / 2, dur / 4)
        f, r, x = hertz(knum), between(1.1, 1.9), pick(1, 2, 3)
        print("\ncarrier=",f,"c/m ratio=",r,"fm index=",x)
        spec = fmspectrum(f,r,x)
        keys = spec.keynums(unique=True, minkey=knum-14, maxkey=knum+14)

        if ismel:
            random.shuffle(keys)
        sub = rhy / len(keys) if ismel else 0
        print("melody:" if ismel else "chord:", "time=", sco.now, "dur=", rhy, "keys=", keys)
        for i, k in enumerate(keys):
            m = Note(time=sco.now + (i * sub), dur=dur, key=k, amp=amp)
            sco.add(m)
        yield rhy


if __name__ == '__main__':
    # It's good practice to add any metadata such as tempo, midi instrument
    # assignments, micro tuning, etc. to track 0 in your midi file.
    tr0 = MidiSeq.metaseq()
    # Track 1 will hold the composition.
    tr1 = MidiSeq()
    # Create a score and give it tr1 to hold the score event data.
    sco = Score(out=tr1)
    # Create the composition.

    # sco.compose(fm_chords(sco, 12, 60, 1.0, 2.0, 2.0, 4.0, .8))
    sco.compose(fm_improv(sco, contour, 1))

    #  Write the tracks to a midi file in the current directory.
    file = MidiFile("fm.mid", [tr0, tr1]).write()
    print(f"Wrote '{file.pathname}'.")

    # To automatially play demos use setmidiplayer() and playfile().
    # Example:
    #     setmidiplayer("fluidsynth -iq -g1 /usr/local/sf/MuseScore_General.sf2")
    #     playfile(file.pathname)


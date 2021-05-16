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
from musx.spectral import Spectrum, fmspectrum
from musx.scheduler import Scheduler
from musx.scales import keynum, hertz
from musx.ran import odds, between, pick
from musx.tools import  setmidiplayer, playfile
from musx.midi import MidiNote, MidiSeq, MidiFile


def fm_chords(q, reps, cen, cm1, cm2, in1, in2, rhy):
    """
    Generates a series of FM chords with random fluctuations in its
    C/M ratios and indexes to yield variations of chordal notes.
    """
    for _ in reps:
        spec = fmspectrum(hertz(cen), between(cm1, cm2), between(in1, in2)) 
        for k in spec.keynums(minkey=48, maxkey=72):
            m = MidiNote(time=q.now, dur=rhy, key=k, amp=.5)
            q.out.addevent(m)
    yield rhy


contour = keynum("a4 g f e a4 b c d gs b c5 ef fs g a5 bf g f e a5 b c d \
                  gs3 f e cs c bf5 gs5 as3 cs5 e6 f4 gs5 d6 e f g c5 b a \
                  g bf c5 cs e4 f gs d4 c b a4 e5 f g a5")


def fm_improv(q, line, beat):
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
        print("melody:" if ismel else "chord:", "time=", q.now, "dur=", rhy, "keys=", keys)
        for i, k in enumerate(keys):
            m = MidiNote(time=q.now + (i * sub), dur=dur, key=k, amp=amp)
            q.out.addevent(m)
        yield rhy


if __name__ == '__main__':
    # It's good practice to add any metadata such as tempo, midi instrument
    # assignments, micro tuning, etc. to track 0 in your midi file.
    t0 = MidiSeq.metaseq()
    # Track 1 will hold the composition.
    t1 = MidiSeq()
    # Create a scheduler and give it t1 as its output object.
    q = Scheduler(t1)
    # Start our composer in the scheduler, this creates the composition.

    # q.compose(fm_chords(q, 12, 60, 1.0, 2.0, 2.0, 4.0, .8))
    q.compose(fm_improv(q, contour, 1))

    # Write a midi file with our track data.
    f = MidiFile("fm.mid", [t0, t1]).write()
    # To automatially play demos use setmidiplayer() to assign a shell
    # command that will play midi files on your computer. Example:
    #   setmidiplayer("fluidsynth -iq -g1 /usr/local/sf/MuseScore_General.sf2")
    print(f"Wrote '{f.pathname}'.")
    playfile(f.pathname)

###############################################################################
"""
A la maniere de 'continuum' (Gyorgi Ligeti).  

If you have matplotlib installed it will also show you the envelopes it used
as the random number sieve to generate the output midi file.

To run this script cd to the parent directory of demos/ and do:
```bash
python3 -m demos.continuum
```
"""


import random
from musx.scheduler import Scheduler
from musx.generators import jumble, choose
from musx.tools import setmidiplayer, playfile
from musx.scales import scale
from musx.midi import MidiNote, MidiSeq, MidiFile
from musx.midi.gm import Harpsichord


def register (q, rhy, dur, low, high, amp):
    """
    Generates a chromatic scale betwen low and high choosing notes from the
    scale in random.
    """ 
    pat = jumble(scale(low, high-low+1, 1))
    while q.elapsed < dur:
        keyn = next(pat)
        midi = MidiNote(time=q.now, dur=rhy, key=keyn, amp=amp)
        q.out.addevent(midi)
        yield rhy

def continuum (q, rhy, minkeys, maxkeys, seclens):
    """
    Calls register() to create the next section's material and then
    waits until the section is over before creating another section.
    """
    # random pattern of section lengths.
    pat = choose(seclens)
    # iterate all the min and max key numbers 
    for low, high in zip(minkeys, maxkeys):
        # get the section's duration
        secdur = next(pat)
        # sprout the next section
        q.compose(register(q, rhy, secdur, low, high, .4))
        # wait till end of section
        yield secdur


if __name__ == '__main__':
    # It's good practice to add any metadata such as tempo, midi instrument
    # assignments, micro tuning, etc. to track 0 in your midi file.
    t0 = MidiSeq.metaseq(ins={0: Harpsichord})
    # Track 1 will hold the composition.
    t1 = MidiSeq()
    # Create a scheduler and give it t1 as its output object.
    q = Scheduler(t1)
    # Lower bound on keynum choices
    minkeys = [60, 59, 58, 57, 56, 55, 54, 53, 52,
                53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68,
                69, 70, 71, 72, 73, 74, 75, 76, 77, 78,
                79, 80, 82, 83, 84, 85, 86, 87, 88, 89, 89]
    # Upper bound on keynum choices
    maxkeys = [62, 63, 64, 65, 66, 67, 68, 69, 70, 
                70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70,
                71, 72, 73, 74, 76, 79, 83, 86, 88, 89,
                89, 89, 89, 89, 89, 89, 89, 89, 89, 89, 89]
    # Length of sections
    seclens = [.5, 1, 1.5, 2, 2.5]
    # Speed of rhythm
    rate = .075
    # Start our composer in the scheduler, this creates the composition.
    q.compose(continuum(q, rate, minkeys, maxkeys, seclens))
    # Write a midi file with our track data.
    f = MidiFile("continuum.mid", [t0, t1]).write()
    # To automatially play demos use setmidiplayer() to assign a shell
    # command that will play midi files on your computer. Example:
    #   setmidiplayer("fluidsynth -iq -g1 /usr/local/sf/MuseScore_General.sf2")
    print(f"Wrote '{f.pathname}'.")
    playfile(f.pathname)

    # Plot the keynum range of the composition if matplotlib is installed.
    try:
        import matplotlib.pyplot as plt
    except:
        print("Sorry, can't show you the envelopes because matplotlib is not installed.")
    else:
        p1x,p1y = [x for x in range(len(minkeys))], [y for y in minkeys]
        plt.plot(p1x, p1y)
        p2x,p2y = [x for x in range(len(maxkeys))], [y for y in maxkeys]
        plt.plot(p2x, p2y)
        plt.show()

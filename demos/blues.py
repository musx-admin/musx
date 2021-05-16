################################################################################
"""
blues.py generates a blusey piece using the `spray()` generator in paint.py.
Composer: Mike Purfield

To run this script cd to the parent directory of demos/ and do:
```bash
python3 -m demos.blues
```
"""


if __name__ == '__main__':

    from musx.midi import MidiSeq, MidiFile
    from musx.ran import pick
    from musx.tools import playfile, setmidiplayer
    from musx.scheduler import Scheduler
    from .paint import spray
    
    # The blues scale.
    blues = [0, 3, 5, 6, 7, 10, 12]
    # It's good practice to add any metadata such as tempo, midi instrument
    # assignments, micro tuning, etc. to track 0 in your midi file.
    t0 = MidiSeq.metaseq()
    # Track 1 will hold the composition.
    t1 = MidiSeq()
    # Create a scheduler and give it t1 as its output object.
    q = Scheduler(t1)
    # The sections of the piece
    s1=spray(q, dur=.2, rhy=.2, band=[0, 3, 5], key=30, amp=0.35, end=36)
    s2=spray(q, dur=.2, rhy=[-.2, -.4, .2, .2], band=[3, 7, 6], key=pick(30, 42), amp=0.5, end=25)
    s3=spray(q, dur=.2, rhy=[-.2, .2, .2], band=blues, key=pick(42, 54), chan=2, end=20)
    s4=spray(q, dur=.2, rhy=[-.6, .4, .4], band=blues, key=66, amp=0.4, end=15)
    s5=spray(q, dur=.2, rhy=.2, band=[0, 3, 5], key=30, amp=0.5, end=10)
    s6=spray(q, dur=.2, rhy=[-.2, -.4, .2, .2], band=[3, 7, 6], key=pick(30, 42), amp=0.8, end=10)
    s7=spray(q, dur=.2, rhy=[-.2, .2, .2], band=blues, key=pick(42, 54), chan=2, end=10)
    s8=spray(q, dur=.2, rhy=[-.6, .4, .4], band=blues, key=66, amp=0.6, end=10)
    s9=spray(q, dur=.2, rhy=.2, band=blues, key=66, amp=0.4, end=6)
    # Start our composer in the scheduler, this creates the composition.
    q.compose([[0,s1], [5, s2], [10, s3], [15, s4], [37, s5], [37, s6], [37, s7], [37,s8], [47,s9]])
    # Write a midi file with our track data.
    f = MidiFile("blues.mid", [t0, t1]).write()
    # To automatially play demos use setmidiplayer() to assign a shell
    # command that will play midi files on your computer. Example:
    #   setmidiplayer("fluidsynth -iq -g1 /usr/local/sf/MuseScore_General.sf2")
    print(f"Wrote '{f.pathname}'.")
    playfile(f.pathname)





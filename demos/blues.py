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

    from musx import Score, MidiSeq, MidiFile, pick
    from .paint import spray
    
    # The blues scale.
    blues = [0, 3, 5, 6, 7, 10, 12]
    # It's good practice to add any metadata such as tempo, midi instrument
    # assignments, micro tuning, etc. to track 0 in your midi file.
    tr0 = MidiSeq.metaseq()
    # Track 1 will hold the composition.
    tr1 = MidiSeq()
    # Create a score and give it tr1 to hold the score event data.
    sco = Score(out=tr1)
    # The sections of the piece
    s1=spray(sco, dur=.2, rhy=.2, band=[0, 3, 5], key=30, amp=0.35, end=36)
    s2=spray(sco, dur=.2, rhy=[-.2, -.4, .2, .2], band=[3, 7, 6], key=pick(30, 42), amp=0.5, end=25)
    s3=spray(sco, dur=.2, rhy=[-.2, .2, .2], band=blues, key=pick(42, 54), chan=2, end=20)
    s4=spray(sco, dur=.2, rhy=[-.6, .4, .4], band=blues, key=66, amp=0.4, end=15)
    s5=spray(sco, dur=.2, rhy=.2, band=[0, 3, 5], key=30, amp=0.5, end=10)
    s6=spray(sco, dur=.2, rhy=[-.2, -.4, .2, .2], band=[3, 7, 6], key=pick(30, 42), amp=0.8, end=10)
    s7=spray(sco, dur=.2, rhy=[-.2, .2, .2], band=blues, key=pick(42, 54), chan=2, end=10)
    s8=spray(sco, dur=.2, rhy=[-.6, .4, .4], band=blues, key=66, amp=0.6, end=10)
    s9=spray(sco, dur=.2, rhy=.2, band=blues, key=66, amp=0.4, end=6)
    # Create the composition.
    sco.compose([[0,s1], [5, s2], [10, s3], [15, s4], [37, s5], [37, s6], [37, s7], [37,s8], [47,s9]])
    # Write the seqs to a midi file in the current directory.
    file = MidiFile("blues.mid", [tr0, tr1]).write()
    print(f"Wrote '{file.pathname}'.")
    
    # To automatially play demos use setmidiplayer() and playfile().
    # Example:
    #     setmidiplayer("fluidsynth -iq -g1 /usr/local/sf/MuseScore_General.sf2")
    #     playfile(file.pathname)





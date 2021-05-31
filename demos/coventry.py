################################################################################
"""
This demo uses the rotation() pattern to produce a change-ringing pattern called
Plain Hunt Minimus for 10 bells from the Cathedral Church of St. Michael in
Coventry, England. See: www.hibberts.co.uk/collect/coventry_old.htm for more
information.

To run this script cd to the parent directory of demos/ and do:
```bash
python3 -m demos.coventry
```
"""


from musx import Note, keynum, allrotations


coventry_bells = {
#         hum    prime  tierce quint  nominal superq  octnom
    'a': [377,   620.5, 825.5, 1162,  1376,   2032.5, 2753.5],
    'b': [345.5, 577,   750.5, 1064,  1244,   1831,   2483],
    'c': [296,   499,   665,   874,   1114,   1647,   2241],
    'd': [285.5, 483,   626,   855.5, 1044,   1546.5, 2119],
    'e': [261,   432,   564,   760.5, 928,    1366,   1858],
    'f': [234.5, 410,   514,   672,   842,    1239,   1697],
    'g': [201,   360,   444,   598,   740,    1103,   1517],
    'h': [186,   365,   427,   552.5, 695.5,  1025.5, 1404.5],
    'i': [175,   304,   376,   514.5, 616,    908,    1243],
    'j': [159,   283.5, 343,   453.5, 558,    823,    1126]
}
"""
Conventry had 10 bells, represented here as letters 'a' to 'j'
with 'a' being the highest bell.  Rows are bell harmonics,
with the 'prime' harmonic being the main tone in each bell.
"""
    
# convert bell hertz values into equivalent floating point key numbers
_conventry_fkeys = {b: [keynum(h, filt=None) for h in l]
                       for b,l in coventry_bells.items()}


def playbells(score, peal, bells, rhy, dur, amp):
    # each bell represented by its 'prime' harmonic.
    primes = {k: bells[k][1] for k in bells.keys()}
    # play the peal (the ordered list of bells to play)
    for b in peal:
        # emphasize top and bottom bell by playing all its harmonics.
        if b in ['a','j']: 
            # keynums are quantized to 25 cents
            for k in [x for x in bells[b]]:
                m = Note(time=score.now, duration=dur*4, pitch=k, amplitude=amp, microdivs=4)            
                score.add(m)
        else: # else play single 'prime' note 
            k = primes[b]
            m = Note(time=score.now, duration=dur, pitch=k, amplitude=amp, microdivs=4)
            score.add(m)
        yield rhy


if __name__ == '__main__':
    from musx.midi.gm import Celesta, Glockenspiel, MusicBox, Vibraphone,\
        Marimba, Xylophone, TubularBells
    from musx import Seq, MidiFile
    from musx import Score

    # Plain Hunt change ringing for 10 bells.
    items = ['a','b','c','d','e','f','g','h','i','j']
    rules = [[0, 2, 1], [1, 2, 1]]
    items = allrotations(items, rules, False, True)
    # It's good practice to add any metadata such as tempo, midi instrument
    # assignments, micro tuning, etc. to track 0 in your midi file.
    track0 = Seq.metaseq(ins={0: TubularBells, 1: TubularBells, 
                               2: TubularBells, 3: TubularBells}, microdivs=4)
    # Track 1 will hold the composition.
    track1 = Seq()
    # Create a score and give it tr1 to hold the score event data.
    sco = Score(out=track1)
    # Create the composition.
    sco.compose(playbells(sco, items, _conventry_fkeys, .25, .6, .8))
    # Write the tracks to a midi file in the current directory.
    file = MidiFile("coventry.mid", [track0, track1]).write()
    print(f"Wrote '{file.pathname}'.")

    # To automatially play demos use setmidiplayer() and playfile().
    # Example:
    #     setmidiplayer("fluidsynth -iq -g1 /usr/local/sf/MuseScore_General.sf2")
    #     playfile(file.pathname)

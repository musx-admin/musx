################################################################################
"""
This demo uses a second order markov generator to compose music in the style of
Stephen Foster, a famous American song writer of the 19th century (1826–1864).
The markov transition table is taken from Chapter 8 of "Computer Music" by
Dodge/Jerse. Sounds best with slow strings.

To run this script cd to the parent directory of demos/ and do:
```bash
python3 -m demos.foster
```
"""


from musx import Score, Note, Seq, MidiFile, keynum, jumble, cycle, choose, markov, intempo
from musx.midi.gm import StringEnsemble1

def pattern_stephen_foster():
    """
    A second order markov process that generates a melody in the style
    of Stephen Foster (american song writer) 1826–1864. Taken from
    "Computer Music" by Dodge, Jerse.
    """
    return markov({
        ('B3', 'D4'): ['D4'],
        ('C#4','D4'): [['D4', .3125], ['E4', .3125], ['A4', .3125]],
        ('D4', 'D4'): [['C#4', .125], ['D4', .125], ['E4', .5625], ['F#4', .125], ['A4', .0625]],
        ('E4', 'D4'): [['B3', .0625], ['D4', .0625], ['E4', .25], ['F#4', .3125], ['A4', .0625], ['C#5', .0625], ['D5', .1875]],
        ('F#4','D4'): [['E4', .75], ['F#4', .1875], ['G4', .0625]],
        ('A4', 'D4'): [['E4', .6875], ['F#4', .3125]],
        ('B4', 'D4'): ['D4'],
        ('D4', 'B3'): ['D4'],
        ('D4', 'C#4'): ['D4'],
        ('E4', 'C#4'): ['D4'],
        ('D4', 'E4'): [['D4', .1875], ['E4', .25], ['F#4', .5], ['A4', .0625]],
        ('E4', 'E4'): [['C#4', .0625], ['D4', .75], ['E4', .0625], ['F#4', .125]],
        ('F#4','E4'): [['C#4', .125], ['D4', .4375], ['E4', .1875], ['F#4', .125], ['A4', .0625], ['D5', .0625]],
        ('D4', 'F#4'): [['E4', .4375], ['F#4', .1875], ['G4', .125], ['A4', .25]],
        ('E4', 'F#4'): [['D4', .0625], ['E4', .1875], ['F#4', .3125], ['G4', .25], ['A4', .0625], ['B4', .0625]], 
        ('F#4','F#4'): [['D4', .1875], ['E4', .25], ['F#4', .3125], ['G4', .125], ['A4', .0625]],
        ('G4', 'F#4'): [['E4', .5], ['G4', .5]],
        ('A4', 'F#4'): [['D4', .3125], ['E4', .25], ['F#4', .1875], ['G4', .0625], ['A4', .125], ['B4', .0625]],
        ('B4', 'F#4'): [['E4', .6875], ['F#4', .3125]],
        ('D4', 'G4'): [['F#4', .6875], ['B4', .3125]],
        ('F#4','G4'): [['F#4', .25], ['G4', .1875], ['A4', .3125], ['B4', .1875]],
        ('G4', 'G4'): [['G4', .5], ['A4', .5]],
        ('A4', 'G4'): ['F#4'],
        ('B4', 'G4'): ['B4'],
        ('A4', 'G#4'): ['A4'],
        ('D4', 'A4'): [['F#4', .25], ['A4', .75]],
        ('E4', 'A4'): [['A4', .8125], ['B4', .1875]],
        ('F#4','A4'): [['F#4', .125], ['A4', .625], ['B4', .1875], ['D5', .0625]],
        ('G4', 'A4'): [['D4', .125], ['A4', .625], ['D5', .25]],
        ('G#4','A4'): ['A4'],
        ('A4', 'A4'): [['F#4', .25], ['G4', .0625], ['G#4', .0625], ['A4', .3125], ['B4', .3125]], 
        ('B4', 'A4'): [['D4', .0625], ['F#4', .5625], ['G4', .0625], ['A4', .125], ['B4', .0625], ['D5', .125]],
        ('D5', 'A4'): [['F#4', .875], ['A4', .125]],
        ('E5', 'A4'): ['A4'],
        ('F#4','B4'): ['A4'],
        ('G4', 'B4'): ['A4'],
        ('A4', 'B4'): [['D4', .0625], ['F#4', .0625], ['A4', .75], ['B4', .0625], ['B4', .0625]],
        ('B4', 'B4'): [['F#4', .125], ['A4', .75], ['D5', .125]],
        ('C#5','B4'): ['A4'],
        ('D5', 'B4'): [['G4', .0625], ['A4', .3125], ['B4', .3125], ['D5', .25]],
        ('D4', 'C#5'): ['D5'],
        ('D5', 'C#5'): [['B4', .75], ['D5', .25]], 
        ('E5', 'C#5'): ['D5'],
        ('D4', 'D5'): [['A4', .125], ['B4', .6875], ['C#5', .1875]],
        ('E4', 'D5'): ['C#5'],
        ('A4', 'D5'): [['A4', .3125], ['B4', .3125], ['C#5', .1875], ['D5', .125]],
        ('B4', 'D5'): [['A4', .5625], ['B4', .125], ['C#5', .3125]],
        ('C#5','D5'): [['B4', .3125], ['E5', .625]],
        ('D5', 'D5'): ['B4'],
        ('D5', 'E5'): [['A4', .3125], ['C#5', .6875]]
        })


def composer_stephen_foster(sco, num, shift=0, chan=0):
    # A second-order markov process generates the melody.
    melody = pattern_stephen_foster()
    # randomly select rhythmic patterns characterisitic of Foster's style
    rhythms = choose([[2, 2], [1, 1, 1, 1], [2, 1, 1], [1, 1, 2], [1, 2, 1], [4]],
                        [.375, .125, .125, .125 ,.25, .125])
    for _ in range(num):
        n=0
        for r in next(rhythms):
            k = keynum(next(melody)) + (shift*12)
            r = intempo(r, 200)
            m = Note(time=sco.now+n, dur=r, key=k, amp=.5, chan=chan)
            sco.add(m)
            n += r
        yield n


if __name__ == '__main__':
    # It's good practice to add any metadata such as tempo, midi instrument
    # assignments, micro tuning, etc. to track 0 in your midi file.
    tr0 = Seq.metaseq(ins={0: StringEnsemble1})
    # Track 1 will hold the composition.
    tr1 = Seq()
    # Create a score and give it tr1 to hold the score event data.
    sco = Score(out=tr1)
    # Compose a 4 voice texture with these octave transposition factors.
    voices = [-1, 0, 1, 2]
    composers = [composer_stephen_foster(sco, 25, t) for t in voices]
    # Create the composition.
    sco.compose(composers)
    # Write the seqs to a midi file in the current directory.
    file = MidiFile("foster.mid", [tr0, tr1]).write()
    print(f"Wrote '{file.pathname}'.")
    
    # To automatially play demos use setmidiplayer() and playfile().
    # Example:
    #     setmidiplayer("fluidsynth -iq -g1 /usr/local/sf/MuseScore_General.sf2")
    #     playfile(file.pathname)


   

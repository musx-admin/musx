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


from musx.midi import MidiNote, MidiSeq, MidiFile
from musx.midi.gm import StringEnsemble1
from musx.scheduler import Scheduler
from musx.scales import keynum
from musx.generators import jumble, cycle, choose, markov
from musx.tools import setmidiplayer, playfile
from musx.rhythm import intempo


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


def composer_stephen_foster(q, num, shift=0, chan=0):
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
            m = MidiNote(time=q.now+n, dur=r, key=k, amp=.5, chan=chan)
            q.out.addevent(m)
            n += r
        yield n


if __name__ == '__main__':
    # It's good practice to add any metadata such as tempo, midi instrument
    # assignments, micro tuning, etc. to track 0 in your midi file.
    t0 = MidiSeq.metaseq(ins={0: StringEnsemble1})
    # Track 1 will hold the composition.
    t1 = MidiSeq()
    # Create a scheduler and give it t1 as its output object.
    q = Scheduler(t1)
    # Compose a 4 voice texture with these octave transposition factors.
    voices = [-1, 0, 1, 2]
    composers = [composer_stephen_foster(q, 25, t) for t in voices]
    # Start our composers in the scheduler, this creates the composition.
    q.compose(composers)
    # Write a midi file with our track data.
    f = MidiFile("foster.mid", [t0, t1]).write()
    # To automatially play demos use setmidiplayer() to assign a shell
    # command that will play midi files on your computer. Example:
    #   setmidiplayer("fluidsynth -iq -g1 /usr/local/sf/MuseScore_General.sf2")
    print(f"Wrote '{f.pathname}'.")
    playfile(f.pathname)


   

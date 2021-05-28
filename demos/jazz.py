################################################################################
"""
This tutorial presents an implementation of an simple automatic jazz
program. The code is derived from a program originally written by
Erik Flister at CCRMA, Stanford University, as a project for his
undergraduate computer music class. His original program has been
simplified and adapted here to work with General MIDI
instruments. Flister's improviser generates music for a jazz trio
(piano, acoustic bass and percussion).

To run this script cd to the parent directory of demos/ and do:
```bash
python3 -m demos.jazz
```
"""


import types
from musx import Score, Note, MidiSeq, MidiFile, keynum, cycle, \
    choose, jumble, intempo, odds, pick, between
from musx.midi.gm import AcousticGrandPiano, AcousticBass


jazz_scale = [0, 2, 3, 5, 7, 9, 10, 12, 14]
"""The scale used by the improvisor."""


jazz_changes = keynum('bf3 ef4 bf3 bf ef4 ef bf3 bf f4 ef bf3 bf')
"""The chord changes for the piano and bass parts."""


jazz_tempo = 120
"""The tempo of the compostion."""


def jazz_high_hat(sco, tmpo, ampl):
    """
    Plays the High Hat on the second and fourth quarter of every measure and
    rests on the first and third beats. Each sound lasts for the duration one
    triplet eighth note i.e. 1/3 of a beat.
    """
    rhy = intempo(1, tmpo)
    dur = intempo(1/3, tmpo)
    amp = .5
    pat = cycle(['r', 42, 'r', 42]) # 'r' is rest
    for _ in range(4):
        x = next(pat)
        if x != 'r':
            m = Note(time=sco.now, dur=dur, key=x, amp=amp * ampl, chan=9)
            sco.add(m)
        yield rhy


def jazz_drums(sco, tmpo, ampl):
    """
    Randomly selects between playing the snare, the bass drum or resting one
    quarter of the time. One tenth of the time it produces a very loud tone.
    """
    elec_snare = 40
    bass_drum = 35
    knums = choose(['r', elec_snare, bass_drum], [.25, 1, 1])
    rhys = cycle([2/3, 1/3])
    amps = choose([.7, .95], [1, .1])
    for _ in range(8):
        k = next(knums)
        a = next(amps)
        r = intempo(next(rhys), tmpo)
        if k != 'r':
            m = Note(time=sco.now, dur=r, key=k, amp=a * ampl, chan=9)
            sco.add(m)
        yield r


def jazz_cymbals(sco, tmpo, ampl):
    """
    The cymbals process performs a constant stream of triplet eighths in
    which the ride1 cymbal is played on the beginning of every quarter
    note. The second and third triplets of each beat are either rests or
    a random choice between ride1, ride2 or a rest.  This is the beat
    map for a measure of the process, where '1' means the ride cymbal 1 is
    played, '-' means a rest, and 'x' means a random choice between ride1,
    ride2 or a rest:

    ```text
    Triplet 8th: 1  2  3    4  5  6    7  8  9   10 11 12
    Cymbals:     1  -  x    1  -  1    1  x  x    1  x  1 
    ```
    """
    ride1 = 51
    ride2 = 59
    rhy = intempo(1/3, tmpo)
    amps = cycle([.6, .5, .9, .7, .5, 1, .6, .5, .9, .7, .5, 1])

    def subpat(wt):
        r1 = choose([ride1, 'r'], [1, wt])
        r2 = choose([ride2, 'r'], [1, wt])
        return choose([r1, r2], [1.5, 1])

    # the events that happen on each triplet of the measure
    meas = {0: ride1,  1: 'r',        2: subpat(5),
            3: ride1,  4: 'r',        5: ride1,
            6: ride1,  7: subpat(7),  8: subpat(7),
            9: ride1, 10: subpat(3), 11: ride1}
    for b in meas:
        k = meas[b]
        if k != 'r':
            if type(k) is not int: # k is a subpattern
                k = next(next(k))
            if k != 'r':
                a = next(amps)
                m = Note(time=sco.now, dur=rhy, key=k, amp=a*ampl, chan=9)
                sco.add(m)
        yield rhy


def jazz_piano(sco, on, tmpo, ampl):
    """
    The jazz piano improvises jazz chords based on a pattern of root
    changes and a scale pattern that is transposed to each root. The
    piano randomly choose between playing triplet eighths or straight
    eights for a given measure.
    """
    reps = odds(.65, 8, 12)
    scal = jumble(jazz_scale)
    rhys = cycle([2/3, 1/3] if reps == 8 else [1/3])
    for _ in range(reps):
        r = intempo(next(rhys), tmpo)
        l = [] if odds(2/5) else [next(scal) for _ in range(between(1,9))]
        for k in l:
            a = pick(.4, .5, .6, .7, .8)
            m = Note(time=sco.now, dur=r, key=on+k, amp=a, chan=0)
            sco.add(m)
        yield r


def jazz_bass(sco, on, tmpo, ampl):
    """
    The bass part plays a melodic line built out of tones from the jazz-scale's
    tonic seventh chord alternating with color tones outside the tonic chord.
    The bass plays a series of 12 triplets per measure, on each triplet only one of
    the two sets is possible. On all but the first triplet a rest is also possible.
    """
    # 5 possible patterns for triplets 1-4
    a = choose(['trrc', 'trrr', 'trtc', 'tctc', 'tctr'], [1.0, .25, .22, .065, .014])
    # 5 possible patterns for 5-7
    b = choose(['rrt', 'rrr', 'rct', 'tct', 'tcr'], [1.0, .25, .22, .038, .007])
    # 5 possible patterns for 8-10
    c = choose(['rrc', 'rtc', 'rrr', 'ctc', 'ctr'], [1.0, .415, .25, .11, .018])
    # two possible values for 11
    d = choose(['r', 't'], [1, .25])
    # two possible values for 12
    e = choose(['r', 'c'], [1, .25])
    # the measure map
    meas = next(a) + next(b) + next(c) + next(d) + next(e)

    rhy = intempo(1/3, tmpo)
    tonics = choose([jazz_scale[i] for i in [0, 2, 4, 6, 7]])
    colors = choose([jazz_scale[i] for i in [1, 3, 5, 6, 8]])
    amps = cycle([.5, .4, 1.0, .9, .4, .9, .5, .4, 1.0, .9, .5, .9])
    durs = cycle([2/3, 1/3, 1/3])

    for x in meas:
        k = -1
        if x == 't':
            k = next(tonics)
        elif x == 'c':
            k = next(colors)
        if k > -1:
            a = next(amps)
            d = next(durs)
            m = Note(time=sco.now, dur=d, key=on+k, amp=ampl*a, chan=1)
            sco.add(m)
        yield rhy


def jazz_combo(sco, measures, tempo):
    """
    The conductor process adds combo parts for each meaure to the schedule 
    generate sound. By adding parts at each measure the conductor could make
    changes to the overall texture, amplitude etc, as the pieces progresses.
    """ 
    roots = cycle(jazz_changes)
    ampl = .9
    for meas in range(measures):
        root = next(roots)
        if  0 == meas % 12:
           ampl = between(.5, 1)
        sco.compose(jazz_piano(sco, root, tempo, ampl))
        sco.compose(jazz_cymbals(sco, tempo, ampl))
        sco.compose(jazz_high_hat(sco, tempo, ampl))
        sco.compose(jazz_drums(sco, tempo, ampl))
        sco.compose(jazz_bass(sco, root-12, tempo, ampl))
        yield intempo(4,tempo)
    

if __name__ == '__main__':
    # It's good practice to add any metadata such as tempo, midi instrument
    # assignments, micro tuning, etc. to track 0 in your midi file.
    tr0 = MidiSeq.metaseq(ins={0: AcousticGrandPiano, 1: AcousticBass})
    # Track 1 will hold the composition.
    tr1 = MidiSeq()
    # Create a score and give it tr1 to hold the score event data.
    sco = Score(out=tr1)

    # c=[]
    # for t in range(0, 15, 2): # t -> 0 2 4 6 8 10 12 14
    #     c += [[t, jazz_high_hat(q, 120, .9)], 
    #           [t, jazz_drums(q, 120, .9)],
    #           [t, jazz_cymbals(q, 120, .9)],
    #           [t, jazz_piano(q, 58, 120, .9)],
    #           [t, jazz_bass(q, 46, 120, .9)]
    #           ]

    # Create the composition.
    sco.compose(jazz_combo(sco, 48, 120))
    # Write the seqs to a midi file in the current directory.
    file = MidiFile("jazz.mid", [tr0, tr1]).write()
    print(f"Wrote '{file.pathname}'.")
    
    # To automatially play demos use setmidiplayer() and playfile().
    # Example:
    #     setmidiplayer("fluidsynth -iq -g1 /usr/local/sf/MuseScore_General.sf2")
    #     playfile(file.pathname)

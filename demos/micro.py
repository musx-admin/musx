################################################################################
"""
Some examples of generating microtonal music with midi.

musx implements 'channel tuning', a system that quantizes midi frequency and
channel space into 'divisions per semitone' and routes midi notes with microtonal 
floating point key numbers to the appropriately tuned channel in the midi file.
Channel tuning claims channels for microtuning at the expense of the number of
channels that can be assigned different instruments.  For example, a tuning value
of 1 means standard semitonal tuning so all 16 channels are available for midi 
instrument assignment. But a division of 2 (two divisions per semitone), which
performs quarter-tone tuning, will claim successive pairs of channels and 
quantizes them to 50 cent steps, so channel 0 is unadjusted and channel 1 is
tuned 50 cents up.  This means a key number 60.20 would be sent to channel
0 and a keynum 60.70 would be sent to channel 1, a quarter tone above channel 0.
The maximum tuning value of 16 provides a tuning quantization step size of 6.25
cents spread out over all 16 channels, which means that one instrument will 
claim all 16 channels. Note: If your synth hardwires channel 9 to a drum map
then for microtunings 9 thru 16 you will hear a percussion sound instead of a
note whenever channel 9 is selected.

For a Note to produce a microtonal sound three conditions must be met:

* The Note's key number must be a floating point value with a fractional
  value greater than 0.
* The Note's 'tuning' parameter must be greater than 1.
* Track 0 (the 'metatrack' of the midi file) must be quantized to the same
  divisions per semitone as the 'tuning' parameter. See: MidiSeq.metatrack().

See also: demos fm.py, rm.py, gamelan.py, `MidiSeq.metatrack()`, `Note()`.

To run this script cd to the parent directory of demos/ and do:
```bash
python3 -m demos.micro
```
"""


from musx import Score, Note, MidiSeq, MidiFile, MidiEvent, odds, divide, \
     deltas, rescale, scale, jumble, temper
from musx.midi.gm import TubularBells, Dulcimer, Flute, Vibraphone, Marimba


def pitchbends(sco, tuning):
    """
    Called by playmicrosteps() to outputs pitchbends to establish a microtuning.

    Parameters
    ----------
    sco : Score
        The musical score to add events to.
    tuning : int
        A value 1 to 16 specificing the divisions per semitone of the tuning.
    """
    values = MidiSeq.channeltuning(tuning)
    for chan,value in enumerate(values):
        # calculate the pitch bend value
        bend = round(rescale(value, -2,  2,  0, 16383))
        sco.add(MidiEvent.pitch_bend(chan, bend, time=sco.now))
    yield -1

    
def microtones(sco, tuning, dur):
    """
    Called by playmicrosteps() to play individual tuning steps over dur seconds.
    
    Parameters
    ----------
    sco : Score
        The musical score to add events to.
    tuning : int
        A value 1 to 16 specificing the divisions per semitone of the tuning.
    dur : number
        The duration over which the tuning steps will be performed.
    """
    rhy = dur*(1/(tuning*12))
    key = 60
    for _ in range(tuning*12+1):
        #print('pre tuning: key',key,end="\t")
        m = Note(time=sco.now, dur=rhy, key=key, tuning=tuning)
        #print("post tuning: key", m.key, "chan", m.chan)
        sco.add(m)
        key += 1/tuning
        yield rhy


def playmicrosteps():
    """
    Performs the microsteps of all semitonal division from 1 (semitones)
    upto 16 divisions per semitone. NOTE: Depending on your midi synth if
    the tuning spans channel 9 you may hear a drum map tone instead of a
    micotonal pitch!
    """
    # It's good practice to add any metadata such as tempo, midi instrument
    # assignments, micro tuning, etc. to track 0 in your midi file.
    tr0 = MidiSeq.metaseq()
    # Track 1 will hold the composition.
    tr1 = MidiSeq()
    # Create a score and give it tr1 to hold the score event data.
    sco = Score(out=tr1)
    # Create composers for each semitonal division from 1 to 16
    composers = []
    now = 0
    dur = 6
    for div in range(1, 16):
        # for each division the first composer outputs pitchbends,
        # and the second outputs the microtonal pitches.
        composers += [[now, pitchbends(sco,div)], [now, microtones(sco,div,dur)]]
        now += dur+1
    # Create the composition.
    sco.compose(composers)
    # Write the tracks to a midi file in the current directory.
    file = MidiFile("micro.mid", [tr0, tr1]).write()
    print(f"Wrote '{file.pathname}'.")
    playfile(f.pathname)

    # To automatially play demos use setmidiplayer() and playfile().
    # Example:
    #     setmidiplayer("fluidsynth -iq -g1 /usr/local/sf/MuseScore_General.sf2")
    #     playfile(file.pathname)

def playmicropentatonic():
    """
    Plays a lovely microtonal pentatonic scale consisting of the prime
    numbered harmonics in the 5th octave of the harmonic series:

    Harmonic number: 17   19   23   29   31   34
    Nearest pitch:   C#   D#   F#   A#   B    C#
    Cent adjustment: +5   -3   +28  +29  +45  +5
    """
    # the harmonic numbers
    harms = [17, 19, 23, 29, 31, 34]
    # convert into ascending intervals of a one octave pentatonic scale
    penta = deltas(temper(divide(harms, 17)))

    #penta = scale(5*4, 60, deltas(semis))

    # It's good practice to add any metadata such as tempo, midi instrument
    # assignments, micro tuning, etc. to track 0 in your midi file.
    tr0 = MidiSeq.metaseq(ins={i: Vibraphone for i in range(16)}, tuning=8)
    # Track 1 will hold the composition.
    tr1 = MidiSeq()
    # Create a score and give it tr1 to hold the score event data.
    sco = Score(out=tr1)

    def playpenta (sco, num, dur, amp, keys):
        pat = jumble(keys)
        for _ in range(num):
            k = next(pat)
            m = Note(time=sco.now, dur=dur*2, key=k, amp=amp, tuning=8)
            sco.add(m)
            yield odds(.2 , 0, dur)

    top = playpenta(sco, 90, .3, .4, scale(72+12, 10, *penta))
    bot = playpenta(sco, 45, .6, .5, scale(48, 10, *penta))
    low = playpenta(sco, 23, 1.2, .8, scale(24, 10, *penta))
    sco.compose([top, [.3*4, bot], [.3*12, low]])
    # Write a midi file with our track data.
    file = MidiFile("micro.mid", [tr0, tr1]).write()
    print(f"Wrote '{file.pathname}'.")

    # To automatially play demos use setmidiplayer() and playfile().
    # Example:
    #     setmidiplayer("fluidsynth -iq -g1 /usr/local/sf/MuseScore_General.sf2")
    #     playfile(file.pathname)


if __name__ == '__main__':

    #playmicrosteps()
    
    playmicropentatonic()


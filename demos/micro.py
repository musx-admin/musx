################################################################################
"""
Two examples of generating microtonal music with midi.

musx implements 'channel tuning', a method that quantizes midi frequency and
channel space into 'divisions per semitone' and routes midi notes with microtonal 
floating point key numbers to an appropriately tuned channel in the midi file.
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
* Track 0 (the 'metatrack' of the midi file) must be quantized to a microtonal
division 1-16. See MidiFile.metatrack() for more information.

To run this script cd to the parent directory of demos/ and do:
```bash
python3 -m demos.micro
```
"""

from musx import Score, Note, Seq, MidiFile, MidiEvent, odds, divide, \
     deltas, rescale, scale, jumble, temper
from musx.midi.gm import Vibraphone


def play_micro_divisions(divs):
    """
    Plays one octave of microtones quantized to 1/divs semitones.

    Parameters
    ----------
    divs : int 1 to 16
        A value of 1 produces 1/1 = 1 = 100 cents (standard semitonal tuning)
        a value of 2 produces 1/2 = .5 = 50 cents (quarter tone tuning) and so on.
    """
    def playmicro(score, key, rhy, divs):
        inc = 1/divs
        for i in range(12 * divs + 1):
            note = Note(time=score.now, duration=rhy, pitch=key)
            score.add(note)
            key += inc
            yield rhy
    # divs can be a value from 1 to 16 
    track0 = MidiFile.metatrack(microdivs=divs)
    track1 = Seq()
    score = Score(out=track1)
    score.compose(playmicro(score, 60, .5, divs))
    file = MidiFile("microdivs.mid", [track0, track1]).write()
    print(f"Wrote '{file.pathname}'.") 


def play_micro_pentatonic():
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
    track0 = MidiFile.metatrack(ins={i: Vibraphone for i in range(16)}, microdivs=8)
    # Track 1 will hold the composition.
    track1 = Seq()
    # Create a score and give it tr1 to hold the score event data.
    score = Score(out=track1)

    def playpenta (score, num, dur, amp, keys):
        pat = jumble(keys)
        for _ in range(num):
            k = next(pat)
            n = Note(time=score.now, duration=dur*2, pitch=k, amplitude=amp)
            score.add(n)
            yield odds(.2 , 0, dur)

    top = playpenta(score, 90, .3, .4, scale(72+12, 10, *penta))
    bot = playpenta(score, 45, .6, .5, scale(48, 10, *penta))
    low = playpenta(score, 23, 1.2, .8, scale(24, 10, *penta))
    score.compose([top, [.3*4, bot], [.3*12, low]])
    # Write a midi file with our track data.
    file = MidiFile("micropenta.mid", [track0, track1]).write()
    print(f"Wrote '{file.pathname}'.")

    # To automatially play demos use setmidiplayer() and playfile().
    # Example:
    #     setmidiplayer("fluidsynth -iq -g1 /usr/local/sf/MuseScore_General.sf2")
    #     playfile(file.pathname)


if __name__ == '__main__':
    play_micro_divisions(2)
    play_micro_pentatonic()


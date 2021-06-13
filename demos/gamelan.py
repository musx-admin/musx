################################################################################
"""
gamelan.py generates a gamelan composition using the `brush()` and `spray()`
generators in paint.py. Composer: Ming-ching Chiu.

To run this script cd to the parent directory of demos/ and do:
```bash
python3 -m demos.gamelan
```
"""


if __name__ == '__main__':
    from musx import Score, Seq, MidiFile
    from musx.midi.gm import Vibraphone
    from musx.paint import brush, spray

    # Scale1 is a 7-tone microtonal scale that evokes the Pelog scale.
    scale1 = [0, 2.2, 3.8, 6.6, 7.1, 9.3, 10, 12, 14.4, 15.8, 18.6, 19.1]
    # Scale2 is a 5-tone pentatonic scale that evokes the Slendro scale.
    scale2 = [0, 2, 3.7, 6.9, 9.1]
    scale3 = [[0, 6.9], [2, 6.9], [3.7, 9.1], [9.1, 14], [3.7, 12]]
    melody = [[36, 43.1, 46], [42.6, 50.2], [38.2, 48, 51.8], [39.8, 46, 54.6],
              [54.6, 62.2, 66.6], [57.3, 66.6, 69.3], [58, 62.2, 67.1], 
              [36, 45.3, 48], [60, 66.6, 69.3], [46, 55.1, 60], 
              [42.6, 50.2, 57.3], [46, 55.1, 60], [57, 66.6, 69.3], 
              [57.3, 66.6, 69.3], [54.6, 62.2, 66.6]]
    # Amplitude scaler to adapt to different sound fonts. this is for fluidsynth
    def A(a): return ([s * 1.35 for s in a] if type(a) is list else a*1.5)
    # Microtonal divisions of the semitone. 2 is quartertone (50 cents) etc.
    microdivs=7
    # It's good practice to add any metadata such as tempo, midi instrument
    # assignments, micro tuning, etc. to track 0 in your midi file.
    track0 = MidiFile.metatrack(ins={i: Vibraphone for i in range(microdivs)}, microdivs=microdivs)
    # Track 1 holds the composition.
    track1 = Seq()
    # Create a score and give it tr1 to hold the score event data.
    score = Score(out=track1)
    # The sections of the piece
    s1=spray(score, pitch=48, duration=3, rhythm=[1, .5], amplitude=A([.3, .35, .4]),
                band=scale1, end=40)
    s2=spray(score, pitch=48, duration=3, rhythm=[1, .5], amplitude=A([.4, .45, .5]), 
                band=scale3, end=25)
    s3=spray(score, pitch=72, duration=3, rhythm=[.75, .25, .5], amplitude=A([.4, .3, .35]),
                band=[3.8, 7.1, [9.3, 14.4]], end=35)
    s4=spray(score, pitch=72, duration=3, rhythm=[.75, .25, .5], amplitude=A([.6, .5, .55]),
                band=[9.3, 12, 14.2, 18.6, [26.2, 30.6]], end=30)
    s5=spray(score, pitch=84,  duration=3, rhythm=[.75, .25, .5], amplitude=A([.6, .5, .55]),
                band=[3.8, 7.1, 9.3, [7.1, 12]],  end=15)
    s6=spray(score, pitch=24,  duration=5, rhythm=[1, 1, .5, 2, 2], amplitude=A(.5),
                band=scale2, end=55)

    s7=brush(score, pitch=[86.2, 93.3, 87.8, 91.1], duration=4, rhythm=[.25, .25, .5], 
                amplitude=A(.3), end=50)
    s8=brush(score, pitch=[86.2, [93.3, 98.8], 87.8, 91.1], duration=4,
                rhythm=[.25, .25, .25, .25, .5], amplitude=A(.25), end=10)
    s9=brush(score, pitch=[81.3, 74.4, 78.6, 72], duration=2, rhythm=[.5, .25, .25],
                amplitude=A(.25), end=50)
    s10=brush(score, pitch=melody, duration=8,
                 rhythm=[2, 1, 1, .5, .5, 3, 1.5, 1.5, 4, 2, 1, 1, .5, .5, 3, 1.5, 1.5, 1.5, .5, 4],
                 amplitude=A([.3, .4, .35, .35]), end=40)

    s11=spray(score, pitch=72, duration=2, rhythm=1/3, amplitude=A(.18),
                 band=[[0, 14.4], [3.8, 12], [15.8, 7.1], [2.2, 9.3], [0, 10],
                       [9.3, 2.2], [7.1, 14.4], [0, 9.3], [3.8, 12]], end=36)
    s12=spray(score, pitch=60, duration=2, rhythm=.5, amplitude=A(.25), band=scale2, end=41)
    s13=spray(score, pitch=48, duration=4, rhythm=[1, 1, 2, 1, 1, 1, 1, 1, .5, .5, 2, 1, .5, .5, 1, 1, 2, 2, .5, .5, 1, 4],
                 amplitude=A(.35), band=scale3, end=32)
    s14=brush(score, pitch=[[36, 42.6, 43.1, 48, 51.8, 57.3, 63.8, 86.4], [12, 24, 31.1, 36, 42.6]],
                 length=2, duration=8, rhythm=[4, 8], amplitude=A(.25))
    # Create the composition.
    score.compose([[0, s1], [40, s2], [10, s3], [40, s4], [50, s5], [20, s6],
          [65, s7], [80, s8], [73, s9], [79, s10],
          [121, s11], [121, s12], [129, s13], [162, s14] ] )
    # Write the tracks to a midi file in the current directory.
    file = MidiFile("gamelan.mid", [track0, track1]).write()
    print(f"Wrote '{file.pathname}'.")

    # To automatially play demos use setmidiplayer() and playfile().
    # Example:
    #     setmidiplayer("fluidsynth -iq -g1 /usr/local/sf/MuseScore_General.sf2")
    #     playfile(file.pathname)


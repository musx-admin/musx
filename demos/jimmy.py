"""
A wild ride on the drum track.
"""

from musx import MidiNote, MidiSeq, MidiFile, Score
from .paint import brush

pphase = [127, 117, 126, 117.5, 125, 119, 124.5, 119.5,
          123, 121, 122.5, 121.5, 121.5, 123, 120, 124, 
          119.5, 124.5, 118, 126, 117.5, 0.5, 116.5, 1, 
          115, 2, 114, 3, 113.5, 4, 112, 5.5, 111.5, 6.25, 
          110, 7.25, 109.25, 8, 108.25, 9, 107, 10.5, 
          106, 11.5, 105, 12.5, 104.25, 13.25, 
          103.5, 14, 102.5, 15, 101.25, 16, 100, 15.5, 
          99.5, 16.5, 98.25, 15, 97.25, 16.5, 
          96.25, 17.25, 95.25, 18, 94, 19.5, 93, 20.25, 
          92.5, 21, 91.5, 22, 90, 23, 89.5, 24, 88, 25.25,
          87.25, 26, 86, 27, 85.25, 28, 84, 29.5,
          83, 30.5, 82.25, 31, 81, 32.25, 80.25, 33, 
          79.25, 34.25, 78, 35.5, 77.25, 36, 76, 37.25, 
          75.5, 38, 74.25, 39.25, 73, 40.5, 72.5, 41, 
          71.25, 42.5, 70, 43.25, 69, 44, 68.5, 45, 
          67.5, 46, 66.25, 47, 65.5, 48, 64, 49.25, 
          63, 50, 62.5, 51, 61.25, 52, 60, 53.5, 
          59.25, 54, 58, 55.25, 57, 56.5, 0,
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

arf = [0, 3, 7, 0, 3, 7, 0, 3, 7, 0, 3, 7, 0, 3, 7, 0]

if __name__ == '__main__':
    # It's good practice to add any metadata such as tempo, midi instrument
    # assignments, micro tuning, etc. to track 0 in your midi file.
    tr0 = MidiSeq.metaseq(tuning=4)
    # Track 1 holds the composition.
    tr1 = MidiSeq()
    # Create a score and give it tr1 to hold the score event data.
    sco = Score(out=tr1)
    # Create the composition.
    sco.compose( [brush(sco, len=1000, key=pphase, rhy=1/16, dur=1, amp=0.75, chan=9, tuning=4),
                brush(sco, len=828, key=pphase, rhy=1/32, dur=7, amp=0.75, chan=1, tuning=4) ,
                brush(sco, len=1000, key=arf, rhy=1/8, dur=1, amp=1, chan=1, tuning=4) , 
                brush(sco, len=200, key=pphase, rhy=1/2, dur=7, amp=0.75, chan=1, tuning=4)])
    # Write the tracks to a midi file in the current directory.
    file = MidiFile("jimmy.mid", [tr0, tr1]).write()
    print(f"Wrote '{file.pathname}'.")

    # To automatially play demos use setmidiplayer() and playfile().
    # Example:
    #     setmidiplayer("fluidsynth -iq -g1 /usr/local/sf/MuseScore_General.sf2")
    #     playfile(file.pathname)

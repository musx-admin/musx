###############################################################################
"""
A musical hommage to the Sierpinski triangle using a recursive process to
generate a self-similar melodies based on a set of tones representing the
"sides" of a triangle.  The duration of each note is the process duration
divided by the number of intervals in the melody. Thus, the entire melody
in the next level will occupy the same mount of time as one tone in the
current level. When the process starts running it outputs each note in the
melody transposed to the current tone. If levels is greater then 1 then the
process sprouts recursive copies of itself for each note in the melody
transposed up trans intervals. The value for levels is decremented by 1,
which will cause the recursive process to stop when the value reaches 0.

To run this script cd to the parent directory of demos/ and do:
```bash
python3 -m demos.sierpinski
```
"""
import musx
import ctcsound

from musx.tools import playfile, setmidiplayer
from musx.score import Score
from musx.scales import keynum
from musx.midi import MidiNote, MidiSeq, MidiFile


def sierpinski(sco, tone, shape, trans, levels, dur, amp):
    """
    Generates a melodic shape based on successive transpositions (levels) of
    itself. 
    
    Parameters
    ----------
    sco : Score
        The musical score to add events to.
    tone : keynum
        The melodic tone on which to base the melody for the current level.
    shape : list
        A list of intervals defining the melodic shape. 
    levels : int
        The number of levels the melody should be reproduced on. 
    dur : int | float
        The duration of the process.
    amp : float
        The amplitude of the process.
    """
    num = len(shape)
    for i in shape:
        k = tone + i
        # play current tone in melody
        m = MidiNote(time=sco.now, dur=dur, key=min(k,127), amp=amp, chan=0)
        sco.add(m)
        if (levels > 1):
            # sprout melody on tone at next level
            sco.compose(sierpinski(sco, (k + trans), shape,
                        trans, levels - 1, dur / num,  amp))
        yield dur
    

if __name__ == "__main__":
    # It's good practice to add any metadata such as tempo, midi instrument
    # assignments, micro tuning, etc. to track 0 in your midi file.
    tr0 = MidiSeq.metaseq()
    # Track 1 will hold the composition.
    tr1 = MidiSeq()
    # Create a scheduler and give it t1 as its output object.
    sco = Score(out=tr1)
    # Create the composition. Specify levels and melody length with care!
    # The number of events that are generateed is exponentially related to
    # the length of the melody and the number of levels. For example the
    # first compose() generates 120 events, the second 726, and the third 2728!
    # sco.compose(sierpinski(sco, keynum('a0'), [0, 7, 5], 12, 4, 3, .5))
    # sco.compose(sierpinski(q, keynum('a0'), [0, 7, 5], 8, 5, 7, .5))
    sco.compose(sierpinski(sco, keynum('a0'), [0, -1, 2, 13], 12, 5, 24, .5))
 
    # Write the tracks to a midi file in the current directory.
    file = MidiFile("sierpinski.mid", [tr0, tr1]).write()
    print(f"Wrote '{file.pathname}'.")
    
    # To automatially play demos use setmidiplayer() and playfile().
    # Example:
    #     setmidiplayer("fluidsynth -iq -g1 /usr/local/sf/MuseScore_General.sf2")
    #     playfile(file.pathname)

    #playfile(f.pathname)
  
    
    # Now the Csound stuff.
    
    orc  = '''

sr = 48000
ksmps = 128
nchnls = 2
0dbfs = 1

gi_ampmidicurve_dynamic_range init .375
gi_ampmidicurve_exponent init 5

prealloc "Harpsichord", 20

connect "Harpsichord", "outleft", "ReverbSC", "inleft"
connect "Harpsichord", "outright", "ReverbSC", "inright"
connect "ReverbSC", "outleft", "MasterOutput", "inleft"
connect "ReverbSC", "outright", "MasterOutput", "inright"

alwayson "ReverbSC"
alwayson "MasterOutput"

gk_overlap init .0125

gk_Harpsichord_level init 0
gk_Harpsichord_pan init .3
gi_Harpsichord_release init .3
gk_Harpsichord_pick init .275
gk_Harpsichord_reflection init .75
gk_Harpsichord_pluck init .5
giharptable ftgen 0, 0, 65536, 7, -1, 1024, 1, 1024, -1
instr Harpsichord
if p3 == -1 goto indefinite
goto non_indefinite
indefinite:
  p3 = 1000000
non_indefinite:
i_instrument = p1
i_time = p2
i_duration = p3
i_midi_key = p4
i_midi_velocity = p5
k_space_front_to_back = p6
i_space_left_to_right rnd .7
i_space_left_to_right += .3
k_space_bottom_to_top = p8
i_phase = p9
i_amplitude ampmidicurve i_midi_velocity, gi_ampmidicurve_dynamic_range, gi_ampmidicurve_exponent
k_gain = ampdb(gk_Harpsichord_level)
iHz = cpsmidinn(i_midi_key)
kHz = k(iHz)
aenvelope transeg 1.0, 20.0, -10.0, 0.05
k_amplitude = 1
apluck pluck 1, kHz, iHz, 0, 1
aharp poscil 1, kHz, giharptable
aharp2 balance apluck, aharp
a_signal	= (apluck + aharp2)
i_attack = .002
i_sustain = p3
i_release = gi_Harpsichord_release
p3 = i_attack + i_sustain + i_release
a_declicking linsegr 0, i_attack, 1, i_sustain, 1, i_release, 0
a_signal = a_signal * i_amplitude * a_declicking * k_gain
#ifdef USE_SPATIALIZATION
a_spatial_reverb_send init 0
a_bsignal[] init 16
a_bsignal, a_spatial_reverb_send Spatialize a_signal, k_space_front_to_back, k_space_left_to_right, k_space_bottom_to_top
outletv "outbformat", a_bsignal
outleta "out", a_spatial_reverb_send
#else
a_out_left, a_out_right pan2 a_signal, i_space_left_to_right
outleta "outleft", a_out_left
outleta "outright", a_out_right
#endif
; printks "Harpsichord      %9.4f   %9.4f\\n", 0.5, a_out_left, a_out_right
prints "Harpsichord    i %9.4f t %9.4f d %9.4f k %9.4f v %9.4f p %9.4f #%3d\\n", p1, p2, p3, p4, p5, p1/6, active(p1)
kpbend    pchbend   2
printks2 "pchbend %9.4f\\n", kpbend
kmodw     midictrl  1
printks2 "kmodw   %9.4f\\n", kmodw
kctl6     midictrl  6
printks2 "kctl6   %9.4f\\n", kctl6
kctl4     midictrl  4
printks2 "kctl4   %9.4f\\n", kctl4
kctl5     midictrl  5
printks2 "kctl5   %9.4f\\n", kctl5
kafter    aftouch   1
printks2 "kafter  %9.4f\\n", kafter
endin

gk_Reverb_feedback init 0.75
gi_Reverb_delay_modulation init 0.05
gk_Reverb_frequency_cutoff init 15000
instr ReverbSC
aleftout init 0
arightout init 0
aleft inleta "inleft"
aright inleta "inright"
; aoutL, aoutR reverbsc ainL, ainR, kfblvl, kfco[, israte[, ipitchm[, iskip]]]
aleftout, arightout reverbsc aleft, aright, gk_Reverb_feedback, gk_Reverb_frequency_cutoff, sr, gi_Reverb_delay_modulation
outleta "outleft", aleftout
outleta "outright", arightout
prints "ReverbSC       i %9.4f t %9.4f d %9.4f k %9.4f v %9.4f p %9.4f #%3d\\n", p1, p2, p3, p4, p5, p1/6, active(p1)
endin

gk_MasterOutput_level init -15
gS_MasterOutput_filename init ""
instr MasterOutput
aleft inleta "inleft"
aright inleta "inright"
k_gain = ampdb(gk_MasterOutput_level)
printks2 "Master gain: %f\\n", k_gain
iamp init 1
iattack init .01
idecay init 10
isustain = 2400 - (iattack + idecay)
aenvelope transeg 0.0, iattack / 2.0, 1.5, iamp / 2.0, iattack / 2.0, -1.5, iamp, isustain, 0.0, iamp, idecay / 2.0, 1.5, iamp / 2.0, idecay / 2.0, -1.5, 0
aleft butterlp aleft, 18000
aright butterlp aright, 18000
outs aleft * k_gain * aenvelope, aright * k_gain * aenvelope
; We want something that will play on my phone.
i_amplitude_adjustment = ampdbfs(-3) / 32767
i_filename_length strlen gS_MasterOutput_filename
if i_filename_length > 0 goto has_filename
goto non_has_filename
has_filename:
prints sprintf("Output filename: %s\\n", gS_MasterOutput_filename)
fout gS_MasterOutput_filename, 18, aleft * i_amplitude_adjustment, aright * i_amplitude_adjustment
non_has_filename:
prints "MasterOutput   i %9.4f t %9.4f d %9.4f k %9.4f v %9.4f p %9.4f #%3d\\n", p1, p2, p3, p4, p5, p1/6, active(p1)
kstatus, kchan, kdata1, kdata2 midiin
;printf "          midi in s %4d c %4d %4d %4d\\n", kdata2, kstatus, kchan, kdata1, kdata2
endin

    
    '''    
    
    # The "f 0" statement prevents an abrupt cutoff.
    sco = "f 0 105\n" + musx.to_csound_score(file)
    print(sco)
    
    csound = ctcsound.Csound()
    csound.setOption("-+msg_color=0")
    csound.setOption("-d")
    csound.setOption("-m195")
    csound.setOption("-f")
    # Change this for your actual audio configuration, try "aplay -l" to see what they are.
    # csound.setOption("-odac:plughw:1,0")
    csound.setOption("-odac")
    # Can also be a soundfile.
    # csound.setOption("-otest.wav")
    csound.compileOrc(orc)
    csound.readScore(sco)
    csound.start()
    # Probably runs a bit smoother in an independent thread (this is a native thread, 
    # not a Python thread).
    thread = ctcsound.CsoundPerformanceThread(csound.csound())
    thread.play()    
    thread.join()



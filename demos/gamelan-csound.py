################################################################################
"""
gamelan.py generates a gamelan composition using the `brush()` and `spray()`
generators in paint.py. Composer: Ming-ching Chiu.

To run this script cd to the parent directory of demos/ and do:
```bash
python3 -m demos.gamelan
```
"""
import musx
import ctcsound

if __name__ == '__main__':
    from musx import Score, Seq, MidiFile
    from musx.midi.gm import Vibraphone
    from .paint import brush, spray

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
    track0 = MidiFile.metatrack(ins={i: Vibraphone for i in range(microdivs)})
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
                       [9.3, 2.2], [7.1, 14.4], [0, 9.3], [3.8, 12]],
                 end=36)
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

    # Now the Csound stuff.
    
    orc  = '''

sr = 48000
ksmps = 128
nchnls = 2
0dbfs = 1

gi_ampmidicurve_dynamic_range init .375
gi_ampmidicurve_exponent init 5

connect "FMWaterBell", "outleft", "ReverbSC", "inleft"
connect "FMWaterBell", "outleft", "ReverbSC", "inleft"
connect "ReverbSC", "outleft", "MasterOutput", "inleft"
connect "ReverbSC", "outright", "MasterOutput", "inright"

alwayson "ReverbSC"
alwayson "MasterOutput"

gk_overlap init .0125

prealloc "FMWaterBell", 12

//////////////////////////////////////////////
// Original by Steven Yi.
// Adapted by Michael Gogins.
//////////////////////////////////////////////
gk_FMWaterBell_level init 12
gi_FMWaterBell_attack init 0.002
gi_FMWaterBell_release init 0.01
gi_FMWaterBell_sustain init 20
gi_FMWaterBell_sustain_level init .1
gk_FMWaterBell_index init .5
gk_FMWaterBell_crossfade init .5
gk_FMWaterBell_vibrato_depth init 0.05
gk_FMWaterBell_vibrato_rate init 6
gk_FMWaterBell_midi_dynamic_range init 30
gk_FMWaterBell_pan init .5
gi_FMWaterBell_cosine ftgen 0, 0, 65537, 11, 1
instr FMWaterBell
i_instrument = p1
i_time = p2
i_duration = p3
; One of the envelopes in this instrument should be releasing, and use this:
i_sustain = 1000
;xtratim gi_FMWaterBell_attack + gi_FMWaterBell_release
xtratim gi_FMWaterBell_attack + gi_FMWaterBell_release
i_midi_key = p4
i_midi_dynamic_range = i(gk_FMWaterBell_midi_dynamic_range)
i_midi_velocity = p5 * i_midi_dynamic_range / 127 + (63.6 - i_midi_dynamic_range / 2)
k_space_front_to_back = p6
k_space_left_to_right = gk_FMWaterBell_pan
k_space_bottom_to_top = p8
i_phase = p9
i_frequency = cpsmidinn(i_midi_key)
; Adjust the following value until "overall amps" at the end of performance is about -6 dB.
i_level_correction = 81
i_normalization = ampdb(-i_level_correction) / 2
i_amplitude = ampdb(i_midi_velocity) * i_normalization * 1.6
k_gain = ampdb(gk_FMWaterBell_level)
a_signal fmbell	1, i_frequency, gk_FMWaterBell_index, gk_FMWaterBell_crossfade, gk_FMWaterBell_vibrato_depth, gk_FMWaterBell_vibrato_rate, gi_FMWaterBell_cosine, gi_FMWaterBell_cosine, gi_FMWaterBell_cosine, gi_FMWaterBell_cosine, gi_FMWaterBell_cosine ;, gi_FMWaterBell_sustain
;a_envelope linsegr 0, gi_FMWaterBell_attack, 1, i_sustain, gi_FMWaterBell_sustain_level, gi_FMWaterBell_release, 0
a_envelope linsegr 0, gi_FMWaterBell_attack, 1, i_sustain, 1, gi_FMWaterBell_release, 0
; ares transegr ia, idur, itype, ib [, idur2] [, itype] [, ic] ...
; a_envelope transegr 0, gi_FMWaterBell_attack, 12, 1, i_sustain, 12, gi_FMWaterBell_sustain_level, gi_FMWaterBell_release, 12, 0
a_signal = a_signal * i_amplitude * a_envelope * k_gain
;_signal = a_signal * i_amplitude * k_gain
a_out_left, a_out_right pan2 a_signal, k_space_left_to_right
outleta "outleft", a_out_left
outleta "outright", a_out_right
prints "%-24.24s i %9.4f t %9.4f d %9.4f k %9.4f v %9.4f p %9.4f #%3d\\n", nstrstr(p1), p1, p2, p3, p4, p5, p7, active(p1)
; printks "FMWaterBell    i %9.4f t %9.4f d %9.4f k %9.4f v %9.4f p %9.4f #%3d l%9.4f r%9.4f\\n", 1, p1, p2, p3, p4, p5, p7, active(p1), dbamp(rms(a_out_left)), dbamp(rms(a_out_right))
endin

gk_Reverb_feedback init 0.5
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

gk_MasterOutput_level init 0
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
    sco = "f 0 90\n" + musx.to_csound_score(file)
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

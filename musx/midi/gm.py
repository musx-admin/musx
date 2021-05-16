"""
Defines constants for GM instruments, controllers and drum map values,
and dictionaries for reverse mapping to names. Names are sanitized for
Python syntax but are close to the names listed in
at https://www.midi.org/specifications-old/item/general-midi-2

Instrument Bank Constants (0-127)
----------------------------------

* AcousticGrandPiano, BrightAcousticPiano, ElectricGrandPiano, HonkytonkPiano, ElectricPiano1, ElectricPiano2, Harpsichord, Clavi
* Celesta, Glockenspiel, MusicBox, Vibraphone, Marimba, Xylophone, TubularBells, Dulcimer
* DrawbarOrgan, PercussiveOrgan, RockOrgan, ChurchOrgan, ReedOrgan, Accordion, Harmonica, TangoAccordion
* AcousticGuitar_nylon, AcousticGuitar_steel, ElectricGuitar_jazz, ElectricGuitar_clean, ElectricGuitar_muted, OverdrivenGuitar, DistortionGuitar, Guitarharmonics
* AcousticBass, ElectricBass_finger, ElectricBass_pick, FretlessBass, SlapBass1, SlapBass2, SynthBass1, SynthBass2
* Violin, Viola, Cello, Contrabass, TremoloStrings, PizzicatoStrings, OrchestralHarp, Timpani
* StringEnsemble1, StringEnsemble2, SynthStrings1, SynthStrings2, ChoirAahs, VoiceOohs, SynthVoice, OrchestraHit
* Trumpet, Trombone, Tuba, MutedTrumpet, FrenchHorn, BrassSection, SynthBrass1, SynthBrass2
* SopranoSax, AltoSax, TenorSax, BaritoneSax, Oboe, EnglishHorn, Bassoon, Clarinet
* Piccolo, Flute, Recorder, PanFlute, BlownBottle, Shakuhachi, Whistle, Ocarina
* Lead1_square, Lead2_sawtooth, Lead3_calliope, Lead4_chiff, Lead5_charang, Lead6_voice, Lead7_fifths, Lead8_basslead
* Pad1_newage, Pad2_warm, Pad3_polysynth, Pad4_choir, Pad5_bowed, Pad6_metallic, Pad7_halo, Pad8_sweep
* FX1_rain, FX2_soundtrack, FX3_crystal, FX4_atmosphere, FX5_brightness, FX6_goblins, FX7_echoes, FX8_scifi
* Sitar, Banjo, Shamisen, Koto, Kalimba, Bagpipe, Fiddle, Shanai
* TinkleBell, Agogo, SteelDrums, Woodblock, TaikoDrum, MelodicTom, SynthDrum, ReverseCymbal
* GuitarFretNoise, BreathNoise, Seashore, BirdTweet, TelephoneRing, Helicopter, Applause, Gunshot

Control Change Constants (0-127)
--------------------------------

* BankSelect, ModulationWheel, Breathcontroller, FootPedal, PortamentoTime, DataEntry, Volume, Balance
* Pan, Expression, EffectControl1, EffectControl2, GeneralPurpose1, GeneralPurpose2, GeneralPurpose3, GeneralPurpose4
* BankSelect_LSB, ModulationWheel_LSB, Breathcontroller_LSB, FootPedal_LSB, PortamentoTime_LSB, DataEntry_LSB, Volume_LSB, Balance_LSB
* Pan_LSB, Expression_LSB, EffectControl1_LSB, EffectControl2_LSB, SustainPedal_on_off, Portamento_on_off, SustenutoPedal_on_off, SoftPedal_on_off
* LegatoPedal_on_off, Hold2Pedal_on_off, SoundVariation, Timbre, ReleaseTime, AttackTime, Brightness, SoundControl6
* SoundControl7, SoundControl8, SoundControl9, SoundControl10, GeneralPurpose5, GeneralPurpose6, GeneralPurpose7, GeneralPurpose8
* PortamentoControl, Effects1Depth, Effects2Depth, Effects3Depth, Effects4Depth, Effects5Depth, Dataincrement, Datadecrement
* NonregisteredParameter_LSB, NonregisteredParameter_MSB, RegisteredParameter_LSB, RegisteredParameter_MSB, AllSoundOff, AllControllersOff, LocalKeyboard_on_off, AllNotesOff
* OmniOff, OmniOn, MonoOn, PolyOn

Percussion Map Constants (34-80)
--------------------------------

* AcousticBassDrum, BassDrum1, SideStick, AcousticSnare, HandClap, ElectricSnare, LowFloorTom, ClosedHiHat
* HighFloorTom, PedalHiHat, LowTom, OpenHiHat, LowMidTom, HiMidTom, CrashCymbal1, HighTom
* RideCymbal1, ChineseCymbal, RideBell, Tambourine, SplashCymbal, Cowbell, CrashCymbal2, Vibraslap
* RideCymbal2, HiBongo, LowBongo, MuteHiConga, OpenHiConga, LowConga, HighTimbale, LowTimbale
* HighAgogo, LowAgogo, Cabasa, Maracas, ShortWhistle, LongWhistle, ShortGuiro, LongGuiro
* Claves, HiWoodBlock, LowWoodBlock, MuteCuica, OpenCuica, MuteTriangle, OpenTriangle
"""

# Named constants for the GM instument map 0-127. 

AcousticGrandPiano = 0
BrightAcousticPiano = 1
ElectricGrandPiano = 2
HonkytonkPiano = 3
ElectricPiano1 = 4
ElectricPiano2 = 5
Harpsichord = 6
Clavi = 7
Celesta = 8
Glockenspiel = 9
MusicBox = 10
Vibraphone = 11
Marimba = 12
Xylophone = 13
TubularBells = 14
Dulcimer = 15
DrawbarOrgan = 16
PercussiveOrgan = 17
RockOrgan = 18
ChurchOrgan = 19
ReedOrgan = 20
Accordion = 21
Harmonica = 22
TangoAccordion = 23
AcousticGuitar_nylon = 24
AcousticGuitar_steel = 25
ElectricGuitar_jazz = 26
ElectricGuitar_clean = 27
ElectricGuitar_muted = 28
OverdrivenGuitar = 29
DistortionGuitar = 30
Guitarharmonics = 31
AcousticBass = 32
ElectricBass_finger = 33
ElectricBass_pick = 34
FretlessBass = 35
SlapBass1 = 36
SlapBass2 = 37
SynthBass1 = 38
SynthBass2 = 39
Violin = 40
Viola = 41
Cello = 42
Contrabass = 43
TremoloStrings = 44
PizzicatoStrings = 45
OrchestralHarp = 46
Timpani = 47
StringEnsemble1 = 48
StringEnsemble2 = 49
SynthStrings1 = 50
SynthStrings2 = 51
ChoirAahs = 52
VoiceOohs = 53
SynthVoice = 54
OrchestraHit = 55
Trumpet = 56
Trombone = 57
Tuba = 58
MutedTrumpet = 59
FrenchHorn = 60
BrassSection = 61
SynthBrass1 = 62
SynthBrass2 = 63
SopranoSax = 64
AltoSax = 65
TenorSax = 66
BaritoneSax = 67
Oboe = 68
EnglishHorn = 69
Bassoon = 70
Clarinet = 71
Piccolo = 72
Flute = 73
Recorder = 74
PanFlute = 75
BlownBottle = 76
Shakuhachi = 77
Whistle = 78
Ocarina = 79
Lead1_square = 80
Lead2_sawtooth = 81
Lead3_calliope = 82
Lead4_chiff = 83
Lead5_charang = 84
Lead6_voice = 85
Lead7_fifths = 86
Lead8_basslead = 87
Pad1_newage = 88
Pad2_warm = 89
Pad3_polysynth = 90
Pad4_choir = 91
Pad5_bowed = 92
Pad6_metallic = 93
Pad7_halo = 94
Pad8_sweep = 95
FX1_rain = 96
FX2_soundtrack = 97
FX3_crystal = 98
FX4_atmosphere = 99
FX5_brightness = 100
FX6_goblins = 101
FX7_echoes = 102
FX8_scifi = 103
Sitar = 104
Banjo = 105
Shamisen = 106
Koto = 107
Kalimba = 108
Bagpipe = 109
Fiddle = 110
Shanai = 111
TinkleBell = 112
Agogo = 113
SteelDrums = 114
Woodblock = 115
TaikoDrum = 116
MelodicTom = 117
SynthDrum = 118
ReverseCymbal = 119
GuitarFretNoise = 120
BreathNoise = 121
Seashore = 122
BirdTweet = 123
TelephoneRing = 124
Helicopter = 125
Applause = 126
Gunshot = 127


instrument_names = {
    0: 'Acoustic Grand Piano',
    1: 'Bright Acoustic Piano',
    2: 'Electric Grand Piano',
    3: 'Honky-tonk Piano',
    4: 'Electric Piano 1',
    5: 'Electric Piano 2',
    6: 'Harpsichord',
    7: 'Clavi',
    8: 'Celesta',
    9: 'Glockenspiel',
    10: 'Music Box',
    11: 'Vibraphone',
    12: 'Marimba',
    13: 'Xylophone',
    14: 'Tubular Bells',
    15: 'Dulcimer',
    16: 'Drawbar Organ',
    17: 'Percussive Organ',
    18: 'Rock Organ',
    19: 'Church Organ',
    20: 'Reed Organ',
    21: 'Accordion',
    22: 'Harmonica',
    23: 'Tango Accordion',
    24: 'Acoustic Guitar (nylon)',
    25: 'Acoustic Guitar (steel)',
    26: 'Electric Guitar (jazz)',
    27: 'Electric Guitar (clean)',
    28: 'Electric Guitar (muted)',
    29: 'Overdriven Guitar',
    30: 'Distortion Guitar',
    31: 'Guitar harmonics',
    32: 'Acoustic Bass',
    33: 'Electric Bass (finger)',
    34: 'Electric Bass (pick)',
    35: 'Fretless Bass',
    36: 'Slap Bass 1',
    37: 'Slap Bass 2',
    38: 'Synth Bass 1',
    39: 'Synth Bass 2',
    40: 'Violin',
    41: 'Viola',
    42: 'Cello',
    43: 'Contrabass',
    44: 'Tremolo Strings',
    45: 'Pizzicato Strings',
    46: 'Orchestral Harp',
    47: 'Timpani',
    48: 'String Ensemble 1',
    49: 'String Ensemble 2',
    50: 'SynthStrings 1',
    51: 'SynthStrings 2',
    52: 'Choir Aahs',
    53: 'Voice Oohs',
    54: 'Synth Voice',
    55: 'Orchestra Hit',
    56: 'Trumpet',
    57: 'Trombone',
    58: 'Tuba',
    59: 'Muted Trumpet',
    60: 'French Horn',
    61: 'Brass Section',
    62: 'SynthBrass 1',
    63: 'SynthBrass 2',
    64: 'Soprano Sax',
    65: 'Alto Sax',
    66: 'Tenor Sax',
    67: 'Baritone Sax',
    68: 'Oboe',
    69: 'English Horn',
    70: 'Bassoon',
    71: 'Clarinet',
    72: 'Piccolo',
    73: 'Flute',
    74: 'Recorder',
    75: 'Pan Flute',
    76: 'Blown Bottle',
    77: 'Shakuhachi',
    78: 'Whistle',
    79: 'Ocarina',
    80: 'Lead 1 (square)',
    81: 'Lead 2 (sawtooth)',
    82: 'Lead 3 (calliope)',
    83: 'Lead 4 (chiff)',
    84: 'Lead 5 (charang)',
    85: 'Lead 6 (voice)',
    86: 'Lead 7 (fifths)',
    87: 'Lead 8 (bass + lead)',
    88: 'Pad 1 (new age)',
    89: 'Pad 2 (warm)',
    90: 'Pad 3 (polysynth)',
    91: 'Pad 4 (choir)',
    92: 'Pad 5 (bowed)',
    93: 'Pad 6 (metallic)',
    94: 'Pad 7 (halo)',
    95: 'Pad 8 (sweep)',
    96: 'FX 1 (rain)',
    97: 'FX 2 (soundtrack)',
    98: 'FX 3 (crystal)',
    99: 'FX 4 (atmosphere)',
    100: 'FX 5 (brightness)',
    101: 'FX 6 (goblins)',
    102: 'FX 7 (echoes)',
    103: 'FX 8 (sci-fi)',
    104: 'Sitar',
    105: 'Banjo',
    106: 'Shamisen',
    107: 'Koto',
    108: 'Kalimba',
    109: 'Bag pipe',
    110: 'Fiddle',
    111: 'Shanai',
    112: 'Tinkle Bell',
    113: 'Agogo',
    114: 'Steel Drums',
    115: 'Woodblock',
    116: 'Taiko Drum',
    117: 'Melodic Tom',
    118: 'Synth Drum',
    119: 'Reverse Cymbal',
    120: 'Guitar Fret Noise',
    121: 'Breath Noise',
    122: 'Seashore',
    123: 'Bird Tweet',
    124: 'Telephone Ring',
    125: 'Helicopter',
    126: 'Applause',
    127: 'Gunshot'
}
'''
A dictionary of GM instrument names indexed by program change values 0 to 127. 
Note: these are the true midi values, i.e. one less than the one-based numbers
listed in GM tables on the web.
'''


BankSelect = 0
ModulationWheel = 1
Breathcontroller = 2
FootPedal = 4
PortamentoTime = 5
DataEntry = 6
Volume = 7
Balance = 8
Pan = 10
Expression = 11
EffectControl1 = 12
EffectControl2 = 13
GeneralPurpose1 = 16
GeneralPurpose2 = 17
GeneralPurpose3 = 18
GeneralPurpose4 = 19
BankSelect_LSB = 32
ModulationWheel_LSB = 33
Breathcontroller_LSB = 34
FootPedal_LSB = 36
PortamentoTime_LSB = 37
DataEntry_LSB = 38
Volume_LSB = 39
Balance_LSB = 40
Pan_LSB = 42
Expression_LSB = 43
EffectControl1_LSB = 44
EffectControl2_LSB = 45
SustainPedal_on_off = 64
Portamento_on_off = 65
SustenutoPedal_on_off = 66
SoftPedal_on_off = 67
LegatoPedal_on_off = 68
Hold2Pedal_on_off = 69
SoundVariation = 70
Timbre = 71
ReleaseTime = 72
AttackTime = 73
Brightness = 74
SoundControl6 = 75
SoundControl7 = 76
SoundControl8 = 77
SoundControl9 = 78
SoundControl10 = 79
GeneralPurpose5 = 80
GeneralPurpose6 = 81
GeneralPurpose7 = 82
GeneralPurpose8 = 83
PortamentoControl = 84
Effects1Depth = 91
Effects2Depth = 92
Effects3Depth = 93
Effects4Depth = 94
Effects5Depth = 95
Dataincrement = 96
Datadecrement = 97
NonregisteredParameter_LSB = 98
NonregisteredParameter_MSB = 99
RegisteredParameter_LSB = 100
RegisteredParameter_MSB = 101
AllSoundOff = 120
AllControllersOff = 121
LocalKeyboard_on_off = 122
AllNotesOff = 123
OmniOff = 124
OmniOn = 125
MonoOn = 126
PolyOn = 127


controller_names = {
    0: "Bank Select",
    1: "Modulation Wheel",
    2: "Breath controller",
    4: "Foot Pedal",
    5: "Portamento Time",
    6: "Data Entry",
    7: "Volume",
    8: "Balance",
    10: "Pan",
    11: "Expression",
    12: "Effect Control 1",
    13: "Effect Control 2",
    16: "General Purpose 1",
    17: "General Purpose 2",
    18: "General Purpose 3",
    19: "General Purpose 4",
    32: "Bank Select (LSB)",
    33: "Modulation Wheel (LSB)",
    34: "Breath controller (LSB)",
    36: "Foot Pedal (LSB)",
    37: "Portamento Time (LSB)",
    38: "Data Entry (LSB)",
    39: "Volume (LSB)",
    40: "Balance (LSB)",
    42: "Pan (LSB)",
    43: "Expression (LSB)",
    44: "Effect Control 1 (LSB)",
    45: "Effect Control 2 (LSB)",
    64: "Sustain Pedal (on/off)",
    65: "Portamento (on/off)",
    66: "Sustenuto Pedal (on/off)",
    67: "Soft Pedal (on/off)",
    68: "Legato Pedal (on/off)",
    69: "Hold 2 Pedal (on/off)",
    70: "Sound Variation",
    71: "Timbre ",
    72: "Release Time",
    73: "Attack Time",
    74: "Brightness",
    75: "Sound Control 6",
    76: "Sound Control 7",
    77: "Sound Control 8",
    78: "Sound Control 9",
    79: "Sound Control 10",
    80: "General Purpose 5",
    81: "General Purpose 6",
    82: "General Purpose 7",
    83: "General Purpose 8",
    84: "Portamento Control",
    91: "Effects 1 Depth",
    92: "Effects 2 Depth",
    93: "Effects 3 Depth",
    94: "Effects 4 Depth",
    95: "Effects 5 Depth",
    96: "Data increment",
    97: "Data decrement",
    98: "Non-registered Parameter (LSB)",
    99: "Non-registered Parameter (MSB)",
    100: "Registered Parameter (LSB)",
    101: "Registered Parameter (MSB)",
    120: "All Sound Off",
    121: "All Controllers Off",
    122: "Local Keyboard (on/off)",
    123: "All Notes Off",
    124: "Omni Off",
    125: "Omni On",
    126: "Mono On",
    127: "Poly On"
}
'''
A dictionary of GM controller names indexed by controller change values 0 to 127. 
Note: these are the true midi values, i.e. one less than the one-based numbers
listed in GM tables on the web. There are a number of undefined values in the 
range so you should iterate using controller_names.items() 
'''

    
AcousticBassDrum = 34
BassDrum1 = 35
SideStick = 36
AcousticSnare = 37
HandClap = 38
ElectricSnare = 39
LowFloorTom = 40
ClosedHiHat = 41
HighFloorTom = 42
PedalHiHat = 43
LowTom = 44
OpenHiHat = 45
LowMidTom = 46
HiMidTom = 47
CrashCymbal1 = 48
HighTom = 49
RideCymbal1 = 50
ChineseCymbal = 51
RideBell = 52
Tambourine = 53
SplashCymbal = 54
Cowbell = 55
CrashCymbal2 = 56
Vibraslap = 57
RideCymbal2 = 58
HiBongo = 59
LowBongo = 60
MuteHiConga = 61
OpenHiConga = 62
LowConga = 63
HighTimbale = 64
LowTimbale = 65
HighAgogo = 66
LowAgogo = 67
Cabasa = 68
Maracas = 69
ShortWhistle = 70
LongWhistle = 71
ShortGuiro = 72
LongGuiro = 73
Claves = 74
HiWoodBlock = 75
LowWoodBlock = 76
MuteCuica = 77
OpenCuica = 78
MuteTriangle = 79
OpenTriangle = 80


percussion_names = {
    34: 'Acoustic Bass Drum',
    35: 'Bass Drum 1',
    36: 'Side Stick',
    37: 'Acoustic Snare',
    38: 'Hand Clap',
    39: 'Electric Snare',
    40: 'Low Floor Tom',
    41: 'Closed Hi Hat',
    42: 'High Floor Tom',
    43: 'Pedal Hi Hat',
    44: 'Low Tom',
    45: 'Open Hi Hat',
    46: 'Low-Mid Tom',
    47: 'Hi-Mid Tom',
    48: 'Crash Cymbal 1',
    49: 'High Tom',
    50: 'Ride Cymbal 1',
    51: 'Chinese Cymbal',
    52: 'Ride Bell',
    53: 'Tambourine',
    54: 'Splash Cymbal',
    55: 'Cowbell',
    56: 'Crash Cymbal 2',
    57: 'Vibraslap',
    58: 'Ride Cymbal 2',
    59: 'Hi Bongo',
    60: 'Low Bongo',
    61: 'Mute Hi Conga',
    62: 'Open Hi Conga',
    63: 'Low Conga',
    64: 'High Timbale',
    65: 'Low Timbale',
    66: 'High Agogo',
    67: 'Low Agogo',
    68: 'Cabasa',
    69: 'Maracas',
    70: 'Short Whistle',
    71: 'Long Whistle',
    72: 'Short Guiro',
    73: 'Long Guiro',
    74: 'Claves',
    75: 'Hi Wood Block',
    76: 'Low Wood Block',
    77: 'Mute Cuica',
    78: 'Open Cuica',
    79: 'Mute Triangle',
    80: 'Open Triangle',
}
'''
A dictionary of GM drum map names indexed by controller change values 34 to 80. 
Note: these are the true midi values, i.e. one less than the one-based numbers
listed in GM tables on the web.
'''


if __name__ == '__main__':
    ## creates hygenically named constants from the instrument names
    # for i,n in musx.midi.gm.controller_names.items():
    #     n = n.replace(' ','').replace(')','').replace('(','_').replace('+','').replace('-','')
    #     print(f"{n} = {i}")

    # creates hygenically named constants from the controller names
    # for i, n in musx.midi.gm.controller_names.items():
    #     n = n.replace(' ','').replace(')','').replace('(','_').replace('+','').replace('-','').replace('/','_')
    #     print(f"{n} = {i}")

    # creates hygenically named constants from the controller names
    #for i, n in percussion_names.items():
    #    n = n.replace(' ','').replace(')','').replace('(','_').replace('+','').replace('-','').replace('/','_')
    #    print(f"{n} = {i}")

    # print("instrument_names = {")
    # for i,n in enumerate(instrument_names):
    #     print(f"    {i}: '{n}',")
    # print("}")

    # print("percussion_names = {")
    # for i,n in enumerate(percussion_names):
    #    print(f"    {i+34}: '{n}',")
    # print("}")
    pass

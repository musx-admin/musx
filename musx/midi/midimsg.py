"""
A module that defines low level constructors and accessors for manipulating 
lists of bytes as midi messsages.
"""

# Channel Messages
kNoteOff     = 0b10000000
kNoteOn      = 0b10010000
kAftertouch  = 0b10100000
kCtrlChange  = 0b10110000
kProgChange  = 0b11000000
kChanPress   = 0b11010000
kPitchBend   = 0b11100000

# Channel Messages masks
kChannelMask = 0b00001111
kStatusMask  = 0b11110000

# System Common Messages
kSysEx       = 0b11110000
kTimeCode    = 0b11110001
kSongPos     = 0b11110010
kSongSel     = 0b11110011
kTuneReq     = 0b11110110
kEOE         = 0b11110111

# System RealTime Messages
kTimingClock = 0b11111000
kStart       = 0b11111010
kContinue    = 0b11111011
kStop        = 0b11111100
kActiveSens  = 0b11111110
kReset       = 0b11111111

# MetaMessages (only exist in midi file)
kMetaMsg     = 0b11111111 # equals kReset but kReset is never found in midi files.
kSeqNumber   = 0b00000000
kText        = 0b00000001
kCopyRight   = 0b00000010
kTrackName   = 0b00000011
kInstName    = 0b00000100
kLyric       = 0b00000101
kMarker      = 0b00000110
kCuePoint    = 0b00000111
kProgName    = 0b00001000
kDevName     = 0b00001001
kChanPrefix  = 0b00100000
kMidiPort    = 0b00100001
kEOT         = 0b00101111
kTempo       = 0b01010001
kSMPTEOff    = 0b00101010
kTimeSig     = 0b01011000
kKeySig      = 0b01011001
kSeqEvent    = 0b01111111

# SMPTE Frame Formats
kfps24     = 0
kfps25     = 1
kfps30drop = 2
kfps30     = 3


def status(msg):
    """Returns the status byte of the message."""
    return (msg[0] & kStatusMask) if is_channel_message(msg) else msg[0]


def has_status(msg, stat):
    """Returns true if the message is of the specified status type."""
    return status(msg) == stat


# Channel Messages


def is_channel_message(msg):
    """Returns true if the message is a channel message."""
    return msg[0] < kSysEx


def channel(msg):
    """Returns the channel number of the message."""
    return msg[0] & kChannelMask


# Note Off and Note On


def note_off(chan, key, vel):
    """
    Creates a note off message.

    Parameters
    ----------
    chan : 0-15
        The midi channel of the message.
    key : byte
        The midi key number.
    vel : byte
        The velocity of the key up.
    """
    return [kNoteOff | chan, key, vel]


def note_on(chan, key, vel):
    """
    Creates a note on message.

    Parameters
    ----------
    chan : 0-15
        The midi channel of the message.
    key : byte
        The midi key number.
    vel : byte
        The velocity of the key down.
    """
    return [kNoteOn | chan, key, vel]


def keynum(msg):
    """Returns the key number of a note on, off, or aftertouch message."""
    return msg[1]


def velocity(msg):
    """Returns the velocity value of a note on or off message."""
    return msg[2]


# Aftertouch


def aftertouch(chan, key, press):
    """
    Creates an aftertouch message.

    Parameters
    ----------
    chan : 0-15
        The midi channel of the message.
    key : byte
        The midi key number.
    press : byte
        The pressure value.
    """
    return [kAftertouch | chan, key, press]


def touch(msg):
    """Returns the value of an aftertouch message."""
    return msg[2]


# Control Change


def control_change(chan, ctrl, val):
    """
    Creates a control change message.

    Parameters
    ----------
    chan : 0-15
        The midi channel of the message.
    ctrl : byte
        The controller number.
    val : byte
        The controller value.
    """ 
    return [kCtrlChange | chan, ctrl, val]


def controller(msg):
    """Returns the controller number of a control change message."""
    return msg[1]


def control(msg):
    """Returns the controller value of a control change message."""
    return msg[2]


# Program Change


def program_change(chan, prog):
    """
    Creates a program change message.

    Parameters
    ----------
    chan : 0-15
        The midi channel of the message.
    prog : byte
        The program value.
    """
    return [kProgChange | chan, prog]


def program(msg):
    """Returns the program value of a program change message."""
    return msg[1]


# Channel Pressure


def channel_pressure(chan, press):
    """
    Creates a channel pressure message.

    Parameters
    ----------
    chan : 0-15
        The midi channel of the message.
    press : byte
        The pressure value.
    """ 
    return [kChanPress | chan, press]


def pressure(msg):
    """Returns the pressure value of a channel pressure message."""
    if status(msg) == kAftertouch:
        assert False, "shouldnt happen"
    return msg[1]


# Pitch Bend


def pitch_bend(chan, value):
    """
    Creates a pitch bend message.
    
    Parameters
    ----------
    chan : 0-15
        The midi channel of the message.
    value : integer
        The 14-bit pitch bend value.
    """
    return [kPitchBend | chan, value & 0x7F, (value >> 7) & 0x7F]


def bend(msg):
    """Returns the pitch bend value of a pitch bend message."""
    return (msg[2] & 0x7F) << 7 | (msg[1] & 0x7F)


# Channel Mode Messages (these are just control changes 120-127)


def all_sounds_off(chan, val):
    """
    Creates an 'all sounds off' control message.

    Parameters
    ----------
    chan : 0-15
        The midi channel of the message.
    val : byte
        The controller value.
    """
    return control_change(chan, 120, val)


def reset_all_controllers(chan, val):
    """
    Creates a 'reset all controllers' control message.

    Parameters
    ----------
    chan : 0-15
        The midi channel of the message.
    val : byte
        The controller value.
    """
    return control_change(chan, 121, val)


def local_control(chan, val):
    """
    Creates a 'local control' control message.

    Parameters
    ----------
    chan : 0-15
        The midi channel of the message.
    val : byte
        The controller value.
    """
    return control_change(chan, 122, val)


def all_notes_off(chan):
    """
    Creates an 'all notes off' control message.

    Parameters
    ----------
    chan : 0-15
        The midi channel of the message.
    """
    return control_change(chan, 123, 0)


def omni_mode_off(chan):
    """
    Creates a 'omni mode off' control message.

    Parameters
    ----------
    chan : 0-15
        The midi channel of the message.
    """
    return control_change(chan, 124, 0)


def omni_mode_on(chan):
    """
    Creates a 'omni mode on' control message.

    Parameters
    ----------
    chan : 0-15
        The midi channel of the message.
    """
    return control_change(chan, 125, 0)


def mono_mode_on(chan):
    """
    Creates a 'mono mode on' control message.

    Parameters
    ----------
    chan : 0-15
        The midi channel of the message.
    """
    return control_change(chan, 126, 0)


def mono_mode_off(chan, chans):
    """
    Creates a 'mono mode off' control message.

    Parameters
    ----------
    chan : 0-15
        The midi channel of the message.
    chans : byte
        The channels.
    """
    return control_change(chan, 126, chans)


def poly_mode_on(chan):
    """
    Creates a 'poly mode on' control message.

    Parameters
    ----------
    chan : 0-15
        The midi channel of the message.
    """
    return control_change(chan, 127, 0)


def is_system_message(msg):
    """Returns true if the message is a system message."""
    return msg[0] >= kSysEx


def is_system_common_message(msg):
    """Returns true if the message is a system common message."""
    return kSysEx <= msg[0] <= kEOE


def is_system_realtime_message(msg):
    """Returns true if the message is a system realtime message."""
    return kTimingClock <= msg[0] <= kReset


# System Common Messages. (these are not valid in midi files.)


def sysex(data):
    """
    Creates a system exclusive message ending with EOE.

    Parameters
    ----------
    data : list
        A list of data bytes ending with EOE.
    """
    if data[-1] != kEOE:
        data.append(kEOE)  # make sure data includes EOE
    return [kSysEx, len(data), bytes(data)]


def midi_time_code(typ, val):
    """
    Creates a time code message.

    Parameters
    ----------
    type : 0-15
        The time code type.
    value : byte
        The type code value.
    """
    return [kTimeCode, (typ << 4) | val]


def midi_song_position(pos):
    """
    Creates a song position message.

    Parameters
    ----------
    pos : int
        A 14 bit song pointer position.
    """
    lsb = pos & 0x7F
    msb = pos >> 7
    return [kSongPos, lsb, msb]


def midi_song_select(song):
    """
    Creates a song select message.

    Parameters
    ----------
    song : byte
        The song number to set.
    """
    return [kSongSel, song]


def midi_tune_request():
    """Creates a midi tune request message."""
    return [kTuneReq]


def midi_end_of_exclusive():
    """Creates an end of exclusive message."""
    return [kEOE]


# System Real Time Messages (these are not valid in midi files.)


def midi_clock():
    """Creates a midi clock message."""
    return [kTimingClock]


def midi_start():
    """Creates a midi start message."""
    return [kStart]


def midi_continue():
    """Creates a midi continue message."""
    return [kContinue]


def midi_stop():
    """Creates a midi stop message."""
    return [kStop]


def active_sensing():
    """Creates an active sensing midi message."""
    return [kActiveSens]


def midi_reset():
    """Creates a midi reset message."""
    return [kReset]


# Midi Meta Messages. (these have the same upper byte value 0xFF as
# as system messages but they are mutually exclusive: system messages cannot
# appear in midi files and meta messages cannot be sent to devices)


def is_meta_message(msg):
    """Returns true if the message is a midi meta message."""
    return msg[0] == kMetaMsg and len(msg) >= 3


def is_meta_message_type(msg, typ):
    """Returns true if the message is a midi meta message of the specified type."""
    return is_meta_message(msg) and msg[1] == typ


def int_to_vlq(val):
    """
    Converts an integer value into a variable length quantity (list).
    """
    vlq = []
    for i in range(21, 0, -7):
        if val >= (1 << i):
            vlq.append(((val >> i) & 0x7F) | 0x80)
    vlq.append(val & 0x7F)
    return vlq


def meta_seq_number(num):
    """
    Creates a sequence number meta message.

    Parameters
    ----------
    num : byte
        The sequence number
    """
    msb = num & (0x7F << 7)
    lsb = num & 0x7f
    return [kMetaMsg, kSeqNumber, 2, msb, lsb]


def text_meta_message(metatype, txt):
    """
    Creates a meta text message.

    Parameters
    ----------
    metatype : byte
        The meta type id of the message.
    txt : string
        The text string for the message.
    """
    data = txt.encode('ascii') if isinstance(txt, str) else txt
    assert isinstance(data, bytes), "meta text message data is not bytes()."
    return [kMetaMsg, metatype, len(data), data]


def text(meta):
    """
    Returns the meta message's text as a string.
    """
    return meta[3].decode('ascii')


def meta_text(txt):
    """
    Creates a text meta message.

    Parameters
    ----------
    txt : string
        The text string for the message.
    """
    return text_meta_message(kText, txt)


def meta_copyright(txt):
    """
    Creates a copyright message.

    Parameters
    ----------
    txt : string
        The copyright string for the message.
    """
    return text_meta_message(kCopyRight, txt)


def meta_track_name(txt):
    """
    Creates a track name meta message.

    Parameters
    ----------
    txt : string
        The track name for the message.
    """
    return text_meta_message(kTrackName, txt)


def meta_inst_name(txt):
    """
    Creates an instrument name meta message.

    Parameters
    ----------
    txt : string
        The instrument name for the message.
    """
    return text_meta_message(kInstName, txt)


def meta_lyric(txt):
    """
    Creates a lyric meta message.

    Parameters
    ----------
    txt : string
        The lyrics string for the message.
    """
    return text_meta_message(kLyric, txt)


def meta_marker(txt):
    """
    Creates a marker meta message.

    Parameters
    ----------
    txt : string
        The meta marker text for the message.
    """
    return text_meta_message(kMarker, txt)


def meta_cue(txt):
    """
    Creates a cue meta message.

    Parameters
    ----------
    txt : string
        The cueing string for the message.
    """
    return text_meta_message(kCuePoint, txt)


def meta_program_name(txt):
    """
    Creates a program name meta message.

    Parameters
    ----------
    txt : string
        The cue string for the message.
    """
    return text_meta_message(kProgName, txt)


def meta_device_name(txt):
    """
    Creates a device name meta message.

    Parameters
    ----------
    txt : string
        The device name.
    """
    return text_meta_message(kDevName, txt)


def meta_chan_prefix(chan):
    """
    Creates a channel prefix meta message.

    Parameters
    ----------
    chan : byte
    The channel prefix number.
    """
    return [kMetaMsg, kChanPrefix, 1, chan]


def meta_port(port):
    """
    Creates a port meta message.
    Note: **This meta event is depreciated in the midi spec.**
    """
    return [kMetaMsg, kMidiPort, 1, port]

 
def meta_eot():
    """Creates an end of track meta message."""
    return [kMetaMsg, kEOT, 0]


def meta_tempo(usecs_per_quarter):
    """
    Creates a tempo meta message.

    Parameters
    ----------
    usecs_per_quarter : int
        The number of microseconds in a quarter note.
    """
    msg = [kMetaMsg, kTempo, 3]
    for i in range(16, -1, -8):
        msg.append((usecs_per_quarter & (0xff << i)) >> i)
    return msg


def tempo(msg):
    """Returns the usec tempo value from a tempo meta message."""
    return (msg[3] << 16) + (msg[4] << 8) + msg[5]


def meta_time_sig(top, bot, clocks=24, tsecs=8):
    """
    Creates a time signature meta message.

    Parameters
    ----------
    top : byte
        The top number of the time signature
    bot : byte
        The power of 2 of the bottom number: 0 is top/1, 2 is top/4, etc.
    clocks : byte
        The number of MIDI clocks between metronome clicks.
    tsecs : byte
        the number of 32nds in a quarter note (usually 8).
    """
    return [kMetaMsg, kTimeSig, 4, top, bot, clocks, tsecs]


def meta_key_sig(sf, mode):
    """
    Creates a key signature meta message.

    Parameters
    ----------
    sf : -7 to 7 
        Negative numbers name flat keys (Eb is -3 etc.) and positive numbers name sharp keys (A is 3 etc.).
    mode : 0 or 1
        Specify 0 for major keys and 1 for minor keys.
    """
    return [kMetaMsg, kKeySig, 2, sf, mode]


def meta_seq_event(data):
    """
    Creates a sequencer specific meta message.

    Parameters
    ----------
    data : list
        A list of bytes to send to the sequencer.   
    """
    return [kMetaMsg, kSeqEvent, len(data), bytes(data)]

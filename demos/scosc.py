###############################################################################
"""
This demo demonstrates how to send OSC messages to SuperCollider in "real time".
Before running the demo you will first need to:

1) Install the python-osc package:

```python3.9 -m pip install python-osc```

2) Start SuperCollider.app and open the file 'bell.scd' located in the same
directory as this file. 

3) With the bell.scd file now visible in SuperCollider, press COMMAND-A to select
the entire document and COMMAND-Return to execute it.

Now that SuperCollider is running, cd to the parent directory of demos/ and do:
```bash
python3 -m demos.scosc
```
"""

import pythonosc.udp_client
import threading, time
import musx


class OscMessage(musx.Event):
    """
    A class to represent the OSC messages sent to SuperCollider
    """
    def __init__(self, name, time, freq=440, dur=.5, amp=.5):
        super().__init__(time)
        self.name = name
        self.data = [time, freq, dur, amp]
    def __str__(self):
        return f"<OscMessage: '{self.name}' {self.data} {hex(id(self))}>"
    __repr__ = __str__

        
def oscplayer(oscseq, oscout):
    """
    A threaded player for 'real time' playback of an OscSeq.
    
    Parameters
    ----------
    oscseq : OscSeq
        An OscSeq containing a time sorted list of OscMessages.
    oscport : pythonosc.udp_client.SimpleUDPClient
        An open pythonosc.udp_client.SimpleUDPClient.
    """
    messages = oscseq.messages
    length = len(messages)
    thistime = messages[0].time()
    nexttime = thistime
    i = 0
    while i < length:
        if messages[i].time == thistime:
            #print(f'playing {messages[i]}')
            oscout.send_message(messages[i].name, messages[i].data)
            i += 1
            continue
        # if here then midi[i] is later than thistime so sleep
        nexttime = messages[i].time
        #print(f'waiting {nexttime-thistime}')
        time.sleep(nexttime - thistime) 
        thistime = nexttime

def plain_hunt(q, rhy, dur):
    """
    A composer function that generates osc messages using the
    Plain Hunt change ringing pattern.
    """
    # one octave of bells numbered 8, 7, ... 1
    bells = [n for n in range(8, 0, -1)]
    # the frequencies each bell plays (D major)
    freqs = {i:f for i,f in zip(bells, musx.hertz("d5 c# b4 a g f# e d"))}
    # Plain Hunt's rotation rules
    rules = [[0, 2, 1], [1, 2, 1]]
    # generate the Plain Hunt pattern for 8 bells
    peals = musx.all_rotations(bells, rules, False, True)
    # write OscMessages to the OscSeq
    for b in peals:
        f = freqs[b]
        m = OscMessage(name="/musx", time=q.now, duration=dur, freq=f, amplitude=.9)
        sco.add(m)
        yield rhy

if __name__ == "__main__":

    # Create an osc connection to send messages to SuperCollider
    oscout = pythonosc.udp_client.SimpleUDPClient("127.0.0.1", 57120)
    # oscseq will hold the composition.
    oscseq = musx.Seq()
    # Create a score and give it oscseq to hold the score event data.
    sco = musx.Score(out=oscseq)
    # Create the composition.
    sco.compose(plain_hunt(sco, .3, 4))
    # play the osc messages in "real time" to SuperCollider
    player = threading.Thread(target=oscplayer, args=(oscseq, oscout))
    player.start()
    player.join()

    

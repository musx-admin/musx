# Installing musx

This document explains how to install musx in a Python [virtual environment](https://docs.python.org/3/library/venv.html).  A virtual environment is an independent Python installation dedicated to a specific project (such as musx) without affecting your computer's global Python environment.  Highly recommended!

1. The musx package requires Python 3.9 or higher.  You can download the most recent releases of Python from https://www.python.org/downloads/. Once downloaded, double-click the installation package to install Python on your computer.

2. Open your computer's terminal application, create a directory dedicated to working with musx, then cd into your new workspace. (The `$` represents your terminal's prompt, do not include it as part of your command!):

``` 
$ mkdir ~/projects/mymusx
$ cd ~/projects/mymusx
```

3. Call Python 3.10 or higher and create a virtual environment for musx. You can use any name, this document calls it *musxenv* :

``` 
$ python3 -m venv musxenv
```

4. Activate the musxenv virtual environment. Once activated you will see the name of the environnment prepended to your terminal's prompt:

```
$ source musxenv/bin/activate
(musxenv) $
```

5. With musxenv activated you can now use the generic 'python' command to invoke the correct Python version for the environment:

```
(musxenv) $ python
 Python 3.10.6 (v3.10.6:9c7b4bd164, Aug  1 2022, 17:13:48) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
 Type "help", "copyright", "credits" or "license" for more information.
 >>> quit()
 (musxenv) $
```

6. Next, make sure the musxenv environment uses the latest versions of pip, setuptools and wheel:

```
(musxenv) $ python -m pip install --upgrade pip setuptools wheel
```

7. Install the musx support packages [matplotlib](https://matplotlib.org/), [jupyter](https://pypi.org/project/jupyter/), and [lxml](https://pypi.org/project/lxml/).  This will take a minute or two...

```
(musxenv) $ python -m pip install matplotlib jupyter lxml
```

8. Associate the musxenv environment name with your jupyter kernel so you can select musxenv as the notebook's kernel when you run musx demos and tutorials in jupyter notebooks.  The jupyter kernel will inform you where it saves the kernel spec should you want to edit its properties further:

```
(musxenv) $ python -m ipykernel install --user --name=musxenv
Installed kernelspec musxvenv in /Users/taube/Library/Jupyter/kernels/musxenv
```

9. Install musx and (optionally) download its support directories into your mymusx working directory for easy access:

```
(musxenv) $ python -m pip install musx
```
* [Documentation (HTML)](https://github.com/musx-admin/musx/tree/main/docs)
* [Tutorials (Jupyter Notebook)](https://github.com/musx-admin/musx/tree/main/tutorials)
* [Demos (Jupyter Notebook)](https://github.com/musx-admin/musx/tree/main/demos)

10. To test that musx is working, start up python, import the musx package, and call a function:

```
(musxenv) $ python
>>> import musx
>>> musx.keynum('C4')
60
>>> exit()
(musxenv) $
```
___

That's it! 🤗  The best way to learn about the musx system is to read the documentation and run the demo and tutorial scripts, e.g.:

```
(musxenv) $ jupyter notebook demos/gamelan.ipynb
```

When you are done with your musx session type 'deactivate' to shut down your virtural environment. Once deactivated your terminal prompt will no longer display the virtual envronment name:

```
(musxenv) $ deactivate
$ 
```

## Customizations

1. To work with the musx tutorials and demos you will want to install a terminal-based midi synthesizer.  [fluidsynth](http://www.fluidsynth.org/) is a good choice, you can use [Homebrew](https://brew.sh/) to install it on mac, linux, and windows:

```
$ brew install fluid-synth
```

Once installed, you need to give fluidsynth a sound font to use, for example the free [MuseScore_General.sf3](ftp://ftp.osuosl.org/pub/musescore/soundfont/MuseScore_General/MuseScore_General.sf2).  After downloading the sound font move it to a permanent location on your hard drive, e.g. /usr/local/soundfonts/, and then pass that pathname to fluidsynth when you play a midi file:

```
$ fluidsynth -iq -g2 /usr/local/soundfonts/MuseScore_General.sf3 mymidifile.mid
```

Since that command is pretty long consider adding an alias to your .bashrc (or whatever) file:

```
$ alias fs="fluidsynth -iq -g2 /usr/local/soundfonts/MuseScore_General.sf3"
```

With that alias in effect, to play a midi file in the terminal you just type:

```
$ fs mymidifile.mid
```

2. To generate audio files, design your own audio instruments, and access dozens of CCMRA's historical audio instruments, install Todd Ingall's [pysndlib](https://pypi.org/project/pysndlib/) package and then load the musx.audio packge:

```
(musxenv) $ pip install pysndlib
(musxenv) $ python
>>> import musx, pysndlib
>>> from musx.audio import AudioNote, AudioFile
>>>
```

 Pysndlib is a Python/Cython wrapper around Bill Schottstaedt's C-language audio library [sndlib](https://ccrma.stanford.edu/software/snd/snd/sndlib.html) developed at CCRMA, Stanford. See the pysndlib tutorial for more information.

3. To send and receive 'real time' MIDI messages install the [python-rtmidi](https://pypi.org/project/python-rtmidi/) package by Christopher Arndt/Gary Scavone. See the [rtmidi](rtmidi.ipynb) tutorial on how
to work with the system in musx.

___

—Rick Taube  

Emeritus Professor, Composition/Theory/CS+Music  
School of Music  
University of Illinois Urbana-Champaign  
Email: taube@illinois.edu  

President, Illiac Software Inc.  
https://harmonia.cloud/  
Email: taube@illiacsoftware.com  


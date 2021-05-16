# Installing musx

There are two ways to install musx:  via pip, or via git.  If you only want to install the working musx package then use pip.  If you want to install the source base that includes demos, source code and other materials use git. 

## Installing musx via pip

```
$ python3.9 -m install musx
```

## Installing musx via git

```
# git clone musx.git
```

The rest of this document explains how to install musx from its git repository into a working python virtual environment. In the explanation that follows, the name *musx_working_directory* refers to the directory on your machine that contains this document.

* musx requires python >= 3.9.  If its not already installed,  [install Python 3.9](https://www.python.org/downloads/) on your computer and then make sure you can start it in a terminal. If you are on a mac you can use Terminal.app located in your /Applications/Utilities/ folder. If you are on Windows 10 you can install the [Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/) for an integrated linux terminal.

* In your terminal's window use the cd command to change directories to the *musx_working_directory* (the directory containing this file) and then create a python [virtual environment](https://docs.python.org/3/library/venv.html).  Make sure that you are using Python 3.9 when you do this:

  ```
  $ cd /path/to/musx_working_directory
  $ python3.9 -m venv venv
  ```

* Your *musx_working_directory* now contains three subdirectories: demos/, doc/ and venv/. Activate your virtural environment by typing this command in your terminal: 
  
  ```
  $ source venv/bin/activate
  ```
  
  Your terminal's `$PATH` variable will now have the venv directory prepended to it so any python calls in this terminal session will be routed to the virtual environment for working with musx.  (Python virtual environments support local, package-specific environments so your computer's global python environment is not affected.)
* Before installing musx make sure that the pip, setuptool and wheel packages are all up-to-date:

  ```
  (venv) $ python3.9 -m pip install --upgrade pip setuptools wheel
  ```

* Install the [matplotlib](https://matplotlib.org/) and [scipy](https://www.scipy.org/) packages:

  ```
  (venv) $ python3.9 -m pip install matplotlib
  (venv) $ python3.9 -m pip install scipy
  ```

  The scipy installation will also install the excellent numpy package.

* Now install musx:

  ```bash
  (venv) $ python3.9 -m pip install musx
  ```
  
* To check that musx is working, start python, import the musx package and call a function:

  ```
  (venv) $ python3.9
  Python 3.9.0 (v3.9.0:9cf6752276, Oct  5 2020, 11:29:23) 
  [Clang 6.0 (clang-600.0.57)] on darwin
  Type "help", "copyright", "credits" or "license" for more information.
  >>> import musx
  >>> musx.keynum('C4')
  60
  >>> exit()
  (venv) $
  ```
  
* That's it! 🤗 You can now start working with musx.  The best way to learn about the system is to run the scripts in musx-demos/ and read the documentation in the doc/ folder.  To run a demo, remain in this directory and specify its module path like this:

  ```
  (venv) $ python3.9 -m demos.gamelan
  ```

  When you are done with your musx session you can deactivate the virtural environment session by typing ` deactivate` in your terminal, or by quitting the terminal.
  
  

## Additional support and customizations

* Install a good editor/IDE for coding in python. Here are two excellent free choices:

  - [Visual Studio Code](https://code.visualstudio.com/) with the [python extension](https://code.visualstudio.com/docs/languages/python)
  - [Pycharm](https://www.jetbrains.com/pycharm/) with the [free student license](https://www.jetbrains.com/community/education/#students).

* You will probably want to play midi files from the terminal.  [fluidsynth](http://www.fluidsynth.org/) is a good choice. On mac or linux you can use [Homebrew](https://brew.sh/) to install it:

  ```
  $ brew install fluid-synth
  ```

  Once installed, you will need to give fluidsynth a sound font to use.  I would suggest starting with the free [MuseScore_General.sf2](ftp://ftp.osuosl.org/pub/musescore/soundfont/MuseScore_General/MuseScore_General.sf2) that ships with [MuseScore](https://musescore.org/en). (Note: there is now a newer, smaller version of this sound font: [MuseScore_General.sf3](ftp://ftp.osuosl.org/pub/musescore/soundfont/MuseScore_General/MuseScore_General.sf3)

  After downloading the sound font move it to a permanent location (e.g. /usr/local/soundfonts) and then pass that pathname to fluidsynth when you play a midi file:

  ```
  $ mv MuseScore_General.sf2 /usr/local/soundfonts
  $ fluidsynth -iq -g2 /usr/local/soundfonts/MuseScore_General.sf2 mymidifile.mid
  ```

  Since that command is pretty long you might want to add an alias in your .bashrc file:

  ```
  alias fs="fluidsynth -iq -g2 /usr/local/soundfonts/MuseScore_General.sf2"
  ```

  With that alias in effect, to play a midi file you just type:

  ```
  fs mymidifile.mid
  ```

  

​	—Rick Taube


# Installing musx

This document explains how to install musx in a Python [virtual environment](https://docs.python.org/3/library/venv.html).  A virtual environment is an independent Python installation dedicated to a specific project (such as musx) without affecting your computer's global Python environment.  Highly recommended!

0) The musx package requires Python 3.9 or higher.  You can download the most recent releases of Python from https://www.python.org/downloads/. Once downloaded, double-click the installation package to install Python on your computer.

1) Open your computer's terminal application, create a directory dedicated to working with musx, then cd into your new workspace (note: the $ represents the terminal's prompt, do not type this as part of your command):

  ```
  $ mkdir ~/projects/mymusx
  $ cd ~/projects/mymusx
  ```

2) Call Python 3.9 or higher and create a virtual environment (venv) for musx:

  ``` 
  $ python3.10 -m venv venv
  ```

3) Activate the musx virtual environment. Once activated you will see the name of your environnment (venv) prepended to each terminal prompt:

  ```
  $ source venv/bin/activate
  (venv) $
  ```

4) With venv activated you can use the generic 'python' command to invoke the correct Python version:

  ```
  (venv) $ python
   Python 3.10.6 (v3.10.6:9c7b4bd164, Aug  1 2022, 17:13:48) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
   Type "help", "copyright", "credits" or "license" for more information.
   >>> quit()
   (venv) $
  ```

5) Make sure venv will use the latest versions of pip, setuptools and wheel:

  ```
  (venv) $ python -m pip install --upgrade pip setuptools wheel
  ```

6) Install the [matplotlib](https://matplotlib.org/), [scipy](https://www.scipy.org/), and [jupyter](https://pypi.org/project/jupyter/) packages to work with musx's interactive demos and tutorials:

  ```
  (venv) $ python -m pip install matplotlib
  
  (venv) $ python -m pip install scipy

  (venv) $ python -m pip install jupyter
  ```

7) Now install the latest musx package and (optionally) copy its documentation and demo directories into your working musx directory:

```
(venv) $ python -m pip install musx

(venv) $ cp -r venv/site-packages/musx/doc ./doc

(venv) $ cp -r venv/site-packages/musx/demos ./demos
```

8) Test that musx works by starting up python, importing the musx package, and calling a function:

```
(venv) $ python
Python 3.10.6 (v3.10.6:9c7b4bd164, Aug  1 2022, 17:13:48) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import musx
>>> musx.keynum('C4')
60
>>> exit()
(venv) $
```
___

That's it! 🤗  The best way to learn about the musx system is to run the scripts in demos/ and read the documentation in the docs/ folder.  To run a demo, you can use the jupyter notebook version or remain in this directory and specify a demo module path like this:

```
(venv) $ python -m demos.gamelan
```

When you are done with your musx session you can deactivate the virtural environment by typing 'deactivate' in your terminal:

```
(venv) $ deactivate
$ 
```

## Additional support and customizations

* Install a good editor/IDE for coding Python. Here are two excellent free choices:

  - [Visual Studio Code](https://code.visualstudio.com/) with the [python extension](https://code.visualstudio.com/docs/languages/python)
  - [Pycharm](https://www.jetbrains.com/pycharm/) with the [free student license](https://www.jetbrains.com/community/education/#students).

* You will probably want to be able to play midi files direectly from the terminal.  [fluidsynth](http://www.fluidsynth.org/) is a good choice, you can use [Homebrew](https://brew.sh/) to install it on mac, linux, and windows:

  ```
  $ brew install fluid-synth
  ```

  Once installed, you will need to give fluidsynth a sound font to use, for example the free [MuseScore_General.sf3](ftp://ftp.osuosl.org/pub/musescore/soundfont/MuseScore_General/MuseScore_General.sf2).

  After downloading the sound font move it to a permanent location on your hard drive, e.g. /usr/local/soundfonts, and then pass that pathname to fluidsynth when you play a midi file:

  ```
  $ mv MuseScore_General.sf3 /usr/local/soundfonts
  $ fluidsynth -iq -g2 /usr/local/soundfonts/MuseScore_General.sf3 mymidifile.mid
  ```

  Since that command is pretty long you might want to add an alias to your .bashrc (or whatever) file:

  ```
  $ alias fs="fluidsynth -iq -g2 /usr/local/soundfonts/MuseScore_General.sf3"
  ```

  With that alias in effect, to play a midi file you just type:

  ```
  $ fs mymidifile.mid
  ```

  

​	—Rick Taube

​		Emeritus Professor, Composition/Theory/CS+Music
​		School of Music
​		University of Illinois Urbana-Champaign
​		Email: taube@illinois.edu


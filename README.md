DigitalPedalBoard
=================

Build your own pedal board and create cool and unique effects to play your guitar or your bass (or other).



##What do I need to know ?

If you just wanna play some musics and don't want to create your own effects or personalize your program you can just follow the installing steps and get started !

But if you want to create your own effects and make your physical pedalboard, you'll need to learn (if you don't know it already):

 - Python 2.7* programming language (take a look at the [Python 2 Official Tutorial](http://docs.python.org/2/tutorial/ "Python 2 Official Tutorial"))
 - Basic knowledge in DSP (Digital Signal Processing), you only have to understand how to make things work and to understand some basic filters.
 - If you want to build a physical pedalboard, you'll need some knowledge in eletrical circuits (no big deal, you won't need to know how to analyze transient ciruits and complicated stuff).
 - If want to build everything by yourself, you may need to know how to program an ARM (we recommend [Arduino](http://arduino.cc/ "Arduino")), but you can choose any ARM you want.

*We used only Python 2.7, we didn't try it out on Python 3, it may work or it may not. You can test by yourself and let us know what happened (we won't pay for any damage this may cause).


##What do I need to buy ?

Actually, if you don't want to, you don't need to buy anything, you can use our program without a pedalboard (but you'll need to use your mouse to change the effects).

But if you want your physical pedalboard, you'll need a ARM board, two foot switches and a expression pedal. And some eletrical components (only some resistors and a variable resistor).
Soon we will post the eletrical components and connections of our pedalboard.


##Installing

Ok, let's head to the main stuff: Making things work !

1. You'll need to install Python 2.7 on your computer. If you have Windows (our sincere condolences) you may want to install Python by using this program: [WinPython](https://code.google.com/p/winpython/ "WinPython"). If you have Linux or Mac, just download Python 2.7 from the official site: http://www.python.org/getit/

2. In this project we used <del>a lot</del> some python packages. Here is a short list of them (you need to install them):
  - matplotlib
  - scipy
  - pyaudio
  - numpy
  - pylab
  - audiolazy
  - wx
  - pickle
  - pyserial
  
  Some of them are included in WinPython installation, you can see that by opening the "WinPython Control Panel" program.

3. If you'll use Arduino, install the [Arduino Software](http://arduino.cc/en/Main/Software "Arduino Software"). If you are using other ARM board, install the software.

Now you have everything you need to get started.



##Getting Started

Start the gui.py program (python gui.py), you'll see something like this:

![alt-text](https://github.com/RicardoBoccoliGallego/DigitalPedalBoard/blob/master/screenshots/initial_screen.png?raw=true)


In the middle-left area we have our effects. We separated them in four categories, you can change that if you want, but it isn't so important.
A effect has 3 things: Its name, a checkbox (you can activate or desactivate) and a button to edit its parameters.

In the right area we have the buttons previous,next,stop and play. The next and previous buttons are used to change effects when you are in preset mode. We also have two graphs which show the input and the output audio.

To start testing, plug your guitar or bass in your computer (and configure it as the main audio input) or use your microfone and press the play button. Pretty cool, right ?

Know, try out applying some effects by pressing its checkboxes (we recommend to start with the echo chaging the echo time to 1 second)

The program has basically 3 modes: Regular Mode (the one we were using), Preset Mode and Preset Editing Mode.

####Regular Mode


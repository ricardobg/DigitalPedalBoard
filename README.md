DigitalPedalBoard
=================

Build your own pedal board and create cool and unique effects to play your guitar or your bass (or other).



##What do I need to know ?

If you just wanna play some musics and don't want to create your own effects or personalize your program you can just follow the installing steps and get started !

But if you want to create your own effects and make your physical pedalboard, you'll need to learn (if you don't know it already):

 - Python 2.7* programming language (take a look at the [Python 2 Official Tutorial](http://docs.python.org/2/tutorial/ "Python 2 Official Tutorial"))
 - Basic knowledge in DSP (Digital Signal Processing), you only have to understand how to make things work and to understand some basic filters
 - AudioLazy package: [AudioLazy](https://github.com/danilobellini/audiolazy "AudioLazy")
 - If you want to build a physical pedalboard, you'll need some knowledge in eletrical circuits (no big deal, you won't need to know how to analyze transient ciruits and complicated stuff)
 - If you want to build everything by yourself, you may need to know how to program a microcontroller (we recommend [Arduino](http://arduino.cc/ "Arduino")), but you can choose any microcontroller you want


We haven't translated everything to English yet, so if you know some Portugues, it would be very helpful.


*We used only Python 2.7, we didn't try it out on Python 3, it may work or it may not. You can test by yourself and let us know what happened (we won't pay for any damage that this may cause).


##What do I need to buy ?

Actually, if you don't want to, you don't need to buy anything, you can use our program without a pedalboard (but you'll need to use your mouse to change the effects).

But if you want your physical pedalboard, you'll need a microcontroller (like Microchip PIC, ARM and Atmel AVR), two foot switches and a expression pedal. And some eletrical components (only some resistors and a variable resistor).
Soon we will post the eletrical components and connections of our pedalboard.


##Installing

Ok, let's head to the main stuff: Making things work !

1. You'll need to install Python 2.7 on your computer. If you have Windows (our sincere condolences) you may want to install Python by using this program: [WinPython](https://code.google.com/p/winpython/ "WinPython"). If you have Linux or Mac, just download Python 2.7 from the official website: http://www.python.org/getit/

2. In this project we used <del>a lot</del> some python packages. Here is a short list of them (you need to install them):
  - matplotlib
  - scipy
  - pyaudio
  - numpy
  - pylab
  - audiolazy
  - wxPython
  - pyserial
  
  Some of them are included in WinPython installation, you can see that by opening the "WinPython Control Panel" program.

3. If you'll use Arduino, install the [Arduino Software](http://arduino.cc/en/Main/Software "Arduino Software"). If you are using other microcontroller, install the required software.

Now you have everything you need to get started.



##Getting Started

Start the gui.py program (python gui.py), you'll see something like this:

![alt-text](/screenshots/initial_screen.png)


In the middle-left area we have our effects. We separated them in four categories, you can change that if you want, but it isn't so important.
A effect has 3 things: Its name, a checkbox (you can activate or desactivate) and a button to edit its parameters.

In the right area we have the buttons previous, next, stop and play. The next and previous buttons are used to change effects when you are in preset mode. We also have two graphs which show the input and the output audio.

To start testing, plug your guitar or bass in your computer (and configure it as the main audio input) or use your microphone, press the play button and listen. Pretty cool, right ?

Now, try out applying some effects by pressing its checkboxes (we recommend to start with the echo and chaging the echo time to 1 second).

The program has basically 3 modes: Regular Mode (the one we were using), Preset Editing Mode and Preset Mode. Below we'll explain them.

####Regular Mode

If you just want to test the effects, this is the mode for you ! It allows you to activate and desactivate effects. When you start the program, this mode will be active. If you are in other mode and want to use this mode, just go to the menu Preset -> Back.


####Preset Editing Mode

This mode is to edit and create presets. If you don't know what a preset is: presets are lists of lists of effects. In other words, you'll have a numbered list (0,1,2,3,..) and any position of the list contains some effects that will be applied when you are in this position (this is very useful for playing songs). This mode isn't complicated, you can go to this mode by 3 ways: File -> New Preset, File -> Load Preset, Preset -> Edit Preset.
When you are in this mode, you'll see a numbered list in the right area. You can press the next or previous button to navigate and when you are in the last position if you press next, you'll create a new position. You can also change the position by using your mouse. When you select a position, you'll only need to select the effects you want to apply and change its parameters.


####Preset Mode

This mode plays a preset. You can see the applied effects and go to the next or to the previous position of the preset.
To go to this mode, you can press the play button when editing your preset or go to Preset -> Play Preset.


You can also save your presets and share them if your friends !


##Making your own effects

To create your own effects, you'll only need to edit the filters.py file. Open it on a text editor and start learning, it contains some effects which we created.
The basic structure of an effect is:
```python
def signal_processing_function(input, params):
    ...
    ...

def effect_information(params=default_values):
    dictionary = {u"parameter_1_name":(default_1_value,data_1_type,(min_1_value,max_1_value))
    , u"parameter_2_name":(default_2_value,data_2_type,(min_2_value,max_2_value))}
    instance = Filtro(signal_processing_function, dictionary, u"FilterName", use_expression_pedal)
    return instance
```

The first function (`signal_processing_function`) is the function that will receive the input, apply the effect and return the output. You can do it in two ways: return the entire processed signal or process sample by sample (you'll have to write `@tostream` before the function and iterate over the input samples). Here we have two examples:
```python
def multiply_entire_signal(input, number):
   return input * number

@tostream
def skip_samples(input, skip_rate):
   i = 0
   for sample in input:
      if i == skip_rate
         i = -1
         yield sample
      i+=1
```

The second function `effect_information` defines some information about the effect. It defines the effect name, its parameters and if it uses (True) or not (False) the expression pedal. When you use the expression pedal you'll need to declare in the `signal_processing_function` a variable that will contain that data, and it must be the first variable after the input. Be aware that the pedal variable is a `ControlStream` (take a look at the AudioLazy documentation) and its value is a float that ranges from 0 to 1.


After creating your <del>Hello World</del> cool effects, you'll need to add them to your filter's list, in the filters.py file, try to find something like this:
```python
filtros = {u"Basic Effects": (passa_altas,passa_baixas,passa_tudo, amplificador, filtro_corta)
          , u"Limiters": (limitador,compressor,filtro_expander)
  
              , u"Distortions": (dist_wire,filtro_senoide_var,filtro_senoide, 
              filtro_mult_env, filtro_res)
              , u"Delays": (eco, filtro_delay_variavel, o_flanger)                
              }
```

It's a dictionary that contains `"effect_group": (effect1,effect2,effect3,...)` You can create a new group or add your effects to an existing group. What you need to add is just the name of the function that contains information about your filter.

Now you are ready to go, start the gui.py program and test your own effects !


##Setting your Microcontroller

Now, let's head to the physical pedalboard. We'll assume that you already have the circuit working (as we said, soon we'll post our circuit schematic). The python file that handles the communication with the Arduino is the serialcom.py.
That file uses the Serial port to get the data, so be sure to program your microcontroller to send data through Serial port using the following code: 
(identification,value). Where identification can be:

1: One of the foot switches is pressed, and the value can assume 1 (go to next effect) or 2 (go to previous effect).

2: The expression pedal state changed. The value can assume any integer between 0 and `limiar_superior_pedal` (which you can define).


####Arduino
You'll find the Arduino code in ArduinoProject/ArduinoProject.ino. You can change the code, but be sure to connect the wires to the correct pins. When you open the Arduino Software, take a look at the Serial Port the Arduino is connected to and go to the serialcom.py file and in the `__init__` function change `porta='COM8'` to `porta='ARDUINO_PORT'`, usually on Windows the port can be COM9,COM12,... and on Linux you'll have a text like this: '/dev/tty...'. You'll also need to test the maximum value that the Arduino is sending (you can figure out that by opening the Serial Console in the Arduino Software and pressing the expression pedal as hard as you can), when you have that value, change the `limiar_superior_pedal=650` to `limiar_superior_pedal=MAX` where MAX is that value you just got.


####Other Microcontrollers
Be sure to send the data by the Serial port. After that, figure out what Serial port you microcontroller is connected to, the data rate and the maximum value that the expression pedal is sending. Now you'll use these values to set the default values of the `__init__` function.


You can change the way to send data to something cooler (like wireless communication or USB), to do that you'll only need to modify the serialcom.py file (and yes, its name will lose all its sense of being so). You'll also need to understand that file to make the right function calls and update everything that must be updated.

Your microcontroller now should be ready, start the gui.py program, play a preset and try it out !


##Advanced Topics
You changed everything you could changed, created an awesome pedalboard with satelite communication, made more than 8000 effects, what now ?
Here'll briefly explain what the project files we didn't explain do and what you could improve.

####data.py
This files handles both saving and loading data using the pickle package. Whenever you are in Regular Mode and change any filter's parameter, the program will take a snapshot of all the filters and save it in the default.data file. When you start the program, it loads that default.data filters and update the default parameters of all filters.

This file also saves and loads your presets. When you change any filter's parameter while on Edit Preset Mode, this change will only be saved on its .preset file, in other words: this change will not be saved in the default.data.

What you may improve ? Maybe saving the presets in the cloud. Making possible to download, upload, rate and share presets would be pretty cool.


####lib.py
This file handles some unrelated stuff: the `FloatSlider` class (which we didn't make, in the source code you can see the author), `DataGen` class and the `MyThread` class (yes, we completely forgot to change the name to a useful name).
- The `FloatSlider`, as its name implies change the standard `Slider` class of the wxPython package to accept float values.
- The `DataGen` returns a tuple with two float values: the input and the output audio.
- The `MyThread` controls the update of the input and the output graphs.


What you may improve ? You could improve the performance of `DataGen` and `MyThread`, which is a critical point of the program.

####player.py
This file handles the audio (both recording and playing). Basically, it contains functions to play, pause and change filters while playing.

What you may improve ? You may want to change the `ChangeableStream` class (yes, change the changeable) and make it faster by updating the `self.last` in the same rate of the graph update rate.


####gui.py
This is the main file, the king of the kings. It has over one thousand lines and despite to create the GUI (General User Interface), it also connects all the files.

This file is the one that may need more improvement than the others. And what that could be ? You could improve the interface, make it brighter, prettier and faster. You could also create new features like user defined effects group and more menus and buttons !


We've already introduced the other three files: filters.py, serialcom.py, ArduinoProject/ArduinoProject.ino in previous sections, so take a look at them.


----

Copyright (C) 2013 Daniel Ken Fujimori Killner, Gabriel Moura Vieira Martinez,Rafael Alves de Araujo Sena, Ricardo Boccoli Gallego, Danilo de Jesus da Silva Bellini.

License is GPLv3. See COPYING.txt for more details.


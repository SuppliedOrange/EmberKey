# EmberKey

<br>

# Versions:
**This app is only compatible with Python versions 3.6 to 3.9** <br>

If you don't have python 3.6 - 3.9, You can download the most reliable release [Python 3.7.9](https://www.python.org/downloads/release/python-379/) or the latest release [Python 3.9.10](https://www.python.org/downloads/release/python-3910/).

<br>
I have downloaded Python 3.7.9 as an example here, you can download anything else just replace `python3.7` with just `python` or `python3.9` etc

<br>

## Downloading Python 3.7.9 <br>
• Firstly, download the [executable installer](https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe). Run it and enable the `Add to path` option before installing <br>
![Enabling path option At the bottom of the screen](/assets/AddToPathImage.png)

• After installing it, open up the project folder and open up command prompt in that directory by typing "cmd" in the address bar. Try typing `python3.7 -V` to see if the version number matches with *3.7.9*.
![Typing "cmd" in address bar](/assets/AddressBarImage.png)
![Typing "python3.7 -V" in the cmd prompt](/assets/CheckPythonVersion.png)

• You should use the `tutorialInstaller.bat` in Batch Files folder to install files. If you still keep running into errors don't worry, there's a fix. You need to manually input these lines:
```
python3.7 -m pip install PySimpleGUI
python3.7 -m pip install keyboard
python3.7 -m pip install playsound
python3.7 -m pip install pillow
```

Done! You have successfully installed Python 3.7.9 and initialized the repo. Give yourself a pat on the back.

To run the program, simply type: <br>
 `python3.7 hotkey_main.py`

<br>

# Installing the source code
If you followed the tutorial above, skip this step.

To install EmberKey, first download the repository directly through the green button that says "Code" on the repository or by using <br>
    `git clone https://github.com/SuppliedOrange/EmberKey`

Then open up a terminal in the repository (You can type "cmd" in the address bar) and install the required modules through `requirements.txt`.

Use command <br> 
`python/py/python3 -m pip install -r requirements.txt` <br>
You can also use `installer.bat` in the repository. It does the same thing.

There are plenty of reasons this command may fail. This can be because you don't have python or pip in your PATH. You simply need to install all the modules in `requirements.txt` (except python3-tk unless you're on linux) and you can do it in anyway you like.

<br>

# Introduction
EmberKey is a tool used to generate [hotkeys][1] that help with daily utility or simply for entertainment. Emberkey is a lightweight, fast and easy to use hotkey app built in Python. Create hotkeys with up to 4 unique functions.

[1]: <https://www.dictionary.com/browse/hotkey#:~:text=or%20hot%20key&text=an%20assigned%20key%20or%20sequence,Also%20called%20shortcut%2C%20keyboard%20shortcut%20.>  "hotkeys"

<br>

# This guide contains:
[Main Menu](#main-menu)

[Settings](#settings)

[Adding Hotkeys](#adding-hotkeys) 

[Removing Hotkeys](#removing-hotkeys)   

[config.json](#config-json-file)
## Main Menu:
The main menu consists of the current hotkeys, as the ones specified in the config.json file.

## Settings:
The settings tab consists of the following options: <br>
`GUI Accent` -> This allows you to change the theme of the app. There are two themes, Dark and Light mode.

`No-Sound Warning` -> When you set a hotkey to play a sound, it looks for the file path for the audio you provided. If the file were to be moved into a new directory, renamed or deleted then this operation would fail and no sound would be played. If you enable this setting then whenever the sound fails to play, you'll hear "Audio Failure".

`Reload All Hotkeys` -> This will stop all active hotkeys and start them again.

`Erase All Hotkeys` -> This will erase all the hotkeys.

`GIF pop-ups` -> Use GIFs in place of pop-ups as success messages wherever possible.

`Check GIF compatibility` -> You'll have to check if your Python version supports PIL or pillow and use the module accordingly. If you fail the compatibility test please do not attempt to enable GIFs.

`Show Console` -> Throughout the functioning of the app, multiple logs are printed. This button will open a debugger that shows everything that is printed to the console.



## Adding Hotkeys

Moving to the Hotkey Editor tab, you'll see option "Add hotkey".

`Setting the hotkey:` You'll be prompted to enter a valid hotkey. A valid hotkey is all-lowercase and seperated by '+' if there is more than one character. Suppose you wanted your hotkey to trigger upon pressing Alt and 0. Your input would be "alt+0". 

`Selecting the mode:` After finishing this step, you'll be prompted to select a hotkey mode. The hotkey mode is what should happen after the hotkey is pressed. There are 4 modes, one to execute a file, one to play a sound, one to type a sentence and lastly to press a specific key. Your next prompt will be different based on what is selected based on this window.

### Modes:

`Executing a file: ` If you wanted to execute a file, you would be prompted to select the file you would like to execute. After selecting, the path of this file is stored in the config.json file. If you changed this file's location, the hotkey would no longer work. You will have to remove the hotkey and add it again with the appropriate file path.

`Playing audio:` If you wanted to play a sound you will have to select a .mp3 file. Just like the above case, this file's path is stored in the config.json file. If you change the file path or rename the file, you will need to remove and re-add the hotkey with the correct path.

`Typing a sentence/word:` If you wanted the hotkey to type a sentence, or rather send a series of keys in quick succession through your keyboard to emulate typing, you would be prompted to enter a sentence or word. This textbox has no limit. Upon pressing the hotkey, the letters will be pressed through your keyboard to write the sentence. Just make sure you have a text box selected to ensure nothing weird happens.

`Remapping a key:` If you wanted to remap a key, let's say J + Alt to Windows/Command Key, you will need to enter "j+alt" in the first text-box and "windows" in the second text-box. Now pressing J + Alt will activate the Windows/Command Key. Easy remapping! Also note that some keys like "windows" will also work on Max as Command, Ubuntu as Superkey etc. Now I must admit that I may be cheating on the word "remap" because it does not actually prevent the initial key from being activated. I did not want to block the key as that would require me to use the winapi which can go very wrong in some cases.

## Removing Hotkeys

In the Hotkey Editor tab you'll see button "Remove Hotkey". Upon pressing the button you'll be greeted with a window that shows all active hotkeys. Under each hotkey is a button "Remove Hotkey". Clicking on this button removes the hotkey above it. Hotkeys also have IDs assigned to them, they're basically the index number of the hotkey from the config.json file.

## Config JSON File
Please don't try to change the JSON unless you know what you're doing. You may trigger an infinite loop of PySimpleGUI errors that can only be dismissed by ending the process through task manager.

The config.json consists of values:

<b>"theme"</b> -> `"DarkGrey8" | "reddit"` <br>
    Switch between Dark mode and Light mode

<b>"defaultFont"</b> -> `"Bahnschrift" | Any font name string`
    Option to change font, incase your computer does not have this font. You may need to use this if you use win10 > or another OS.

<b>"addProcessData"</b> -> `["hotkey","hotkey type", "hotkey params"]` <br>
Set the values to send to the "hotkey" key (done by system)

    {hotkey} can be a+shift,0+space etc..
    {hotkey type} can be "opens" | "writes" | "plays" | "remaps"
    {hotkey params} depends on the type of hotkey. It can be a file path, plain text or a key combination

<b>"hotkeys"</b> -> `[ ["hotkey","hotkey type","hotkey params"], ... ]` <br>
The values recieved from the "addProcessData" key

<br>

# Credits:
Made for a school assignment by `Dhruv`, `Johan` and `Bhumika` from Class 11 A.
This project was made in pure Python code and was built in just 4 days.
This project was made alongside our main project, Axelia, a sci-fi RPG game built in Godot Engine.

<br>

# Known Issues:

`Sound Failure:`<br>
Some MP3 files will fail to play. I believe this has something to do with the file name. Try renaming your file to something simple like "aVeryCoolAudioFile.mp3". playsound happens to be a very unreliable library. A nodejs package port was possible to fix this but since we wanted to keep the project 100% Python we did not use any other language.

`Remapped key does not press:` <br>
Now this has been on my radar for a while. The keyboard module recieves the function call and performs accordingly. However while accessing `_os_keyboard.press` (from the Key Controller) there seems to be a silent dll.call error. dll.call as far as I know is a winapi method to call a mouse function or key for the windows api. When I was debugging, the key suddenly started to work. I have come to conclusion that using `identifier keys` may be the problem. Remapping keys like shift,alt,enter etc can cause this. I would recommend remapping something simple like "p+z" to press "windows" or something to solve this issue temporarily. I'll have to see the Key Controller documentation for this.

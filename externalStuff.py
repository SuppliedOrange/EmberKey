
#Functions that can be used in general python.
#These functions are put here to avoid taking up space in the main file.

import json
from minimize import minimize
import keyboard
import copy
import ntpath
from playsound import playsound
import os
import PySimpleGUI as sg

legalhotkeys = list("`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm./!@#$%^&*()_{}|:\"<>?") # main, typable keys.
legalhotkeys.extend(['f1','f2','f3','f4','f5','f6','f7','f8','f9','f10','f11','f12','space','backspace','tab','enter','delete','pageup','pagedown','home','esc','comma','plus','down','up','left','right','print screen','scroll lock','insert','num lock','caps lock','play/pause media',]) # extra keys
legalhotkeys.extend(list(keyboard.all_modifiers)) #modifiers
loadedHotkeys = []

def openAndCloseWindow(window): #close and open the window very quickly to make it appear in the task bar
    minimize(window) 
    window.normal()

def loadData():
    data = open('config.json')
    data = json.load(data)
    return data
def updateData(updateKey,updateValue):
    data = loadData()
    with open("config.json", "w") as jsonFile:
        data[updateKey] = updateValue
        json.dump(data, jsonFile)
def check_valid_hotkey(string):
    string = str(string).lower()
    string = string.split("+")
    newString = []
    repeatChecker = []
    for i in string:
        if not len(i):
            return None
        if not i == '+':
            i = keyboard.normalize_name(i)
        if i in keyboard._canonical_names.canonical_names.values():
            legalhotkeys.append(i)
        if i not in legalhotkeys or i in repeatChecker:
            return None
        repeatChecker.append(i)
        newString.append(i)
    return " + ".join(newString)
def isValidHotkey(value,data):
    value = value.lower()
    defaultTextColor = "black" if data['theme'] == "reddit" else "white"
    isValid = ["Invalid Format",'red',False] if not check_valid_hotkey(value) else [check_valid_hotkey(value),defaultTextColor,True]
    if (isValid[2]):
        for i in data['hotkeys']:
            if value == i[0]:
                isValid = ["Hotkey already exists",'red',False]
    return isValid
def createReusableLayout(Layout): # this is super important for pysimplegui. you'll be able to reuse layouts by replicating it, or as i did it here- using copy.deepcopy()
    LayoutList = [Layout]
    NewLayout = copy.deepcopy(Layout)
    LayoutList.append(NewLayout)
    LayoutList.pop(0)
    return LayoutList[0]

def get_hotkeys_removal(): #get hotkeys for removal
    data = loadData()
    hotkeys = data['hotkeys']
    defaultFont = data['defaultFont']
    if not hotkeys:
        return [[sg.Text("You have no hotkeys to remove!",font=(defaultFont,20))]]
    hotkey_models = []
    id = 0
    for i in hotkeys:
        verbs = {
            'opens': "will open",
            'plays' : 'will play sound',
            'writes' : "will type out",
            'remaps' : "will instead output"
        }
        params = i[2] if not i[1] in ['opens','plays'] else ntpath.basename(f'{i[2]}')
        hotkey_string = f'\n{i[0]} {verbs[i[1]]} {params}\n\n'
        hotkey_ID = 'Hotkey ID: ' + str(id) + '\n'
        hotkey_models.append([sg.T('')])
        hotkey_models.append([sg.Text(hotkey_ID + hotkey_string,font=(defaultFont,15))])
        hotkey_models.append([sg.Button("Remove this Hotkey",key=f'RemoveHotkeyWithID {id}',size=(17,1))])
        id += 1
    return hotkey_models

def get_hotkeys():
    hotkeys = loadData()["hotkeys"]
    hotkey_string = "You have no hotkeys yet! Add your first hotkey"
    if not len(hotkeys):
        return hotkey_string
    hotkey_string = ''
    for i in hotkeys:
        params = i[2] if not i[1] in ['opens','plays'] else ntpath.basename(f'{i[2]}')
        hotkey_string += f'\n{hotkeys.index(i) + 1}: {i[0]} {parseVerbs(i[1],"verb")} {params}\n\n'
    return hotkey_string

def play_sound(sound_path):
    raw_sound_path = r'{}'.format(sound_path)
    try:
        playsound(raw_sound_path)
    except Exception as e:
        print("[ERROR] Could not find the audio file",raw_sound_path,"\nYou may have moved/deleted this file. If that's not the problem, re-add this hotkey\nError: ",e)
        if (loadData()['warnNoSound']):
            playsound('./assets/incorrectsound.mp3')

def keyboardWrite(textToWrite='ApplicationName'):
    keyboard.write(textToWrite)

def open_file(file_path):
    raw_file_path = r'{}'.format(file_path)
    try:
        os.startfile(raw_file_path)
    except:
        print("[ERROR] Could not find the file",raw_file_path,"\nYou may have moved/deleted this file. If that's not the problem, re-add this hotkey")

def runMappedKey(key):
    print("pressing " + str(key))
    try:
        keyboard.send(str(key))
    except:
        print('[ERROR] Could not press key',key)

def parseVerbs(verb,parsetype=None):
    parsed_verbs = {}
    if not parsetype: return
    if parsetype == 'function':
        parsed_verbs = {
            'plays' : play_sound,
            'writes' : keyboardWrite,
            'opens' : open_file,
            'remaps' : runMappedKey
        }
    elif parsetype == 'verb':
        parsed_verbs = {
            'opens': "will open",
            'plays' : 'will play sound',
            'writes' : "will type out",
            'remaps' : "will instead output"
        }
    return parsed_verbs[verb]

def addHotkey(hotkey,callback, hotkeyParams):
    callback = parseVerbs(callback,'function')
    newHotkey = keyboard.add_hotkey(hotkey,callback, args = ([hotkeyParams]))
    loadedHotkeys.append(newHotkey)

def removeHotkey(hotkeySecret,force=False):
    if (type(hotkeySecret) == 'int'):
        hotkeySecret = loadedHotkeys[hotkeySecret]
    
    hotkeyDB = loadData()['hotkeys']
    indexOfHotkey = loadedHotkeys.index(hotkeySecret)
    del hotkeyDB[indexOfHotkey]
    if force: # If we're forcing it, remove it from the JSON too
        print('[LOG] Force removing the key')
        updateData('hotkeys',hotkeyDB)

    try:
        keyboard.remove_hotkey(hotkey_or_callback=hotkeySecret)
        loadedHotkeys.remove(hotkeySecret)
    except:
        print("[LOG] Could not remove hotkey. Hotkey was probably never loaded\nHotkey:",hotkeySecret)
        

def removeAllHotkeys(force=False): # removing all hotkeys and loading all hotkeys without force is same as reloading all hotkeys
    if not loadedHotkeys: return
    print('[LOG] User removed all hotkeys!')
    if not force:
        for i in loadedHotkeys:
            removeHotkey(i)
    else: # this erases all data
        print('[LOG] User has force deleted!')
        updateData('hotkeys',[])

def loadAllHotkeys():

    try:
        hotkeyData = loadData()['hotkeys']
    except Exception as e:
        print('[ERROR] Error hit while loading data from JSON file. Possibly blank.')
        askClearJSON()

    print("[LOG] Attempting to load all hotkeys, this is the hotkey data:")
    print(hotkeyData)

    if not hotkeyData: return

    for hotkey in hotkeyData:
        try:
            addHotkey(hotkey[0],hotkey[1],hotkey[2])
        except Exception as e:
            print("[ERROR] Error hit while loading hotkeys!\nError:",e)
            askClearJSON()
        print(f'[LOG] Loaded hotkey {hotkey[0]} with ability "{hotkey[1]}" with params [{hotkey[2]}]')
    print('[LOG] Loaded all hotkeys')

def askClearJSON():
    deleteData = sg.popup_yes_no("Looks like you hit an error while loading the app. \nThis can be caused by the JSON file.\nWe can fix this by clearing your data entirely.\nWould you like to clear data?")
    if deleteData == "Yes":
        data = {
            "theme": "reddit",
            "hotkeys": [],
            "addProcessData": [],
            "defaultFont": "Bahnschrift",
            "warnNoSound": False,
            "useGIF": False
        }
        with open("config.json", "w") as jsonFile:
            json.dump(data, jsonFile)
        print("[EMERGENCY LOG] Dumped all data. Loaded JSON data to defaults.")
        exit(0)

    else:
        exit(1)

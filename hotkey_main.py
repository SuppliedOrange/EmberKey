#!/usr/bin/env python 3.7.9

import PySimpleGUI as sg
import json
import keyboard
from externalStuff import legalhotkeys, loadedHotkeys, openAndCloseWindow, loadData, updateData, isValidHotkey, createReusableLayout, get_hotkeys, check_valid_hotkey,addHotkey, loadAllHotkeys, removeAllHotkeys, get_hotkeys_removal, removeHotkey
import webbrowser

loadAllHotkeys()
linkToDocs = 'https://github.com/SuppliedOrange/PythonHotkeyAppThing'
hotkeyIcon = 'emberkeyLogo.ico'


def debugWindow():
    logging_layout = [
        [sg.Text("Everything we log will appear here")],
        [sg.Output(size=(60,15), font='Courier 8', expand_x=True, expand_y=True,key="debuggerConsole")]
    ]
    window = sg.Window("Debugger",createReusableLayout(logging_layout), element_justification='c',keep_on_top=True,icon=hotkeyIcon)
    window.finalize()

def successWindow(loadSentences=None):
    import random
    from PIL import Image, ImageTk, ImageSequence

    loadingWindowLayout =  [
    [sg.Image(key = 'gif')],
    [sg.Text("Done!",font = (loadData()['defaultFont'],40), justification='c',key='loadingText',auto_size_text=True)]
    ]
    window = sg.Window("Success Message",createReusableLayout( loadingWindowLayout ),element_justification='c', margins=(0,0),element_padding=(0,0),finalize=True, auto_size_text=True,keep_on_top=True,modal=True,icon=hotkeyIcon)
    window.make_modal()

    window['loadingText'].expand(True,True,True)
    gif = 'yay'

    interframe_duration = Image.open(f'./assets/{gif}.gif').info['duration']

    loadSentences = loadSentences or {
                                        3: "Success ＼(^o^)／",
                                        6: "Operation successful!!",
                                        9: "Python ftw :100:"
                                    }

    loadCounter = 0

    while(True):
        toBreak = False
        loadCounter+=1
        for frame in ImageSequence.Iterator(Image.open(f'./assets/{gif}.gif')):
            event,values = window.read(timeout=interframe_duration)
            if(event==sg.WIN_CLOSED):
                window.close()
                toBreak = True
                break
            window['gif'].update(data=ImageTk.PhotoImage(frame))

        textUpdate = 'Success ＼(^o^)／'

        for i in loadSentences.keys():
            if i <= loadCounter:
                textUpdate = loadSentences[i]

        window['loadingText'].update(textUpdate)
        loadCounter = 0 if loadCounter > 10 else loadCounter

        if (toBreak):
            break
        
def addedHotkeyMessage (msg="Added Hotkey!"): # success window with no gif
    loadingWindowLayout =  [
    [sg.Image("./assets/successCatto.png")],
    [sg.Text(msg,font = (loadData()['defaultFont'],40), justification='c',key='loadingText',auto_size_text=True)]
    ]
    window = sg.Window("Success Message",createReusableLayout( loadingWindowLayout ),element_justification='c', margins=(0,0),element_padding=(0,0),finalize=True, auto_size_text=True,keep_on_top=True,modal=True,icon=hotkeyIcon)
    window.make_modal()

    window['loadingText'].expand(True,True,True)

    while True:
            
        event, values = window.read(timeout=100)

        if event in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED,None):
            print("[LOG] Clicked Exit!")
            break

def checkCanUseGIF():
    def failureMessage(error):
        print(error)
        sg.popup("Unfortunately your Python does not support GIFs :(\nError:\n" + str(error))
    try:
        from PIL import Image, ImageTk, ImageSequence
    except Exception as error:
        return failureMessage(error)
    gifWindowLayout =  [
    [sg.Image(key = 'gif')],
    [sg.Text("Your Python version supports GIFs!",font = (loadData()['defaultFont'],40), justification='c',key='supportsMessage',auto_size_text=True)]
    ]
    try:
        window = sg.Window("Success Message", createReusableLayout(gifWindowLayout) ,element_justification='c', margins=(0,0),element_padding=(0,0),finalize=True, auto_size_text=True,keep_on_top=True,modal=True,icon=hotkeyIcon)
    except Exception as error:
        return failureMessage(error)
        
    window['supportsMessage'].expand(True,True,True)
    gif = 'yay'
    
    interframe_duration = Image.open(f'./assets/{gif}.gif').info['duration']
    while(True):
        toBreak = False
        for frame in ImageSequence.Iterator(Image.open(f'./assets/{gif}.gif')):
            event,values = window.read(timeout=interframe_duration)
            if(event==sg.WIN_CLOSED):
                window.close()
                toBreak = True
                break
            window['gif'].update(data=ImageTk.PhotoImage(frame))

        if (toBreak):
            break
    return "Success"

def removeHotKeyWindow():
    
    def genHotkeyRemovalLayout():
        hotkeyRemovalLayout = [
        [sg.Text("My Hotkeys",font=(loadData()['defaultFont'],40))]
        ]
        hotkeyRemovalData = get_hotkeys_removal()
        for i in hotkeyRemovalData:
            hotkeyRemovalLayout.append(i)
        return hotkeyRemovalLayout

    def genWindow(windowLayout):
        windowLayout.append([sg.T('')])
        windowLayout.append([sg.Button('Exit',key='exitHotkeyRemoval',size=(10,1))])
        reusableWindowLayout = createReusableLayout(windowLayout)
        window = sg.Window("Removing Hotkeys", [[sg.Column(reusableWindowLayout,scrollable=True,key='columnHolder',size=(600,400))]] , margins=(0,0),element_padding=(0,0),finalize=True, auto_size_text=True,keep_on_top=False,modal=True, resizable = True,size=(600,400),icon=hotkeyIcon)
        window.make_modal()
        return window
    
    window = genWindow(genHotkeyRemovalLayout())
    window['columnHolder'].expand(True,True,True)

    while True:
        event,values = window.read(100)
        if(event==sg.WIN_CLOSED or event=="exitHotkeyRemoval"):
            window.close()
            break
        
        event = event.split()

        if (event[0] == "RemoveHotkeyWithID"):
            confirmation = sg.popup_yes_no("Are you sure you want to remove the hotkey with ID " + event[1] + "?")
            if confirmation == "Yes":
                removeHotkey(loadedHotkeys[int(event[1])],force=True)
                window.close()
                window = genWindow(genHotkeyRemovalLayout())
                sg.popup("You have successfully removed the hotkey")



def addHotKeyWindow():
    defaultFont = loadData()['defaultFont']
    process = {
         "startWindow1" : True,
         "givenHotkey" : None,
         "startWindow2" : False,
         "givenAction" : None,
         "startWindow3" : False,
         "givenParams" : None
     }

    allKeys = ''
    for i in legalhotkeys:
        allKeys += "\n" + i
    allKeysLayout = [
        [sg.Multiline(allKeys,size=(20,20), font=(defaultFont,16), expand_x=True, expand_y=True, write_only=True)]
    ]
    addHotKeyWindowLayout = [
        [sg.Text('Enter a Hotkey',font=(defaultFont,40))],
        [sg.Input(key='hotkeyInput',focus=True)],
        [sg.Text('Invalid Key',font=(defaultFont,18),key='validator',text_color='')],
        [sg.Text('Examples:',font=(defaultFont,20))],
        [sg.Text('"shift+ctrl+a" -> Press shift, control and A \n"alt+1" -> Press alt and 1\n"enter" -> Press Enter key',font=(defaultFont,11))],
        [sg.Button("Show keys",key="showAllKeys"),sg.Button("Next",key="complete1")]
        
     ]
    selectHotKeyTypeWindowLayout = [
        [sg.Text('I want the Hotkey to...',font=(defaultFont,40))],
        [sg.Button(image_filename='./assets/cattoOpen.png',image_subsample=2,k='openFile'),sg.Button(image_filename='./assets/cattoType.png',image_subsample=2,k='keyboardWrite')],
        [sg.Button(image_filename='./assets/cattoRemap.png',image_subsample=2,k='keyboardRemap'),sg.Button(image_filename='./assets/cattoPlay.png',image_subsample=2,k='playSound')],
        [sg.Text("Current hotkey: Unknown",key='currHotkeyMessage')]
    ]

    firstKey = loadData()['addProcessData'][0] if len(loadData()['addProcessData']) else "f6"

    parameterLayouts = {
        "opens" : [
            [sg.Text("What file would you like to open?",font=(defaultFont,40))],
            [sg.Button("Choose File",key='chooseFile',size=(30,2),focus=True)],
        ],
        "writes" : [
            [sg.Text("What do we write?",font=(defaultFont,40))],
            [sg.Text("By \"writing\", we pass on the letters to your keyboard in quick succession in order. \nSo 'Hello there' would press H,e,l,l,o,space,t.. etc",font=(loadData()["defaultFont"],10))],
            [sg.Input("I love typescript!",font=("Bahnschrift",20),key='writesInput',focus=True)],
            [sg.Button("Done",key="writtenMessage",size=(30,2))]
        ],
        "remaps" : [
            [sg.Text("What key are we remapping?",font=(defaultFont,40))],
            [sg.Input(firstKey,key="keyboardRemapKey1"),sg.Text(" should press "),sg.Input("g",key="keyboardRemapKey2")],
            [sg.Text("Remapping key 'f6' to 'g'",font=(defaultFont,11),key="keyboardRemapValidator")],
            [sg.Text("\nExamples:\n'f1' to 'backspace'\n'up+delete' to 'windows+shift+s' (screenshot)\n'alt+a' to 'ă' (unconventional letter)\n")],
            [sg.Button("Show all keys",key='showAllKeys'),sg.Button("Finish",key="remappedKeys")]
        ],
        "plays" : [
            [sg.Text("What audio would you like to play?",font=(defaultFont,40))],
            [sg.Text(".mp3 files are supported for audio files",font=(defaultFont,15))],
            [sg.Button("Choose File",key='chooseAudioFile',size=(30,2),focus=True)],
        ],

    }
    

    def initializeProcess(chosenValue):
        process["givenAction"] = chosenValue
        currdata = loadData()['addProcessData']
        currdata.append(process["givenAction"])
        updateData("addProcessData",currdata)

    def addProcessWindow(windowName,windowLayout,size_=(None,None)):
        reusableWindowLayout = createReusableLayout(windowLayout)
        window = sg.Window(windowName, reusableWindowLayout , margins=(0,0),element_padding=(0,0),finalize=True, auto_size_text=True,keep_on_top=False,modal=True,icon=hotkeyIcon,size=size_,element_justification='c')
        window.make_modal()
        return window
    
    window = addProcessWindow("Adding Hotkey", addHotKeyWindowLayout)
    data = loadData()

    while True:
        event,values = window.read(100)
        if(event==sg.WIN_CLOSED):
            window.close()
            break

        elif (event == "showAllKeys"):
            addProcessWindow("All possible keys",allKeysLayout)

        elif (event == "complete1"):
            process["givenHotkey"] = str(values["hotkeyInput"]).lower()
            updateData("addProcessData",[process["givenHotkey"]])

        elif (event == "openFile"):
            initializeProcess("opens")
        elif (event == "keyboardWrite"):
            initializeProcess("writes")
        elif (event == "keyboardRemap"):
            initializeProcess("remaps")
        elif (event == "playSound"):
            initializeProcess("plays")


        elif (event == "chooseFile"):
            print("[LOG] Trying to choose a file for new hotkey")
            def askPopUp():
                filePath = sg.popup_get_file('Choose your file', keep_on_top=True)
                if not filePath:
                    print("[LOG] User did not choose a file.")
                    return False
                else:
                    print("[LOG] User chose file: " + str(filePath))
                    proceed = sg.popup_ok_cancel("You chose: " + str(filePath), keep_on_top=True)
                    if proceed == 'cancel':
                        print("[LOG] User cancelled.")
                        pass
                    else:
                        process["givenParams"] = filePath
                        currdata = loadData()['addProcessData']
                        currdata.append(process['givenParams'])
                        updateData("addProcessData",currdata)
                        return True
            v = askPopUp()
            if not v: pass
            if (not loadData()['useGIF']):
                addedHotkeyMessage()
            else:
                import ntpath # we're importing it here because it's a situational module and we don't want to import stuff and possibly sacrifice miliseconds of performance
                filepath = ntpath.basename(process['givenParams'])
                if len(filepath) > 7:
                    filepath = filepath[0:5] + "..." + filepath[len(filepath) - 7: len(filepath)]
                gifMessages = {
                    0: "Hotkey'd " + process["givenHotkey"] + "!",
                    3: "Executes file" + filepath,
                    9: "Don't use it too many times!"
                }
                successWindow(gifMessages)


            
        elif (event == "chooseAudioFile"):
            print("[LOG] Trying to choose a sound file for new audio hotkey")
            def askPopUp():
                filePath = sg.popup_get_file('Choose your file', keep_on_top=True,file_types=(("All Files","*.mp3"),))
                if not filePath:
                    print("[LOG] User did not choose an audio file.")
                    pass
                else:
                    print("[LOG] User chose an audio file: " + str(filePath))
                    proceed = sg.popup_ok_cancel("You chose: " + str(filePath), keep_on_top=True)
                    if proceed == 'cancel':
                        print("[LOG] User cancelled.")
                        pass
                    else:
                        process["givenParams"] = filePath
                        currdata = loadData()['addProcessData']
                        currdata.append(process['givenParams'])
                        updateData("addProcessData",currdata)
                        return
            askPopUp()
            if (not loadData()['useGIF']):
                addedHotkeyMessage()
            else:
                import ntpath # same reason as above
                filepath = ntpath.basename(process['givenParams'])
                if len(filepath) > 7:
                    filepath = filepath[0:5] + "..." + filepath[len(filepath) - 7: len(filepath)]
                gifMessages = {
                    0: "Hotkey'd " + process['givenHotkey'] + "!",
                    3:  "Trigger audio " + filepath + " with ease",
                    9: "Try it out!"
                }
                successWindow(gifMessages)
        
        elif (event == "writtenMessage"):
            writtenMessage = values['writesInput']
            process["givenParams"] = writtenMessage
            currdata = loadData()["addProcessData"]
            currdata.append(process["givenParams"])            
            updateData("addProcessData",currdata)
            if (not loadData()['useGIF']):
                addedHotkeyMessage()
            else:
                gifMessages = {
                    0: "Hotkey'd " + process["givenHotkey"],
                    3: process["givenParams"],
                    9: "Try it out on a text box!"
                }
                successWindow(gifMessages)

        elif (event == 'remappedKeys'):
            keys = [values['keyboardRemapKey1'],values['keyboardRemapKey2']]
            process["givenParams"] = keys
            currdata = loadData()['addProcessData']
            currdata.append(process["givenParams"])
            updateData("addProcessData",currdata)
            print(f"Hotkey Added!\n{keys[0]} key will now behave as {keys[1]}")
            if (not loadData()['useGIF']):
                addedHotkeyMessage()
            else:
                gifMessages = {
                    0: "Remapped " + keys[0] + "!",
                    3:  keys[0] + " = " + keys[1],
                    9: "Try pressing " + keys[0]
                }
                successWindow(gifMessages)


        #the first window process has already started
        #first process, to give hotkey
        if (not process["givenHotkey"]):
            isValid = isValidHotkey(values['hotkeyInput'],data)
            window['validator'].update(isValid[0],text_color=isValid[1])
            window["complete1"].update(disabled= not isValid[2])

        # upon completion of first process, open the second window.
        elif (process["givenHotkey"] and not process["startWindow2"]):
            print('[LOG] User is switching to window 2 after selecting hotkey',process['givenHotkey'])
            window.close()
            window = addProcessWindow("Selecting hotkey type",selectHotKeyTypeWindowLayout,size_=(590,600))
            process["startWindow2"] = True
            window["currHotkeyMessage"].update("Current hotkey: " + loadData()['addProcessData'][0])
        
        #after starting window 2, ask user for type of hotkey
        elif (process["givenAction"] and not process["startWindow3"]):
            print('[LOG] User is switching to window 3 after selecting action',process['givenAction'])
            window.close()
            window = addProcessWindow("Adding parameters",parameterLayouts[process["givenAction"]])
            process["startWindow3"] = True
            if (process['givenAction'] == "remaps"): #if chosen type is remap, update the remap window to include current hotkey.
                window["keyboardRemapKey1"].update(loadData()['addProcessData'][0])
            
        # if the process is repmapping, repeatedly update the validation text.   
        elif(process["startWindow3"] and process['givenAction'] == 'remaps' and not process["givenParams"]):
            def validRemapKey(key1,key2):
                for key in [key1,key2]:
                    key = key.strip()
                    if not len(key):
                        return [f"No key provided for {'Key 1' if key == key1 else 'Key 2'}",False]
                    if not check_valid_hotkey(key):
                        return ["Invalid keys for " + key,False]
                return [f'Remapping key "{key1}" to key "{key2}"',True]
            key1,key2 = values['keyboardRemapKey1'],values['keyboardRemapKey2']
            validRemapCombo = validRemapKey(key1,key2)
            defaultTextColor = "black" if data['theme'] == "reddit" else "white"
            color = defaultTextColor if validRemapCombo[1] else 'red'
            window['keyboardRemapValidator'].update(validRemapCombo[0],text_color=color)
            window['remappedKeys'].update(disabled= not validRemapCombo[1])
                
        # if parameters are given, the job is done. now comes the actual part.
        elif (process["givenParams"]):
            givenHotkey,givenAction,givenParams = process['givenHotkey'],process['givenAction'], process['givenParams']
            if (givenAction == "writes"):
                addHotkey(givenHotkey,givenAction,givenParams)
            elif (givenAction == "opens"):
                addHotkey(givenHotkey,givenAction,givenParams)
            elif (givenAction == "plays"):
                addHotkey(givenHotkey,givenAction,givenParams)
            elif (givenAction == "remaps"):
                addHotkey(givenParams[0],givenAction,givenParams[1])            

            data = loadData()
            currHotkeyData = data['hotkeys']
            currAddProcessData = []

            if not givenAction == "remaps": # for remapping, we take the user's input instead of the provided hotkey, incase they decide to change it.
                currAddProcessData = [process['givenHotkey'],givenAction,givenParams]
            else:
                currAddProcessData = [givenParams[0],givenAction,givenParams[1]]

            currHotkeyData.append(currAddProcessData)
            updateData('hotkeys',currHotkeyData)
            window.close()
            print('[LOG] Completed the HotKey adding process.')
                 

def make_window(theme):
    sg.theme(theme)
    menu_def = [['&Docs', ['&Open Docs','&Adding Hotkey','&Removing Hotkey']],
                ['&About', ['&Credits','&Tools Used']] ]
    right_click_menu_def = [[], ['Edit Me','Exit']]
    defaultFont = loadData()['defaultFont']

    my_hotkeys_layout =  [

                # [sg.Menu(menu_def, key='-MENU-')],
                [sg.Text('Your Hotkeys',font=(defaultFont,40))],
                [sg.Multiline(get_hotkeys(),size=(9,9), font=(defaultFont,11), expand_x=True, expand_y=True, write_only=True,disabled=True,key='hotkeylist')],
                [sg.Button("Reload Hotkeys",key='reload_hotkeys')],
                [sg.Text('\nWelcome to EmberKey!',font=(defaultFont,20))],
                [sg.Text('Add your own hotkeys to play sound, execute a file, type something or just remap a key!')]
                ]

    hotkey_editor_layout = [
               [sg.Text('Hotkeys',font=(defaultFont,30),justification='c')],
               [sg.Button(image_filename='./assets/addHotKeyAnim.gif',image_subsample=2,key="attemptAddHotkey"),sg.Button(image_filename='./assets/removeHotKeyAnim.gif',image_subsample=2,key="attemptRemoveHotkey")],
               ]
    
    settings_layout = [
                    [sg.Text("Choose the GUI's accent")],
                    [sg.Radio('Dark', "theme", default=True, size=(10,1), k='dark'), sg.Radio('Light', "theme", default=False, size=(10,1), k='light')],
                    [sg.Button("Update Theme")],
                    [sg.T('')], # This is an empty element, to leave a space between options.
                    [sg.Checkbox('Warn me through TTS when the audio file I chose no longer exists in the directory',default=loadData()['warnNoSound'],key='warnNoSoundCheckBox')],
                    [sg.Button("Update Warning")],
                    [sg.T('')],
                    [sg.Text("Hotkey Options")],
                    [sg.Button('Reload All Hotkeys',key="reloadHotkeys"),sg.Button('Erase All Hotkeys',key='eraseHotkeys')],
                    [sg.T('')],
                    [sg.Text("Use GIFs Options")],
                    [sg.Checkbox('Use GIFs instead of pop-ups where possible',default=loadData()['useGIF'],key='use_gifs_checkbox')],
                    [sg.Button('Update GIF settings',key="use_gifs_button")],
                    [sg.Button('Check compatibility',key='check_gif_compatibility_button')],
                    [sg.T('')],
                    [sg.Button('Show Console',key="showConsole")]
                    ]
    
    layout = [ [sg.MenubarCustom(menu_def, key='-MENU-', font = defaultFont, tearoff=True, background_color='#18222d', text_color='white' )]]
                
    menuOptions = [
            sg.Tab('My Hotkeys', my_hotkeys_layout),
            sg.Tab('Hotkey Editor', hotkey_editor_layout),
            sg.Tab('Settings', settings_layout),
            ]
    
    layout +=[[sg.TabGroup([menuOptions], key='-TAB GROUP-', expand_x=True, expand_y=True)]]
    layout[-1].append(sg.Sizegrip())
    window = sg.Window('EmberKey', createReusableLayout(layout), right_click_menu=right_click_menu_def, right_click_menu_tearoff=True, grab_anywhere=True, resizable=True, margins=(0,0), finalize=True, icon = hotkeyIcon)
    window.set_min_size(window.size)
    return window

def main():
    window = make_window(sg.theme())
    openAndCloseWindow(window)
    
    # This is an Event Loop 
    while True:
            
        event, values = window.read(timeout=100)

        if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
            print('============ Event = ', event, ' ==============')
                
        if event in (None, 'Exit'):
            print("[LOG] Clicked Exit!")
            break
            
        elif event == 'Open Docs':
            webbrowser.open(linkToDocs + "#emberkey")
        elif event == 'Adding Hotkey':
            webbrowser.open(linkToDocs + "#adding-hotkeys")
        elif event == 'Removing Hotkey':
            webbrowser.open(linkToDocs + "#removing-hotkeys")

        elif event == 'Credits':
            print("[LOG] User viewed credits.")
            sg.popup('EmberKey',
                     'This app was built for a Computer Science project.',
                     'Class 11 A',
                     'Members of the team are:',
                     '|  Dhruv',
                     '|  Johan',
                     '|  Bhumika', keep_on_top=True)

        elif event == 'Tools Used':
            print('[LOG] User viewed tools used.')
            sg.popup('This app was built in 4 days using the following modules',
                     '|  PySimpleGUI [Main]',
                     '|  keyboard [Hotkeys]',
                     '|  pillow [GIFs]',
                     '|  json [Config Storage]',
                     '|  os [Execution]',
                     '|  playsound@1.2.2 [Playing audio]',
                     '|  copy',
                     '|  ntpath',
                     '|  webbrowser [Opening docs]', keep_on_top=True)

        elif event == "attemptAddHotkey":
            print("[LOG] User is trying to add a hotkey")
            addHotKeyWindow()

        elif event == 'attemptRemoveHotkey':
            print("[LOG] User is trying to remove a hotkey")
            removeHotKeyWindow()

        elif event == "reload_hotkeys":
            window['hotkeylist'].update(get_hotkeys())
        
        elif event == "reloadHotkeys": #not to be confused with event reload_hotkeys, this is used to restart all the current hotkeys
            print('[LOG] User reloaded all hotkeys')
            removeAllHotkeys()
            loadAllHotkeys()
            addedHotkeyMessage("All hotkeys were reloaded!")

        elif event == 'eraseHotkeys':
            print('[LOG] User is trying to erase all hotkeys')
            confirmation = sg.popup_yes_no("Are you sure?")
            if confirmation == 'Yes':
                removeAllHotkeys(force=True)
                sg.popup_auto_close("Removed all hotkeys.")
                print('[LOG] User erased all hotkeys')
            else:
                print('[LOG] User cancelled process')

        elif event == "showConsole":
            print('[LOG] Displaying Debug Window')
            debugWindow()
            window.close()
            window = make_window(loadData()['theme'])

        elif event == "Update Warning":
            choice = values['warnNoSoundCheckBox']
            print('[LOG] User updated sound warnings to',choice)
            updateData('warnNoSound',choice)

        elif event == "use_gifs_button":
            choice = values['use_gifs_checkbox']
            if (choice):
                wantsToCheckComp = sg.popup_yes_no("It is recommended that you check if your python version supports the GIF module before enabling this option.\nDo you want to run a compatibility test?")
                if wantsToCheckComp == "Yes":
                    canUseGifs = checkCanUseGIF()
                    if canUseGifs == "Success":
                        updateData('useGIF',True)
                        print('[LOG] User activated GIF settings after checking compatibility')
                else:
                    updateData('useGIF',True)
                    print('[LOG] User activated GIF settings without checking compatibility')
            else:
                updateData('useGIF',False)
                print('[LOG] User deactivated GIF feature.')

        elif event == 'check_gif_compatibility_button':
            print("[LOG] User checked GIF compatibility")
            checkCanUseGIF()

        elif event == "Update Theme":
            themeMode = {
                'user': "light" if values['light'] else "dark",
                'processor': "reddit" if values['light'] else 'DarkGrey8' 
            }
            print("Changed theme to",themeMode['user'])
            with open("config.json", "r") as jsonFile:
                data = json.load(jsonFile)
            with open("config.json", "w") as jsonFile:
                data['theme'] = themeMode['processor']
                json.dump(data, jsonFile)
            print("Updated config file's theme to",themeMode['user'])
            window.close()
            window = make_window(themeMode['processor'])
            if (loadData()["useGIF"]):
                loadSentences = {
                    3: "Success ＼(^o^)／",
                    6: "Theme updated!",
                    9: "Python ftw :100:"
                    }
                successWindow(loadSentences)
            else:
                sg.Popup("Theme updated successfully!")

        elif event == 'Edit Me':
            sg.execute_editor(__file__)

        elif event == 'Versions':
            sg.popup(sg.get_versions(), keep_on_top=True)

    window.close()
    keyboard.unhook_all_hotkeys
    exit(0)

if __name__ == '__main__':
    sg.theme(loadData()['theme'])
    main()

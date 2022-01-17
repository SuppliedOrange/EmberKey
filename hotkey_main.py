#!/usr/bin/env python 3.7.9

import PySimpleGUI as sg
import json
import keyboard
from externalStuff import legalhotkeys, loadedHotkeys, openAndCloseWindow, loadData, updateData, isValidHotkey, createReusableLayout, get_hotkeys, check_valid_hotkey,addHotkey, loadAllHotkeys, removeAllHotkeys, get_hotkeys_removal, removeHotkey
import webbrowser

'''
with open("config.json", "r") as jsonFile:
    data = json.load(jsonFile)
with open("config.json", "w") as jsonFile:
    data['hotkeys'] = []
    json.dump(data, jsonFile)
print("Flushed all hotkeys")
'''
loadAllHotkeys()
linkToDocs = 'https://github.com/SuppliedOrange/PythonHotkeyAppThing'


def debugWindow():
    logging_layout = [
        [sg.Text("Everything we log will appear here")],
        #[sg.Multiline(size=(60,15), font='Courier 8', expand_x=True, expand_y=True, write_only=True,
        #reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True, auto_refresh=True,key='debuggerConsole')],
        [sg.Output(size=(60,15), font='Courier 8', expand_x=True, expand_y=True,key="debuggerConsole")]
    ]
    window = sg.Window("Debugger",createReusableLayout(logging_layout), element_justification='c',keep_on_top=True)
    window.finalize()

'''
from PIL import Image, ImageTk, ImageSequence
def successWindow():

    loadingWindowLayout =  [
    [sg.Image(key = 'mumei')],
    [sg.Text("Done!",font = ('Bahnschrift',40), justification='c',key='loadingText',auto_size_text=True)]
    ]
    window = sg.Window("Success Message", loadingWindowLayout ,element_justification='c', margins=(0,0),element_padding=(0,0),finalize=True, auto_size_text=True,keep_on_top=True,modal=True)
    window.make_modal()

    window['loadingText'].expand(True,True,True)

    #gif = ['yay','walk','fingerspin']
    #gif = random.choice(gif)  #Let's not use these.. I need to show this app to my parents too.
    gif = 'yay'

    interframe_duration = Image.open(f'./assets/{gif}.gif').info['duration']

    loadSentences = {
    3: "Success ＼(^o^)／",
    6: "Theme updated!",
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
            window['mumei'].update(data=ImageTk.PhotoImage(frame))

        textUpdate = 'Success ＼(^o^)／'

        for i in loadSentences.keys():
            if i <= loadCounter:
                textUpdate = loadSentences[i]

        window['loadingText'].update(textUpdate)
        loadCounter = 0 if loadCounter > 10 else loadCounter

        if (toBreak):
            break

        # I have retired this function. I have decided to abandon GIFs in order to focus on compatibility
'''

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
        window = sg.Window("Removing Hotkeys", [[sg.Column(reusableWindowLayout,scrollable=True)]] , margins=(0,0),element_padding=(0,0),finalize=True, auto_size_text=True,keep_on_top=False,modal=True, resizable = True)
        window.make_modal()
        return window
    
    window = genWindow(genHotkeyRemovalLayout())

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
         "givenParams" : None,
         "hotKeySecret" : None
     }

    allKeys = ''
    for i in legalhotkeys:
        allKeys += "\n" + i
    allKeysLayout = [
        [sg.Multiline(allKeys,size=(20,20), font=(defaultFont,16), expand_x=True, expand_y=True, write_only=True)]
    ]
    addHotKeyWindowLayout = [
        [sg.Text('Enter a Hotkey',font=(defaultFont,40))],
        [sg.Input(key='hotkeyInput')],
        [sg.Text('Invalid Key',font=(defaultFont,18),key='validator',text_color='')],
        [sg.Text('Examples:',font=(defaultFont,20))],
        [sg.Text('"shift+ctrl+a" -> Press shift, control and A \n"alt+1" -> Press alt and 1\n"enter" -> Press Enter key',font=(defaultFont,11))],
        [sg.Button("Show keys",key="showAllKeys"),sg.Button("Next",key="complete1")]
        
     ]
    selectHotKeyTypeWindowLayout = [
        [sg.Text('I want the Hotkey to...',font=(defaultFont,40))],
        [sg.Radio('Open a file', "hotKeyType", default=True, size=(15,1), k='openFile'), sg.Radio('Type something', "hotKeyType", default=False, size=(10,1), k='keyboardWrite')],
        [sg.Radio('Remap a key', "hotKeyType", default=False, size=(15,1), k='keyboardRemap'), sg.Radio('Play a sound', "hotKeyType", default=False, size=(10,1), k='playSound')],
        [sg.Button("Next",key="complete2")],
        [sg.Text("Current hotkey: Unknown",key='currHotkeyMessage')]
    ]

    firstKey = loadData()['addProcessData'][0] if len(loadData()['addProcessData']) else "f6"

    parameterLayouts = {
        "opens" : [
            [sg.Text("What file would you like to open?",font=(defaultFont,40))],
            [sg.Button("Choose File",key='chooseFile')],
            [sg.Button("Finish",disabled=True,key='Finish')]
        ],
        "writes" : [
            [sg.Text("What do we write?",font=(defaultFont,40))],
            [sg.Text("By \"writing\", we pass on the letters to your keyboard in quick succession in order. \nSo 'Hello there' would press H,e,l,l,o,space,t.. etc",font=("Bahnschrift",10))],
            [sg.Input("I love typescript!",font=("Bahnschrift",20),key='writesInput')],
            [sg.Button("Done",key="writtenMessage")]
        ],
        "remaps" : [
            [sg.Text("What key are we remapping?",font=(defaultFont,40))],
            [sg.Input(firstKey,key="keyboardRemapKey1"),sg.Text(" should press "),sg.Input("g",key="keyboardRemapKey2")],
            [sg.Text("Remapping key 'f6' to 'g'",font=(defaultFont,11),key="keyboardRemapValidator")],
            [sg.Text("\nExamples:\n'f1' to 'backspace'\n'shift+up' to 'windows+shift+s' (screenshot)\n'alt+a' to 'ă' (unconventional letter)\n")],
            [sg.Button("Show all keys",key='showAllKeys'),sg.Button("Finish",key="remappedKeys")]
        ],
        "plays" : [
            [sg.Text("What audio would you like to play?",font=(defaultFont,40))],
            [sg.Text("Unfortunately, only .mp3 files are supported.",font=(defaultFont,15))],
            [sg.Button("Choose File",key='chooseAudioFile')],
            [sg.Button("Finish",disabled=True,key='Finish')]
        ],

    }
    

    def addProcessWindow(windowName,windowLayout):
        reusableWindowLayout = createReusableLayout(windowLayout)
        window = sg.Window(windowName, reusableWindowLayout , margins=(0,0),element_padding=(0,0),finalize=True, auto_size_text=True,keep_on_top=False,modal=True)
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

        elif (event == "complete2"):
            chosenValue = None
            if (values["openFile"]):
                chosenValue = "opens"
            elif (values["keyboardWrite"]):
                chosenValue = "writes"
            elif (values["keyboardRemap"]):
                chosenValue = "remaps"
            elif (values["playSound"]):
                chosenValue = "plays"
            else:
                chosenValue = "???"
            
            process["givenAction"] = chosenValue
            currdata = loadData()['addProcessData']
            currdata.append(process["givenAction"])
            updateData("addProcessData",currdata)

        elif (event == "chooseFile"):
            print("[LOG] Trying to choose a file for new hotkey")
            def askPopUp():
                filePath = sg.popup_get_file('Choose your file', keep_on_top=True)
                if not filePath:
                    print("[LOG] User did not choose a file.")
                    pass
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
                        window['Finish'].update(disabled= False)
                        return
            askPopUp()
            
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
                        window['Finish'].update(disabled= False)
                        return
            askPopUp()
        
        elif (event == "writtenMessage"):
            writtenMessage = values['writesInput']
            process["givenParams"] = writtenMessage
            currdata = loadData()["addProcessData"]
            currdata.append(process["givenParams"])            
            updateData("addProcessData",currdata)
            sg.popup_auto_close("Hotkey added!\nClick on finish to quit to main app.",auto_close_duration=5)

        elif (event == 'remappedKeys'):
            keys = [values['keyboardRemapKey1'],values['keyboardRemapKey2']]
            process["givenParams"] = keys
            currdata = loadData()['addProcessData']
            currdata.append(process["givenParams"])
            updateData("addProcessData",currdata)
            sg.popup_auto_close(f"Hotkey Added!\nYour {keys[0]} key will now behave as {keys[1]}")


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
            window = addProcessWindow("Selecting hotkey type",selectHotKeyTypeWindowLayout)
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
                return [f'Remapping key(s) "{key1}" to key(s) "{key2}"',True]
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
                [sg.Text('\nWelcome to [Name of App]!',font=(defaultFont,20))],
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
                    [sg.Button('Show Console',key="showConsole")]
                    ]
    
    layout = [ [sg.MenubarCustom(menu_def, key='-MENU-', font = defaultFont, tearoff=True, background_color='#18222d', text_color='white' )]]
                #[sg.Text('Demo Of (Almost) All Elements', size=(38, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)]]
                
    menuOptions = [
            sg.Tab('My hotkeys', my_hotkeys_layout),
            sg.Tab('Hotkey Editor', hotkey_editor_layout),
            sg.Tab('Settings', settings_layout),
            ]
    
    layout +=[[sg.TabGroup([menuOptions], key='-TAB GROUP-', expand_x=True, expand_y=True)]]
    layout[-1].append(sg.Sizegrip())
    window = sg.Window('Python Hotkey App', createReusableLayout(layout), right_click_menu=right_click_menu_def, right_click_menu_tearoff=True, grab_anywhere=True, resizable=True, margins=(0,0), finalize=True,
                       #scaling=2.0,
                       )
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
            webbrowser.open(linkToDocs + "#application-name")
        elif event == 'Adding Hotkey':
            webbrowser.open(linkToDocs + "#adding-hotkeys")
        elif event == 'Removing Hotkey':
            webbrowser.open(linkToDocs + "#removing-hotkeys")

        elif event == 'Credits':
            print("[LOG] User viewed credits.")
            sg.popup('[App Name]',
                     'This app was built for a Computer Science project.',
                     'Class 11 A',
                     'Members of the team are:',
                     '|  Dhruv',
                     '|  Johan',
                     '|  Bhumika', keep_on_top=True)

        elif event == 'Tools Used':
            print('[LOG] User viewed tools used.')
            sg.popup('This app was built in 3 days using the following modules',
                     '|  PySimpleGUI [Main]',
                     '|  keyboard [Hotkeys]',
                 #   '|  PIL [GIFs]',   No more.
                     '|  json [Config Storage]',
                     '|  subprocess [Execution]',
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
            sg.popup_auto_close("All hotkeys were reloaded!")

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
            #successWindow()
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

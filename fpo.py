import json
import os
import subprocess as sp

import PySimpleGUI as sg

sg.theme('DarkAmber')
configPath = '.\config'
configFile = '.\config\config.json'
locationsFile = '.\config\locations.json'


def programsFound(locationsFile):
    with open(locationsFile, 'r', encoding='utf-8') as cf:
        programsFound = json.load(cf)
    return programsFound


def findProgramPath(filename, locationsFile):
    for p in programsFound(locationsFile)['programs']:
        if filename == p['name']:
            filepath = p['path']
    return filepath


def addProgram(window):

    menubar, askfilepath, askfilename = languageChooser()

    filepath = sg.popup_get_file(askfilepath, no_window=True)
    filename = sg.popup_get_text(title='FPO', message=askfilename)

    print(filename)

    if filepath == '':
        return

    if filename == '' or filename is None:
        filename = os.path.basename(filepath).capitalize().replace('.exe', '')

    entry = {
        'name': filename,
        'path': filepath,
    }

    if filepath not in programsFound(locationsFile):

        with open(locationsFile, 'r+', encoding='utf-8') as cf:
            data = json.load(cf)
            data['programs'].append(entry)
            cf.seek(0)
            json.dump(data, cf, indent=4, ensure_ascii=False)
            arrayNewFilenames = []
            for p in data['programs']:
                newFilename = p['name']
                arrayNewFilenames.append(newFilename)

            window['-LBPROGRAM-'].update(values=arrayNewFilenames)


def buttonOpen(values):
    if not values['-LBPROGRAM-']:
        sg.popup_error('Por favor, selecione um item!')
    else:
        nomePrograma = values['-LBPROGRAM-'][0]
        caminhoPrograma = findProgramPath(nomePrograma, locationsFile)
        if caminhoPrograma.endswith('.exe'):
            sp.Popen(
                [caminhoPrograma],
                creationflags=sp.DETACHED_PROCESS | sp.CREATE_NEW_PROCESS_GROUP,
            )
        else:
            os.startfile(caminhoPrograma)


def configIni():

    arrayFileName = []

    if not os.path.exists(locationsFile):
        pattern = {"programs": []}
        if not os.path.exists(configPath):
            os.mkdir(configPath)
        with open(locationsFile, 'w', encoding='utf-8') as cf:
            json.dump(pattern, cf)

    for p in programsFound(locationsFile)['programs']:
        filename = p['name']
        arrayFileName.append(filename)

    return arrayFileName


def languageChooser(flag=0):

    language = ['ptBR', 'enUS']

    if not os.path.exists(configFile):
        pattern = {"language": language[flag]}
        if not os.path.exists(configPath):
            os.mkdir(configPath)
        with open(configFile, 'w', encoding='utf-8') as cf:
            json.dump(pattern, cf)

    askFilepath_ptBR = 'Adicionar programa'
    askFilepath_enUS = 'Add program'

    askFilename_ptBR = 'Insira nome personalizado do arquivo:'
    askFilename_enUS = 'Insert a customized filename:'

    menubar_ptBR = [
        ['&Arquivo', ['&Adicionar programa']],
        ['&Editar', ['&Editar configuração']],
    ]

    menubar_enUS = [
        ['&Arquivo', ['&Add program']],
        ['&Editar', ['&Editar configuração']],
    ]

    with open(configFile, 'r', encoding='utf-8') as cf:
        langs = json.load(cf)

    if langs['language'] == 'ptBR':
        menubar = menubar_ptBR
        askFilename = askFilename_ptBR
        askFilepath = askFilepath_ptBR
    else:
        menubar = menubar_enUS
        askFilename = askFilename_enUS
        askFilepath = askFilepath_enUS

    return menubar, askFilepath, askFilename


def mainWindow():

    arrayFileName = configIni()
    menubar, askFilepath, askFilename = languageChooser()

    layout = [
        [sg.Menu(menubar, tearoff=False, pad=(200, 1))],
        [sg.T('Fast Program Opener')],
        [sg.LB(arrayFileName, enable_events=True, key='-LBPROGRAM-', size=(25, 10))],
        [sg.RButton('Abrir', key='-BOPEN-', size=(19, 1))],
    ]

    window = sg.Window('FPO', layout, finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        # TODO adicionar função para editar arquivo de locations (locationsFile)
        if event == 'Adicionar programa' or event == 'Add program':
            addProgram(window)
        if event == '-BOPEN-':
            buttonOpen(values)

    window.close()


mainWindow()

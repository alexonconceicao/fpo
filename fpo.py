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

    items = languageChooser()

    filepath = sg.popup_get_file(items[1], no_window=True)
    filename = sg.popup_get_text(title='FPO', message=items[2])

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


def languageChooser():

    language = ['ptBR', 'enUS']

    if not os.path.exists(configFile):
        pattern = {"language": language[0]}
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
        [
            '&Editar',
            [
                '&Editar configura????o',
                '&Idioma',
                [
                    'Portugu??s',
                    'Ingl??s',
                ],
            ],
        ],
    ]

    menubar_enUS = [
        ['&File', ['&Add program']],
        [
            '&Edit',
            [
                '&Edit config',
                '&Language',
                [
                    'Portuguese',
                    'English',
                ],
            ],
        ],
    ]

    with open(configFile, 'r', encoding='utf-8') as cf:
        langs = json.load(cf)

    if langs['language'] == 'ptBR':
        menubar = menubar_ptBR
        askFilename = askFilename_ptBR
        askFilepath = askFilepath_ptBR
        abrir = 'Abrir'
    else:
        menubar = menubar_enUS
        askFilename = askFilename_enUS
        askFilepath = askFilepath_enUS
        abrir = 'Open'

    items = [menubar, askFilepath, askFilename, abrir]

    return items


def mainWindow():

    arrayFileName = configIni()
    items = languageChooser()

    layout = [
        [sg.Menu(items[0], tearoff=False, pad=(200, 1))],
        [sg.T('Fast Program Opener')],
        [sg.LB(arrayFileName, enable_events=True, key='-LBPROGRAM-', size=(25, 10))],
        [sg.RButton(items[3], key='-BOPEN-', size=(19, 1))],
    ]

    window = sg.Window('FPO', layout, finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        # TODO adicionar fun????o para editar arquivo de locations (locationsFile)
        if event == 'Adicionar programa' or event == 'Add program':
            addProgram(window)
        if event == '-BOPEN-':
            buttonOpen(values)
        if event == 'Portugu??s' or event == 'Portuguese':
            with open(configFile, 'r') as f:
                data = json.load(f)
            if data['language'] != 'ptBR':
                data['language'] = 'ptBR'
                with open(configFile, 'w') as f:
                    json.dump(data, f)
        if event == 'Ingl??s' or event == 'English':
            with open(configFile, 'r') as f:
                data = json.load(f)
            if data['language'] != 'enUS':
                data['language'] = 'enUS'
                with open(configFile, 'w') as f:
                    json.dump(data, f)

    window.close()


mainWindow()

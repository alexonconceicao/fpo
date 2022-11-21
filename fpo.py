import os
import subprocess as sp

import PySimpleGUI as sg

sg.theme('DarkAmber')


def programasEncontrados(configFile):
    with open(configFile, 'r+') as cf:
        programasEncontrados = cf.readlines()[2:]
    return programasEncontrados


def mainWindow():

    configPath = '.\config'
    configFile = '.\config\config.txt'
    vetorNomeArquivo = []

    if not os.path.exists(configFile):
        if not os.path.exists(configPath):
            os.mkdir(configPath)
        with open(configFile, 'w+', encoding='utf-8') as cf:
            cf.write('Lista de programas:\n')

    for p in programasEncontrados(configFile):
        nomeArquivo = (
            os.path.basename(p).replace('.exe', '').capitalize().replace('\n', '')
        )
        vetorNomeArquivo.append(nomeArquivo)

    menubar = [
        ['&Arquivo', ['&Adicionar programa', '&Salvar']],
        ['&Editar', ['&Editar configuração']],
    ]

    layout = [
        [sg.Menu(menubar, tearoff=False, pad=(200, 1))],
        [sg.T('Fast Program Opener')],
        [sg.LB(vetorNomeArquivo, enable_events=True, key='-LBPROGRAM-', size=(50, 6))],
        [sg.RButton('Abrir', key='-BOPEN-', size=(40, 1))],
    ]

    window = sg.Window('FPO', layout, finalize=True, modal=False)
    lbProgramWindow = window['-LBPROGRAM-']
    itemSelecionado = ''
    programa = ''

    while True:
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED:
            break
        if event == 'Adicionar programa':
            filename = sg.popup_get_file('Adicionar programa', no_window=True)

            if filename not in programasEncontrados(configFile):
                with open(configFile, 'a+', encoding='utf-8') as cf:
                    cf.writelines(['\n' + filename])

            with open(configFile, 'r+') as cf:
                programasAtualizados = cf.readlines()[2:]

            vetorNomeArquivoAtualizados = []
            for p in programasAtualizados:
                nomeArquivo = (
                    os.path.basename(p)
                    .replace('.exe', '')
                    .capitalize()
                    .replace('\n', '')
                )
                vetorNomeArquivoAtualizados.append(nomeArquivo)

            window['-LBPROGRAM-'].update(values=vetorNomeArquivoAtualizados)

        if event == '-LBPROGRAM-':
            programaSelecionado = values[event]
            if programaSelecionado:
                itemSelecionado = programaSelecionado[0]
                index = lbProgramWindow.get_indexes()[0]

        if event == '-BOPEN-':
            if itemSelecionado != '':
                for p in programasEncontrados(configFile):
                    programa = p.replace('\n', '')
                    if itemSelecionado.lower() in programa.lower():
                        print(programa)
                        sp.Popen(
                            [programa],
                            creationflags=sp.DETACHED_PROCESS
                            | sp.CREATE_NEW_PROCESS_GROUP,
                        )

            else:
                sg.popup_error('Por favor, selecione um item!')

    window.close()


mainWindow()

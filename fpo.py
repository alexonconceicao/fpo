import os
import subprocess as sp

import PySimpleGUI as sg
import json

sg.theme('DarkAmber')
configPath = '.\config'
configFile = '.\config\locations.json'


def programasEncontrados(configFile):
    with open(configFile, 'r') as cf:
        programasEncontrados = json.load(cf)
    return programasEncontrados


def buscarCaminhoPrograma(nome, configFile):
    for p in programasEncontrados(configFile)['programas']:
        if nome == p['nome']:
            caminho = p['caminho']
    return caminho


def mainWindow():

    vetorNomeArquivo = []

    if not os.path.exists(configFile):
        dict = {"programas": []}
        if not os.path.exists(configPath):
            os.mkdir(configPath)
        with open(configFile, 'w', encoding='utf-8') as cf:
            json.dump(dict, cf)

    for p in programasEncontrados(configFile)['programas']:
        nomeArquivo = p['nome']
        vetorNomeArquivo.append(nomeArquivo)

    menubar = [
        ['&Arquivo', ['&Adicionar programa']],
        ['&Editar', ['&Editar configuração']],
    ]

    layout = [
        [sg.Menu(menubar, tearoff=False, pad=(200, 1))],
        [sg.T('Fast Program Opener')],
        [sg.LB(vetorNomeArquivo, enable_events=True, key='-LBPROGRAM-', size=(25, 10))],
        [sg.RButton('Abrir', key='-BOPEN-', size=(19, 1))],
    ]

    window = sg.Window('FPO', layout, finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        # TODO adicionar função para editar arquivo de locations (configFile)
        if event == 'Adicionar programa':
            # TODO adicionar verificador caso usuário não digite nome personalizado
            caminhoDoArquivo = sg.popup_get_file('Adicionar programa', no_window=True)
            nomeDoArquivo = sg.popup_get_text('Insira nome personalizado do arquivo:')
            entry = {
                'nome': nomeDoArquivo,
                'caminho': caminhoDoArquivo,
            }

            if caminhoDoArquivo not in programasEncontrados(configFile):

                with open(configFile, 'r+') as cf:
                    dados = json.load(cf)
                    dados['programas'].append(entry)
                    cf.seek(0)
                    json.dump(dados, cf, indent=4)
                    vetorNomeArquivosAtualizados = []
                    for p in dados['programas']:
                        nomeArquivo = p['nome']
                        vetorNomeArquivosAtualizados.append(nomeArquivo)

                    window['-LBPROGRAM-'].update(values=vetorNomeArquivosAtualizados)

        if event == '-BOPEN-':
            if not values['-LBPROGRAM-']:
                sg.popup_error('Por favor, selecione um item!')
            else:
                nomePrograma = values['-LBPROGRAM-'][0]
                caminhoPrograma = buscarCaminhoPrograma(nomePrograma, configFile)
                sp.Popen(
                    [caminhoPrograma],
                    creationflags=sp.DETACHED_PROCESS | sp.CREATE_NEW_PROCESS_GROUP,
                )

    window.close()


mainWindow()

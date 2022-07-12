import PySimpleGUI as sg
import os

import pygame.event
from pygame import mixer

class BackEnd:

    def __init__(self, directorio):
        self.cont = 0
        self.cont_click = 0
        self.diretorio = self.buscar_musicas(directorio)

    def nome_musica(self, diretorio):
        nome = self.buscar_musicas(diretorio)
        lista = []
        for n in nome:
            lista.append(n[40:])

        return lista

    def buscar_musicas(self, diretorio):
        dic = []
        for (root, dirs, files) in os.walk(diretorio):
            for file in files:
                if '.mp3' in file:
                    dic.append(root + '/' + file)
        return dic

    def tocar_musica(self):
        pygame.init()
        mixer.music.load(self.diretorio[self.cont])
        mixer.music.play()

    def pausar_musica_button(self):
        if self.cont_click == 0:
            mixer.music.pause()
            self.cont_click += 1

        else:
            self.despausar()
            self.cont_click -= 1

    def despausar(self):
        mixer.music.unpause()

    def proxima_musica(self):
        if (len(self.diretorio) - 1) == self.cont:
            mixer.music.stop()
            self.cont = 0
            self.tocar_musica()

        else:
            mixer.music.stop()
            self.cont += 1
            self.tocar_musica()

    def musica_tocando(self):
        mixer.init()
        if mixer.music.get_busy():
            return True

        else:
            return False

    def voltar_musica(self):
        if self.cont == 0:
            mixer.music.stop()
            self.cont = len(self.diretorio) - 1
            self.tocar_musica()

        else:
            mixer.music.stop()
            self.cont -= 1
            self.tocar_musica()


class FrontEnd:
    def __init__(self, diretorio):
        self.back = 'img/back.png'
        self.img = 'img/img.png'
        self.play = 'img/play_button.png'
        self.pause = 'img/pause.png'
        self.next = 'img/next.png'
        self.diretorio = diretorio

    def tela(self):
        sg.theme_background_color('black')
        layout = [
            [sg.Canvas(size=(300, 10), pad=(0, 0), background_color='black')],
            [sg.Canvas(size=(27, 330), pad=(0, 0), background_color='black'),  sg.Image(self.img, size=(230, 300), pad=(0, 0))],
            [sg.Text(background_color='black', pad=(0, 0), key='nome', size=(40, 1))],
            [sg.Canvas(size=(500, 0), pad=(0, 0), background_color='white')],
            [sg.Canvas(size=(10, 10), background_color='black')],
            [sg.Button(image_filename=self.back, pad=(5, 0), border_width=0, mouseover_colors='black', enable_events=True,
                       key='voltar_musica'), sg.Canvas(size=(10, 10), background_color='black'), sg.Button(image_filename=self.play,
                       pad=(0, 0), border_width=0, mouseover_colors='black', enable_events=True, key='play'), sg.Canvas(size=(10, 10),
                       background_color='black'), sg.Button(image_filename=self.pause, pad=(5, 0), border_width=0, mouseover_colors='black',
                       enable_events=True, key='pause'), sg.Canvas(size=(10, 10), background_color='black'), sg.Button(image_filename=self.next,
                       pad=(5, 0), border_width=0, mouseover_colors='black', enable_events=True, key='proxima_musica')]
        ]
        tela = sg.Window(title='Player', layout=layout, finalize=True, size=(300, 500))
        return tela

    def run(self, back):
        tela = self.tela()
        while True:
            ev, val = tela.read()


            if ev == sg.WIN_CLOSED:
                tela.close()
                break


            if ev == 'play':
                back.tocar_musica()
                tela.find_element('nome').update(back.nome_musica(self.diretorio)[back.cont])


            elif ev == 'pause':
                back.pausar_musica_button()

            elif ev == 'voltar_musica':
                back.voltar_musica()
                tela.find_element('nome').update(back.nome_musica(self.diretorio)[back.cont])

            elif ev == 'proxima_musica':
                back.proxima_musica()
                tela.find_element('nome').update(back.nome_musica(self.diretorio)[back.cont])



if __name__ == '__main__':
    diretorio = sg.popup_get_folder('Selecione a pasta que está as músicas', background_color='black')

    tela = FrontEnd(diretorio)
    backend = BackEnd(diretorio)
    tela.run(backend)
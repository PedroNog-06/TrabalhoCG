"""
Arquivos do trabalho:
    - Main -> Roda o programa
    - Model  -> Figura e as transformações
    - View   -> Desenha tudo na tela
    - Controller -> Lê o teclado e atualiza o Model
"""

import pygame
from Model.figura import FiguraModel
from Model.config import LARGURA, ALTURA
from View.view_figura import View
from Controller.controller_figura import Controller


def main():
    pygame.init()

    # Cria a janela
    screen = pygame.display.set_mode((LARGURA, ALTURA))  # Variáveis em MAIÚSCULAS são 'constantes' em Python.
    pygame.display.set_caption("Trabalho de Computação Gráfica")

    clock = pygame.time.Clock()

    # Instancia as três camadas do MVC
    model = FiguraModel()
    view = View(screen)
    controller = Controller(model)

    # ----- Loop principal ------
    # A cada frame ele segue os passos abaixo
    # 1. Processar o que aconteceu (eventos e teclas)
    # 2. Desenhar o estado atual na tela
    # 3. Esperar o tempo necessário para manter 60 frames por segundo

    while controller.rodando:
        eventos = pygame.event.get()

        controller.processar_eventos(eventos)      # Trata TAB, R, setas e etc
        controller.processar_teclas_continuas()    # Trata WASD, QE, ZX e etc

        view.renderizar(model)    # Desenha tudo na tela

        clock.tick(60)          # Limita a 60 FPS

    pygame.quit()   # Fecha a janela e encerra o programa


if __name__ == "__main__":  #Só roda o main se este arquivo for o programa principal, e não importado por outro.
    main()

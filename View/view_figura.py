#Aqui fica tudo que aparece na tela: o fundo, os eixos, a figura desenhada e a hud no canto superior esquerdo.

import math
import pygame

from Model.config import CX, CY, LARGURA, ALTURA   #Centro de X, Centro de Y, Largura e Altura da tela


# Cores que serão usadas
PRETO   = (  0,   0,   0)
BRANCO  = (255, 255, 255)
CINZA   = (180, 180, 180)
AMARELO = (255, 255,   0)
VERMELHO = (200,   0,   0)
VERDE   = (  0, 200,   0)


class View:
    """
    Responsável por tudo que é visível na janela do pygame.

    Recebe a tela (screen) do pygame e um objeto FiguraModel, e sabe como
    transformar esses dados em pixels na tela.
    """

    def __init__(self, screen):
        self.screen = screen
        self.fonte  = pygame.font.SysFont("monospace", 20)  #Definindo a fonte da hud do programa

    def renderizar(self, model):
        """
        Redesenha a tela inteira com base no estado atual do model.

        Chamado uma vez por frame, no final do loop principal.
        Importante: A ordem da chamada importa.
        """
        self.screen.fill(PRETO) #Primeiro o fundo
        self._desenhar_eixos() #Depois os eixos de referência
        self._desenhar_figura(model.vertices_transformados) #Depois a figura com os vértices já transformados
        self._desenhar_hud(model)   #E por fim, a hud
        pygame.display.flip()   #Atualiza a tela com tudo que foi desenhado


    # Métodos da classe para desenhar na tela

    def _desenhar_eixos(self):
        """
        Desenha as linhas de referência X e Y no centro da tela.
        Ajuda a visualizar o ponto de origem das transformações.
        """
        pygame.draw.line(self.screen, VERMELHO, (0, CY), (LARGURA, CY), 1)   # Eixo X
        pygame.draw.line(self.screen, VERDE,    (CX, 0), (CX, ALTURA), 1)    # Eixo Y

    def _desenhar_figura(self, vertices):
        
        #Liga os vértices da figura com linhas, formando o polígono ou elipse.
        n = len(vertices)
        if n < 2:   # Se tiver menos de 2 vértices, não é polígono, então não desenha.
            return
        
        for i in range(n):
            pygame.draw.line(
                self.screen,    # Tela onde a linha será desenhada
                BRANCO,
                vertices[i],    # Vértice atual
                vertices[(i + 1) % n],  # % n para conectar o último vértice de volta ao primeiro
                2
            )

    def _desenhar_hud(self, model):
        """
        Exibe a hud no canto superior esquerdo.

        As linhas exibidas mudam de acordo com o modo atual (polígono ou elipse),
        e a cor do texto muda para destacar em qual modo estamos.
        """
        if model.modo_elipse:
            cor     = AMARELO
            modo_str = "ELIPSE"
            linhas  = [
                f"Modo: {modo_str}(TAB)",
                f"Raio A (horiz) : {model.raio_a}px (← →)",
                f"Raio B (vert)  : {model.raio_b}px (↑ ↓)",
                f"Lados          : {model.n}",
                f"Transladar     : ({model.tx}, {model.ty}) (WASD)",
                f"Rotação        : {math.degrees(model.angulo):.1f}° (QE)",
                f"Escala         : {model.escala:.2f}(ZX)",
                f"Cisalh.        : ({model.shx:.2f}, {model.shy:.2f})(CV / BN)",
                f"Reset          : R",
            ]
        else:
            cor     = CINZA
            modo_str = "POLÍGONO"
            linhas  = [
                f"Modo: {modo_str} (TAB)",
                f"Lados      : {model.n} (↑ ↓)",
                f"Transladar : ({model.tx}, {model.ty}) (WASD)",
                f"Rotação    : {math.degrees(model.angulo):.1f}° (QE)",
                f"Escala     : {model.escala:.2f} (ZX)",
                f"Cisalh.    : ({model.shx:.2f}, {model.shy:.2f}) (CV / BN)",
                f"Reset      : R",
            ]

        for i, linha in enumerate(linhas):
            superficie = self.fonte.render(linha, True, cor)    #Renderiza o texto da linha com a cor definida
            self.screen.blit(superficie, (10, 10 + i * 26)) #Desenha a linha na tela, com um espaçamento vertical de 26 pixels entre as linhas

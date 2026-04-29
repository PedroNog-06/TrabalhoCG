"""
Recebe o que o usuário fez e atualiza o Model de acordo.

Dois tipos de teclas são tratados de formas diferentes:
- Eventos discretos (KEYDOWN): acionados uma única vez por pressão.
  Exemplo: TAB para trocar de modo, R para resetar.

- Teclas contínuas (get_pressed): verificadas a cada frame enquanto
  a tecla estiver pressionada. Exemplo: WASD para mover suavemente.
"""

import pygame


class Controller:
    """
    Processa entradas do teclado e traduz em ações no Model.

    A separação entre eventos discretos e contínuos existe porque o pygame
    trata esses dois casos de formas diferentes. 
    O comportamento que queremos também é diferente: um reset só deve acontecer uma vez,
    mas o movimento com WASD deve ser suave e contínuo.
    """

    def __init__(self, model):
        self.model = model
        self.rodando = True    # Quando False, o loop principal encerra

    def processar_eventos(self, eventos):
        """
        Trata a fila de eventos do pygame -> coisas que aconteceram uma vez.

        Chamado no início de cada frame com a lista de eventos acumulados.
        """
        for event in eventos:

            # Usuário fechou a janela
            if event.type == pygame.QUIT:
                self.rodando = False

            # Tecla pressionada (evento único)
            if event.type == pygame.KEYDOWN:

                # TAB alterna entre modo polígono e elipse
                if event.key == pygame.K_TAB:
                    self.model.alternar_modo()

                # R reseta todas as transformações
                if event.key == pygame.K_r:
                    self.model.resetar()

                # Setas ↑↓ adicionam/removem lados (só no modo polígono)
                if not self.model.modo_elipse:
                    if event.key == pygame.K_UP:
                        self.model.incrementar_lados()

                    if event.key == pygame.K_DOWN:
                        self.model.decrementar_lados()


    def processar_teclas_continuas(self):
        """
        Verifica quais teclas estão sendo seguradas neste frame.

        Diferente dos eventos, isso é verificado a cada frame — por isso
        o movimento é suave ao segurar uma tecla.
        """
        teclas = pygame.key.get_pressed()

        # Translação (WASD)
        if teclas[pygame.K_w]: self.model.ty -= 3
        if teclas[pygame.K_s]: self.model.ty += 3
        if teclas[pygame.K_a]: self.model.tx -= 3
        if teclas[pygame.K_d]: self.model.tx += 3

        # Rotação (Q = sentido anti-horário, E = horário)
        if teclas[pygame.K_q]: self.model.angulo -= 0.03
        if teclas[pygame.K_e]: self.model.angulo += 0.03

        # Escala (Z diminui, X aumenta)
        if teclas[pygame.K_z]: self.model.escala = max(0.1, self.model.escala - 0.01)
        if teclas[pygame.K_x]: self.model.escala += 0.01

        # Cisalhamento horizontal (C diminui, V aumenta)
        if teclas[pygame.K_c]: self.model.shx -= 0.01
        if teclas[pygame.K_v]: self.model.shx += 0.01

        # Cisalhamento vertical (B diminui, N aumenta)
        if teclas[pygame.K_b]: self.model.shy -= 0.01
        if teclas[pygame.K_n]: self.model.shy += 0.01

        # Controles do modo elipse (setas ajustam os raios)
        if self.model.modo_elipse:
            if teclas[pygame.K_RIGHT]: self.model.aumentar_raio_a()
            if teclas[pygame.K_LEFT]:  self.model.diminuir_raio_a()
            if teclas[pygame.K_UP]:    self.model.aumentar_raio_b()
            if teclas[pygame.K_DOWN]:  self.model.diminuir_raio_b()

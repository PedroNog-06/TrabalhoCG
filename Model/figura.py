from Model.config import CX, CY, RAIO_POL, RAIO_A ,RAIO_B
from Model.geometria import gerar_vertices_poligono, gerar_vertices_elipse
from Model.transformacoes import (
    mat_translacao, mat_rotacao, mat_escala, mat_cisalhamento, aplicar_transformacao
)
"""
    Guarda tudo que define o estado atual da figura na tela.

    A View lê esses dados para saber o que desenhar.
    O Controller modifica esses dados conforme o usuário aperta teclas.
"""

class FiguraModel:
    def __init__(self):
        self.modo_elipse = False        # Modo atual: polígono ou elipse
        self.n = 3                      # Começa no Triangulo
        self.raio = RAIO_POL            # Raio do Polígono

        self.raio_a = RAIO_A            # Raio Horizontal
        self.raio_b = RAIO_B            # Raio Vertical

        self.tx = 0                     # Deslocamento horizontal
        self.ty = 0                     # Deslocamento vertical
        self.angulo = 0.0               # Rotação em radianos
        self.escala = 1.0               # Fator de escala (1.0 = tamanho original)
        self.shx = 0.0                  # Cisalhamento horizontal
        self.shy = 0.0                  # Cisalhamento vertical

         # Vértices originais (sem transformação) — recalculados só quando necessário
        self._vertices_base = []
        self._precisa_regen = True  # Flag: indica que os vértices precisam ser recalculados

        # Gera os vértices iniciais
        self._regenerar_vertices()

    @property       # Permite acessar como atributo, mas é calculado na hora
    def vertices_transformados(self):
        """
            Retorna os vértices com todas as transformações aplicadas.

            É recalculado toda vez que essa propriedade é lida, então a View
            sempre recebe os dados mais atuais sem precisar pedir explicitamente.
        """

        if self._precisa_regen: # Se for True, os parâmetros precisam ser remodelados
            self._regenerar_vertices()

        # Constrói a matriz de transformação com base nos parâmetros atuais
        M = (
            mat_translacao(CX + self.tx, CY + self.ty)
            @ mat_rotacao(self.angulo)
            @ mat_escala(self.escala, self.escala)
            @ mat_cisalhamento(self.shx, self.shy)
            @ mat_translacao(-CX, -CY)
        )

        return aplicar_transformacao(self._vertices_base, M)     # Aplica a matriz de transformação aos vértices base e retorna os vértices transformados

    def _regenerar_vertices(self):
        # Recria os vértices base de acordo com o modo atual.

        if self.modo_elipse:
            self._vertices_base = gerar_vertices_elipse(self.n, self.raio_a, self.raio_b, CX, CY) #Gera os vértices da elipse com os parâmetros atuais
        else:
            self._vertices_base = gerar_vertices_poligono(self.n, self.raio, CX, CY)    #Gera os vértices do polígono com os parâmetros atuais

        self._precisa_regen = False  # Depois de regenerar, marca que os vértices estão atualizados e não precisam ser recalculados novamente até que algum parâmetro mude

    def alternar_modo(self):
        # Troca entre modo polígono e modo elipse.
        self.modo_elipse = not self.modo_elipse #Altera o valor do booleano
        self._precisa_regen = True  # Marca que os vértices precisam ser recalculados, porque o modo mudou e os vértices do polígono e da elipse são diferentes.

    def incrementar_lados(self):
        self.n += 1  # Aumenta o número de lados do polígono
        self._precisa_regen = True

    def decrementar_lados(self):
        self.n = max(3, self.n - 1) # Mínimo de 3 lados (triângulo)
        self._precisa_regen = True

    def aumentar_raio_a(self):
        self.raio_a = max(10, self.raio_a + 1)  # Aumenta o raio horizontal da elipse, com um mínimo de 10 pixels para evitar que fique muito achatada
        self._precisa_regen = True

    def diminuir_raio_a(self):
        self.raio_a = max(10, self.raio_a - 1)  # Diminui o raio horizontal da elipse, com um mínimo de 10 pixels para evitar que fique muito achatada
        self._precisa_regen = True

    def aumentar_raio_b(self):
        self.raio_b = max(10, self.raio_b + 1)  # Aumenta o raio vertical da elipse, com um mínimo de 10 pixels para evitar que fique muito achatada
        self._precisa_regen = True

    def diminuir_raio_b(self):
        self.raio_b = max(10, self.raio_b - 1)  # Diminui o raio vertical da elipse, com um mínimo de 10 pixels para evitar que fique muito achatada
        self._precisa_regen = True

    def resetar(self):
        # Volta todas as transformações e quantidade de vértices para os valores iniciais.

        self.tx = 0
        self.ty = 0
        self.angulo = 0.0
        self.escala = 1.0
        self.shx = 0.0
        self.shy = 0.0
        if (self.modo_elipse == False):
            self.raio = RAIO_POL
        else:
            self.raio_a = RAIO_A
            self.raio_b = RAIO_B
        self.n= 3
        self._precisa_regen = True
"""
Aqui ficam todas as informações sobre a figura atual (quantos lados tem,
onde ela está, o quanto foi rotacionada, etc.) e toda a matemática por trás
das transformações
"""

import math
import numpy as np


# ------ Configuração da Tela ------
LARGURA  = 800
ALTURA   = 600
CX       = LARGURA  // 2   # Centro X da tela
CY       = ALTURA   // 2   # Centro Y da tela
RAIO_POL = 150             # Raio padrão do polígono regular


#Geração de vértices pra o polígono e a elipse
def gerar_vertices_poligono(n, raio, cx, cy):
    """
    Calcula os pontos de um polígono regular com 'n' lados.

    A ideia é distribuir 'n' pontos igualmente ao redor de um círculo.
    Para cada ponto, usamos seno e cosseno para descobrir onde ele fica
    no espaço.

    Em telas do Pygame, o Y cresce para baixo, então precisamos inverter para o polígono ficar correto.
    """
    vertices = []
    for i in range(n):  #Para cada vértice:
        angulo = (2 * math.pi / n) * i         # Divide o círculo em 'n' partes iguais
        x = cx + raio * math.cos(angulo)
        y = cy - raio * math.sin(angulo)        # Invertido por causa do sistema de coordenadas da tela
        vertices.append((x, y))
    return vertices


def gerar_vertices_elipse(n, a, b, cx, cy):
    """
    Calcula os pontos de uma elipse aproximada por 'n' segmentos de reta.

    Funciona igual ao polígono, mas com dois raios diferentes:
    - 'a' controla o tamanho horizontal
    - 'b' controla o tamanho vertical

    Quanto maior o 'n', mais suave e redondinha a elipse aparece.
    Com n=4, por exemplo, você veria um losango.
    """
    vertices = []
    for i in range(n):  #Para cada vértice:
        angulo = (2 * math.pi / n) * i       # Divide o círculo em 'n' partes iguais
        x = cx + a * math.cos(angulo)
        y = cy - b * math.sin(angulo)   # Invertido por causa do sistema de coordenadas da tela
        vertices.append((x, y))
    return vertices

"""
Cada função abaixo cria uma matriz de transformação que, 
ao ser multiplicada por um ponto, move/rotaciona/deforma esse ponto.
Usamos coordenadas homogêneas (x, y, 1) para que todas as transformações
possam ser combinadas com uma única multiplicação de matrizes.
"""

def mat_translacao(tx, ty):
    """
    Move a figura para outro lugar.
    tx e ty indicam quantos pixels mover em X e Y.
    """
    return np.array([   #Escolhemos numpy para facilitar a manipulação de matrizes
        [1, 0, tx],
        [0, 1, ty],
        [0, 0,  1]
    ], dtype=float)


def mat_rotacao(theta):
    """
    Gira a figura em torno da origem.
    theta é o ângulo em radianos. math.radians() para converter de graus
    """
    cos = math.cos(theta)
    sen = math.sin(theta)
    return np.array([
        [cos, -sen, 0],     #Invertido no seno por conta do Y ser invertido na tela.
        [sen,  cos, 0],
        [  0,    0, 1]
    ], dtype=float)


def mat_escala(sx, sy):
    """
    Aumenta ou diminui a figura.
    por exemplo: sx = 2 dobra o tamanho em X, sy = 0.5 reduz pela metade em Y
    """
    return np.array([
        [sx,  0, 0],
        [ 0, sy, 0],
        [ 0,  0, 1]
    ], dtype=float)


def mat_cisalhamento(shx, shy):
    """
    "Inclina" a figura, como se você empurrasse só o topo para o lado.
    shx inclina horizontalmente, shy inclina verticalmente.
    """
    return np.array([
        [  1, shx, 0],
        [shy,   1, 0],
        [  0,   0, 1]
    ], dtype=float)


def aplicar_transformacao(vertices, matriz):
    """
    Aplica uma matriz de transformação a todos os vértices da figura.

    Para cada ponto (x, y), convertemos para (x, y, 1) e multiplicamos
    pela matriz. O resultado dá o novo (x, y) transformado
    """
    resultado = []
    for (x, y) in vertices: 
        ponto = np.array([x, y, 1]) #Coordenadas homogêneas
        novo  = matriz @ ponto              # '@' é o operador de multiplicação de matrizes
        resultado.append((novo[0], novo[1]))    #Novo ponto transformado
    return resultado


def construir_matriz_composta(cx, cy, tx, ty, angulo, escala, shx, shy):
    """
    Combina todas as transformações numa única matriz.

    A ordem importa! O que fazemos aqui é:
    1. Mover a figura para a origem para que rotação e escala funcionem no centro
    2. Aplicar o cisalhamento
    3. Aplicar a escala
    4. Aplicar a rotação
    5. Devolver a figura ao centro da tela e aplicar a translação do usuário

    Isso evita que a figura gire em torno do canto da tela em vez do próprio centro.
    """
    return (
        mat_translacao(cx + tx, cy + ty) @  #Primeiro move a figura pro centro da tela já com a translação do usuário
        mat_rotacao(angulo)              @  #Depois aplica a rotação
        mat_escala(escala, escala)       @  #Depois a escala
        mat_cisalhamento(shx, shy)       @  #Depois o cisalhamento
        mat_translacao(-cx, -cy)    #Por fim, move a figura de volta pro lugar original com as transformações aplicadas
    )


class FiguraModel:
    """
    Guarda tudo que define o estado atual da figura na tela.

    A View lê esses dados para saber o que desenhar.
    O Controller modifica esses dados conforme o usuário aperta teclas.
    """

    def __init__(self):
        # Modo atual: polígono ou elipse
        self.modo_elipse = False

        # Parâmetros do polígono
        self.n    = 5           # Número de lados (começa como pentágono)
        self.raio = RAIO_POL    # Raio do polígono

        # Parâmetros da elipse
        self.raio_a = 200       # Raio horizontal
        self.raio_b = 100       # Raio vertical

        # Transformações aplicadas pelo usuário
        self.tx     = 0         # Deslocamento horizontal
        self.ty     = 0         # Deslocamento vertical
        self.angulo = 0.0       # Rotação em radianos
        self.escala = 1.0       # Fator de escala (1.0 = tamanho original)
        self.shx    = 0.0       # Cisalhamento horizontal
        self.shy    = 0.0       # Cisalhamento vertical

        # Vértices originais (sem transformação) — recalculados só quando necessário
        self._vertices_base  = []
        self._precisa_regen  = True     # Flag: indica que os vértices precisam ser recalculados

        # Gera os vértices iniciais
        self._regenerar_vertices()


    @property   # Permite acessar como atributo, mas é calculado na hora
    def vertices_transformados(self):
        """
        Retorna os vértices com todas as transformações aplicadas.

        É recalculado toda vez que essa propriedade é lida, então a View
        sempre recebe os dados mais atuais sem precisar pedir explicitamente.
        """
        if self._precisa_regen:     # Se for True, os parâmetros precisam ser remodelados
            self._regenerar_vertices()

        M = construir_matriz_composta(  #Constrói a matriz de transformação com base nos parâmetros atuais
            CX, CY,
            self.tx, self.ty,
            self.angulo,
            self.escala,
            self.shx, self.shy
        )
        return aplicar_transformacao(self._vertices_base, M)    #Aplica a matriz de transformação aos vértices base e retorna os vértices transformados


    def _regenerar_vertices(self):
        #Recria os vértices base de acordo com o modo atual.
        if self.modo_elipse:
            self._vertices_base = gerar_vertices_elipse(
                self.n, self.raio_a, self.raio_b, CX, CY    #Gera os vértices da elipse com os parâmetros atuais
            )
        else:
            self._vertices_base = gerar_vertices_poligono(
                self.n, self.raio, CX, CY   #Gera os vértices do polígono com os parâmetros atuais
            )
        self._precisa_regen = False     #Depois de regenerar, marca que os vértices estão atualizados e não precisam ser recalculados novamente até que algum parâmetro mude


    def alternar_modo(self):
        #Troca entre modo polígono e modo elipse.
        self.modo_elipse = not self.modo_elipse #Altera o valor do booleano
        self._precisa_regen = True  #Marca que os vértices precisam ser recalculados, porque o modo mudou e os vértices do polígono e da elipse são diferentes.


    def incrementar_lados(self):
        self.n += 1     #Aumenta o número de lados do polígono
        self._precisa_regen = True  #Marca que os vértices precisam ser recalculados, porque o modo mudou e os vértices do polígono e da elipse são diferentes.


    def decrementar_lados(self):
        self.n = max(3, self.n - 1)     # Mínimo de 3 lados (triângulo)
        self._precisa_regen = True  #Marca que os vértices precisam ser recalculados, porque o modo mudou e os vértices do polígono e da elipse são diferentes.


    def aumentar_raio_a(self):
        self.raio_a = max(10, self.raio_a + 1)  #Aumenta o raio horizontal da elipse, com um mínimo de 10 pixels para evitar que fique muito achatada
        self._precisa_regen = True  #Marca que os vértices precisam ser recalculados, porque o modo mudou e os vértices do polígono e da elipse são diferentes.

    def diminuir_raio_a(self):
        self.raio_a = max(10, self.raio_a - 1)  #Diminui o raio horizontal da elipse, com um mínimo de 10 pixels para evitar que fique muito achatada
        self._precisa_regen = True  #Marca que os vértices precisam ser recalculados, porque o modo mudou e os vértices do polígono e da elipse são diferentes.

    def aumentar_raio_b(self):
        self.raio_b = max(10, self.raio_b + 1)  #Aumenta o raio vertical da elipse, com um mínimo de 10 pixels para evitar que fique muito achatada
        self._precisa_regen = True  #Marca que os vértices precisam ser recalculados, porque o modo mudou e os vértices do polígono e da elipse são diferentes.

    def diminuir_raio_b(self):
        self.raio_b = max(10, self.raio_b - 1)  #Diminui o raio vertical da elipse, com um mínimo de 10 pixels para evitar que fique muito achatada
        self._precisa_regen = True  #Marca que os vértices precisam ser recalculados, porque o modo mudou e os vértices do polígono e da elipse são diferentes.

    def resetar(self):
        #Volta todas as transformações para os valores iniciais.
        self.tx     = 0
        self.ty     = 0
        self.angulo = 0.0
        self.escala = 1.0
        self.shx    = 0.0
        self.shy    = 0.0

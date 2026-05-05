import numpy as np
import math

"""
Cada função abaixo cria uma matriz de transformação que, 
ao ser multiplicada por um ponto, move/rotaciona/deforma esse ponto.
Usamos coordenadas homogêneas (x, y, 1) para que todas as transformações
possam ser combinadas com uma única multiplicação de matrizes.
"""
# Escolhemos numpy para facilitar a manipulação de matrizes

def mat_translacao(tx, ty):
    """
        Move a figura para outro lugar.
        tx e ty indicam quantos pixels mover em X e Y.
    """

    return np.array([
                            [1,0,tx],
                            [0,1,ty],
                            [0,0,1]
                           ], dtype=float)

def mat_rotacao(theta):
    """
        Gira a figura em torno da origem.
        theta é o ângulo em radianos. math.radians() para converter de graus
    """

    cos, sen = math.cos(theta), math.sin(theta)
    return np.array([
                            [cos,-sen,0],        #Invertido no seno por conta do Y ser invertido na tela.
                            [sen,cos,0],
                            [0,0,1]
                           ], dtype=float)

def mat_escala(sx, sy):
    """
        Aumenta ou diminui a figura.
        por exemplo: sx = 2 dobra o tamanho em X, sy = 0.5 reduz pela metade em Y
    """

    return np.array([
                            [sx,0,0],
                            [0,sy,0],
                            [0,0,1]
                           ], dtype=float)

def mat_cisalhamento(shx, shy):
    """
        "Inclina" a figura, como se você empurrasse só o topo para o lado.
        shx inclina horizontalmente, shy inclina verticalmente.
    """

    return np.array([
                            [1,shx,0],
                            [shy,1,0],
                            [0,0,1]
                           ], dtype=float)


def aplicar_transformacao(vertices, matriz):
    """
        Aplica uma matriz de transformação a todos os vértices da figura.

        Para cada ponto (x, y), convertemos para (x, y, 1) e multiplicamos
        pela matriz. O resultado dá o novo (x, y) transformado
    """

    resultado = []
    for x, y in vertices:
        ponto = np.array([x, y, 1])
        novo = matriz @ ponto
        resultado.append((novo[0], novo[1]))
    return resultado
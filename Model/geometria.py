import math

def gerar_vertices_poligono(n, raio, cx, cy):
    """
        Calcula os pontos de um polígono regular com 'n' lados.

        A ideia é distribuir 'n' pontos igualmente ao redor de um círculo.
        Para cada ponto, usamos seno e cosseno para descobrir onde ele fica
        no espaço.

        Em telas do Pygame, o Y cresce para baixo, então precisamos inverter para o polígono ficar correto.
    """

    vertices = []
    for i in range(n):                           # Para cada vértice:
        angulo = (2 * math.pi / n) * i           # Divide o círculo em 'n' partes iguais
        x = cx + raio * math.cos(angulo)
        y = cy - raio * math.sin(angulo)         # Invertido por causa do sistema de coordenadas da tela
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

    vertices = []                          # Semelhante ao Poligono
    for i in range(n):
        angulo = (2 * math.pi / n) * i
        x = cx + a * math.cos(angulo)
        y = cy - b * math.sin(angulo)
        vertices.append((x, y))
    return vertices
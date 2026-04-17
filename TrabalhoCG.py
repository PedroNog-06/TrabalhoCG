import pygame
import math
import numpy as np

pygame.init()

LARGURA, ALTURA = 800, 600
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Passo 5 - Elipse")
clock = pygame.time.Clock()

PRETO  = (0,   0,   0)
BRANCO = (255, 255, 255)
CINZA  = (180, 180, 180)
AMARELO= (255, 255,  0)

CX   = LARGURA // 2
CY   = ALTURA  // 2
RAIO = 150


# ── Funções de vértices ──────────────────────────────────────────

def gerar_vertices(n, raio, cx, cy):
    vertices = []
    for i in range(n):
        angulo = (2 * math.pi / n) * i
        x = cx + raio * math.cos(angulo)
        y = cy - raio * math.sin(angulo)
        vertices.append((x, y))
    return vertices


def gerar_elipse(n, a, b, cx, cy):
    vertices = []
    for i in range(n):
        angulo = (2 * math.pi / n) * i
        x = cx + a * math.cos(angulo)
        y = cy - b * math.sin(angulo)
        vertices.append((x, y))
    return vertices


def desenhar_poligono(screen, vertices, cor, espessura=2):
    n = len(vertices)
    for i in range(n):
        pygame.draw.line(screen, cor, vertices[i], vertices[(i + 1) % n], espessura)


# ── Matrizes de transformação ────────────────────────────────────

def mat_translacao(tx, ty):
    return np.array([[1, 0, tx],
                     [0, 1, ty],
                     [0, 0,  1]], dtype=float)

def mat_rotacao(theta):
    c, s = math.cos(theta), math.sin(theta)
    return np.array([[ c, -s, 0],
                     [ s,  c, 0],
                     [ 0,  0, 1]], dtype=float)

def mat_escala(sx, sy):
    return np.array([[sx,  0, 0],
                     [ 0, sy, 0],
                     [ 0,  0, 1]], dtype=float)

def mat_cisalhamento(shx, shy):
    return np.array([[  1, shx, 0],
                     [shy,   1, 0],
                     [  0,   0, 1]], dtype=float)

def aplicar_transformacao(vertices, matriz):
    resultado = []
    for (x, y) in vertices:
        ponto = np.array([x, y, 1])
        novo  = matriz @ ponto
        resultado.append((novo[0], novo[1]))
    return resultado

def desenhar_eixos(screen):
    pygame.draw.line(screen, (200, 0, 0), (0, CY), (LARGURA, CY), 1)  # X vermelho
    pygame.draw.line(screen, (0, 200, 0), (CX, 0), (CX, ALTURA), 1)   # Y verde


# ── Estado inicial ───────────────────────────────────────────────

n           = 6
tx, ty      = 0, 0
angulo      = 0.0
escala      = 1.0
shx, shy    = 0.0, 0.0
raio_a      = 200       # raio horizontal da elipse
raio_b      = 100       # raio vertical da elipse
modo_elipse = False
atualizar   = True
vertices_base = []

fonte = pygame.font.SysFont("monospace", 20)


# ── Loop principal ───────────────────────────────────────────────

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                modo_elipse = not modo_elipse
                atualizar = True

            if event.key == pygame.K_r:
                tx, ty   = 0, 0
                angulo   = 0.0
                escala   = 1.0
                shx, shy = 0.0, 0.0

            if not modo_elipse:
                if event.key == pygame.K_UP:
                    n += 1
                    atualizar = True
                if event.key == pygame.K_DOWN:
                    n = max(3, n - 1)
                    atualizar = True

    # Regenera vértices base se necessário
    if atualizar:
        if modo_elipse:
            vertices_base = gerar_elipse(n, raio_a, raio_b, CX, CY)
        else:
            vertices_base = gerar_vertices(n, RAIO, CX, CY)
        atualizar = False

    # Teclas contínuas
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_w]: ty -= 3
    if teclas[pygame.K_s]: ty += 3
    if teclas[pygame.K_a]: tx -= 3
    if teclas[pygame.K_d]: tx += 3
    if teclas[pygame.K_q]: angulo -= 0.03
    if teclas[pygame.K_e]: angulo += 0.03
    if teclas[pygame.K_z]: escala = max(0.1, escala - 0.01)
    if teclas[pygame.K_x]: escala += 0.01
    if teclas[pygame.K_c]: shx -= 0.01
    if teclas[pygame.K_v]: shx += 0.01
    if teclas[pygame.K_b]: shy -= 0.01
    if teclas[pygame.K_n]: shy += 0.01

    if modo_elipse:
        if teclas[pygame.K_RIGHT]:
            raio_a = max(10, raio_a + 1)
            atualizar = True
        if teclas[pygame.K_LEFT]:
            raio_a = max(10, raio_a - 1)
            atualizar = True
        if teclas[pygame.K_UP]:
            raio_b = max(10, raio_b + 1)
            atualizar = True
        if teclas[pygame.K_DOWN]:
            raio_b = max(10, raio_b - 1)
            atualizar = True

    # Monta matriz composta
    M = (
        mat_translacao(CX + tx, CY + ty) @
        mat_rotacao(angulo)              @
        mat_escala(escala, escala)       @
        mat_cisalhamento(shx, shy)       @
        mat_translacao(-CX, -CY)
    )
    vertices_transformados = aplicar_transformacao(vertices_base, M)

    # Desenha
    screen.fill(PRETO)
    desenhar_eixos(screen)                                        # ← aqui
    desenhar_poligono(screen, vertices_transformados, BRANCO)

    # HUD — muda de cor dependendo do modo
    cor_modo = AMARELO if modo_elipse else CINZA
    modo_str = "ELIPSE" if modo_elipse else "POLÍGONO"

    if modo_elipse:
        hud = [
            f"Modo: {modo_str}              (TAB)",
            f"Raio A (horiz) : {raio_a}px   (←→)",
            f"Raio B (vert)  : {raio_b}px   (↑↓)",
            f"Lados          : {n}",
            f"Transladar     : ({tx}, {ty})  (WASD)",
            f"Rotação        : {math.degrees(angulo):.1f}°  (QE)",
            f"Escala         : {escala:.2f}         (ZX)",
            f"Cisalh.        : ({shx:.2f}, {shy:.2f})   (CV / BN)",
            f"Reset          : R",
        ]
    else:
        hud = [
            f"Modo: {modo_str}            (TAB)",
            f"Lados      : {n}            (↑↓)",
            f"Transladar : ({tx}, {ty})   (WASD)",
            f"Rotação    : {math.degrees(angulo):.1f}°  (QE)",
            f"Escala     : {escala:.2f}        (ZX)",
            f"Cisalh.    : ({shx:.2f}, {shy:.2f})  (CV / BN)",
            f"Reset      : R",
        ]

    for i, linha in enumerate(hud):
        surf = fonte.render(linha, True, cor_modo)
        screen.blit(surf, (10, 10 + i * 26))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
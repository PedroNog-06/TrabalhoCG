# Computação Gráfica — Transformações 2D com Pygame

Projeto desenvolvido para a disciplina de Computação Gráfica. O objetivo é demonstrar na prática como funcionam as principais transformações geométricas 2D — translação, rotação, escala e cisalhamento — aplicadas sobre polígonos regulares e elipses, usando matrizes homogêneas.

---

## Sobre o projeto

A aplicação exibe uma figura geométrica interativa numa janela pygame. O usuário pode, em tempo real, mover, girar, esticar e inclinar a figura usando o teclado. Todas as transformações são calculadas via multiplicação de matrizes 3×3 (coordenadas homogêneas), o que é a base matemática padrão para transformações em computação gráfica.

O projeto foi estruturado no padrão **MVC (Model-View-Controller)**, separando claramente:
- A **lógica e o estado** da figura
- A **renderização** na tela
- O **tratamento de entrada** do usuário

---

## Funcionalidades

- Geração de **polígonos regulares** com número de lados configurável (mínimo: triângulo)
- Geração de **elipses** aproximadas por segmentos de reta, com raios ajustáveis independentemente
- Transformações aplicáveis em tempo real:
  - **Translação** (mover a figura)
  - **Rotação** (girar em torno do próprio centro)
  - **Escala** (aumentar/diminuir)
  - **Cisalhamento** (inclinar horizontal e verticalmente)
- HUD na tela exibindo os valores atuais de cada transformação
- Reset instantâneo para o estado inicial

---

## Controles

| Tecla | Ação |
|---|---|
| `TAB` | Alterna entre modo Polígono e Elipse |
| `↑` / `↓` | Adiciona/remove lados (polígono) ou ajusta raio vertical (elipse) |
| `←` / `→` | Ajusta raio horizontal (apenas no modo elipse) |
| `W` `A` `S` `D` | Move a figura |
| `Q` / `E` | Gira a figura |
| `Z` / `X` | Diminui/aumenta a escala |
| `C` / `V` | Cisalhamento horizontal |
| `B` / `N` | Cisalhamento vertical |
| `R` | Reseta todas as transformações |

---

## Estrutura do projeto

```
/
├── main.py          # Ponto de entrada — inicializa o pygame e mantém o loop principal
├── model.py         # Estado da figura e toda a matemática (matrizes, geração de vértices)
├── view.py          # Renderização na tela (figura, eixos, HUD)
└── controller.py    # Leitura do teclado e atualização do model
```

### Por que MVC?

Num código de jogo ou simulação, é fácil acabar com tudo misturado no mesmo loop: lógica, desenho e input num arquivo só. O MVC força uma separação que torna o código mais fácil de entender, modificar e expandir. Se quiser mudar a cor do HUD, você mexe só na View. Se quiser adicionar uma nova transformação, você mexe só no Model e no Controller — a View não precisa saber que aquilo existe.

---

## Tecnologias

- **Python 3**
- **Pygame** — janela, renderização e captura de input
- **NumPy** — operações com matrizes para as transformações geométricas

---

## Como executar

**1. Clone o repositório**
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

**2. Instale as dependências**
```bash
pip install pygame numpy
```

**3. Execute**
```bash
python main.py
```

---

## Conceitos abordados

- **Coordenadas homogêneas:** representar pontos 2D como vetores 3D `(x, y, 1)` para que translação, rotação, escala e cisalhamento possam ser combinados numa única multiplicação de matrizes.
- **Composição de transformações:** a ordem em que as matrizes são multiplicadas importa. Neste projeto, a figura é sempre movida para a origem antes de ser transformada, garantindo que rotação e escala aconteçam em torno do próprio centro.
- **Aproximação de elipses por polígonos:** quanto mais lados, mais suave a curva — a elipse é, na prática, um polígono com muitos lados e dois raios diferentes.

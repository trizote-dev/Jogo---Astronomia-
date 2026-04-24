import pygame

# Inicializa pygame (deve ser feito uma vez)
pygame.init()

# Tela
LARGURA = 800
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Sobrevivência em Marte")

# Fontes e cores
fonte = pygame.font.SysFont("consolas", 24, bold=True)
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 100)
CINZA = (150, 150, 150)
VERMELHO = (255, 50, 50)
AZUL = (50, 150, 255)
VERDE = (80, 200, 120)

# Carregar imagens
# Atenção: o caminho dos arquivos deve estar correto, relativo a onde você executa o jogo.
fundo = pygame.image.load("assets/fundo_marte.png")
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

astronauta_vivo = pygame.image.load("assets/astronauta_vivo.png").convert_alpha()
astronauta_vivo = pygame.transform.scale(astronauta_vivo, (70, 70))
astronauta_morto = pygame.image.load("assets/astronauta_morto.png").convert_alpha()
astronauta_morto = pygame.transform.scale(astronauta_morto, (70, 70))


def tela_inicial():
    """Desenha a tela inicial"""
    TELA.blit(fundo, (0, 0))
    titulo = fonte.render("🚀 Sobrevivência em Marte 🚀", True, AMARELO)
    instrucao = fonte.render("Pressione ENTER para começar", True, BRANCO)
    TELA.blit(titulo, (200, 200))
    TELA.blit(instrucao, (240, 300))
    pygame.display.flip()


def desenhar_barra(x, y, valor, cor, icone_surf):
    """Desenha uma barra de status para valor entre 0 e 5"""
    largura_total = 100
    altura = 12
    # fundo da barra (cinza escuro)
    pygame.draw.rect(TELA, (80, 80, 80), (x, y, largura_total, altura))
    # preenchimento proporcional
    if valor > 0:
        proporcao = valor / 5  # supondo máximo 5
        pygame.draw.rect(TELA, cor, (x, y, largura_total * proporcao, altura))
    # desenhar ícone (ex: 💧, 🍖, ⚡) à esquerda
    TELA.blit(icone_surf, (x - 25, y - 8))


def desenhar_tela(dia, astronautas, selecionado, game_over, score_final=None):
    """Desenha o jogo visualmente na tela"""
    # fundo
    TELA.blit(fundo, (0, 0))

    # dia
    texto_dia = fonte.render(f"🌙 Dia {dia}", True, BRANCO)
    TELA.blit(texto_dia, (20, 20))

    # astronautas + barras
    for i, astro in enumerate(astronautas):
        # posição do sprite
        x = 120 + i * 160
        y = 250

        # escolher imagem conforme vivo/morto
        if astro.vivo:
            img = astronauta_vivo
        else:
            img = astronauta_morto

        # desenhar
        TELA.blit(img, (x, y))

        # se for o selecionado e vivo, desenhar contorno
        if i == selecionado and astro.vivo:
            pygame.draw.rect(TELA, AMARELO, (x - 5, y - 5, 80, 80), 3)

        # nome
        cor_nome = BRANCO if astro.vivo else CINZA
        nome_texto = fonte.render(astro.nome, True, cor_nome)
        TELA.blit(nome_texto, (x - 10, y + 80))

        # barras de status (água, comida, energia) com ícones simples
        ic_agua = fonte.render("💧", True, AZUL)
        ic_comida = fonte.render("🍖", True, (255, 165, 0))
        ic_energia = fonte.render("⚡", True, VERDE)

        desenhar_barra(x, y + 100, astro.agua, AZUL, ic_agua)
        desenhar_barra(x, y + 120, astro.comida, (255, 165, 0), ic_comida)
        desenhar_barra(x, y + 140, astro.energia, VERDE, ic_energia)

    # HUD inferior (comandos)
    pygame.draw.rect(TELA, (0, 0, 0, 180), (0, 530, LARGURA, 70))
    comandos = [
        "[ESPAÇO] Avançar Dia",
        "[1-4] Selecionar Astronauta",
        "[A] Coletar Água",
        "[C] Comer"
    ]
    for i, instr in enumerate(comandos):
        texto = fonte.render(instr, True, BRANCO)
        TELA.blit(texto, (20 + i * 200, 550))

    # se game over, desenhar overlay escuro + mensagens
    if game_over:
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        TELA.blit(overlay, (0, 0))

        texto_go = fonte.render("💀 GAME OVER 💀", True, VERMELHO)
        TELA.blit(texto_go, (300, 200))

        if score_final is not None:
            texto_score = fonte.render(f"Você sobreviveu {score_final} dias!", True, BRANCO)
            TELA.blit(texto_score, (260, 250))

        texto_reiniciar = fonte.render("Pressione R para reiniciar", True, AMARELO)
        TELA.blit(texto_reiniciar, (250, 300))

    pygame.display.flip()

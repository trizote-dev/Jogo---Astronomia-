import pygame

# Cores
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 100)
CINZA = (150, 150, 150)
VERMELHO = (255, 50, 50)
AZUL = (50, 150, 255)
VERDE = (80, 200, 120)

LARGURA = 800
ALTURA = 600

# Variáveis globais — inicializadas depois
TELA = None
fonte = None
fundo = None
astronauta_vivo = None
astronauta_morto = None

def inicializar():
    """Chame isso UMA VEZ no main() antes de qualquer outra coisa."""
    global TELA, fonte, fundo, astronauta_vivo, astronauta_morto

    pygame.init()
    TELA = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Sobrevivência em Marte")

    fonte = pygame.font.SysFont("consolas", 24, bold=True)

    # Caminho absoluto — resolve o problema de "de onde você roda"
    import os
    base = os.path.dirname(os.path.abspath(__file__))

    fundo = pygame.image.load(os.path.join(base, "assets", "fundo_marte.png"))
    fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

    astronauta_vivo = pygame.image.load(os.path.join(base, "assets", "astronauta_vivo.png")).convert_alpha()
    astronauta_vivo = pygame.transform.scale(astronauta_vivo, (70, 70))

    astronauta_morto = pygame.image.load(os.path.join(base, "assets", "astronauta_morto.png")).convert_alpha()
    astronauta_morto = pygame.transform.scale(astronauta_morto, (70, 70))


def tela_inicial():
    TELA.blit(fundo, (0, 0))
    titulo = fonte.render("Sobrevivencia em Marte", True, AMARELO)
    instrucao = fonte.render("Pressione ENTER para comecar", True, BRANCO)
    TELA.blit(titulo, (200, 200))
    TELA.blit(instrucao, (240, 300))
    pygame.display.flip()


def desenhar_barra(x, y, valor, cor, icone_surf):
    largura_total = 100
    altura = 12
    pygame.draw.rect(TELA, (80, 80, 80), (x, y, largura_total, altura))
    if valor > 0:
        proporcao = valor / 5
        pygame.draw.rect(TELA, cor, (x, y, int(largura_total * proporcao), altura))
    TELA.blit(icone_surf, (x - 25, y - 8))


def desenhar_tela(dia, astronautas, selecionado, game_over, score_final=None):
    TELA.blit(fundo, (0, 0))

    texto_dia = fonte.render(f"Dia {dia}", True, BRANCO)
    TELA.blit(texto_dia, (20, 20))

    for i, astro in enumerate(astronautas):
        x = 120 + i * 160
        y = 250
        img = astronauta_vivo if astro.vivo else astronauta_morto
        TELA.blit(img, (x, y))

        if i == selecionado and astro.vivo:
            pygame.draw.rect(TELA, AMARELO, (x - 5, y - 5, 80, 80), 3)

        cor_nome = BRANCO if astro.vivo else CINZA
        nome_texto = fonte.render(astro.nome, True, cor_nome)
        TELA.blit(nome_texto, (x - 10, y + 80))

        ic_agua = fonte.render("A", True, AZUL)
        ic_comida = fonte.render("C", True, (255, 165, 0))
        ic_energia = fonte.render("E", True, VERDE)

        desenhar_barra(x, y + 100, astro.agua, AZUL, ic_agua)
        desenhar_barra(x, y + 120, astro.comida, (255, 165, 0), ic_comida)
        desenhar_barra(x, y + 140, astro.energia, VERDE, ic_energia)

    # HUD inferior — transparência correta
    hud = pygame.Surface((LARGURA, 70))
    hud.set_alpha(180)
    hud.fill((0, 0, 0))
    TELA.blit(hud, (0, 530))

    comandos = ["[ESPACO] Avancar Dia", "[1-4] Selecionar", "[A] Agua", "[C] Comer"]
    for i, instr in enumerate(comandos):
        texto = fonte.render(instr, True, BRANCO)
        TELA.blit(texto, (20 + i * 200, 550))

    if game_over:
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        TELA.blit(overlay, (0, 0))

        texto_go = fonte.render("GAME OVER", True, VERMELHO)
        TELA.blit(texto_go, (300, 200))

        if score_final is not None:
            texto_score = fonte.render(f"Voce sobreviveu {score_final} dias!", True, BRANCO)
            TELA.blit(texto_score, (260, 250))

        texto_reiniciar = fonte.render("Pressione R para reiniciar", True, AMARELO)
        TELA.blit(texto_reiniciar, (250, 300))

    pygame.display.flip()

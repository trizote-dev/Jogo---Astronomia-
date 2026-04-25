import pygame
import sys

try:
    from interface import inicializar, desenhar_tela, tela_inicial
except ImportError as e:
    print(f"Erro ao importar interface.py: {e}")
    input("Pressione Enter para fechar...")
    sys.exit()


class Astronauta:
    def __init__(self, nome):
        self.nome = nome
        self.agua = 3
        self.comida = 3
        self.energia = 3
        self.vivo = True

    def coletar_agua(self):
        if self.vivo:
            self.agua = min(5, self.agua + 1)

    def comer(self):
        if self.vivo and self.comida > 0:
            self.comida -= 1
            self.energia = min(5, self.energia + 1)

    def passar_dia(self):
        if not self.vivo:
            return
        if self.agua > 0:
            self.agua -= 1
        else:
            self.energia -= 1
        if self.comida > 0:
            self.comida -= 1
        else:
            self.energia -= 1
        if self.energia <= 0:
            self.vivo = False


def criar_astronautas():
    return [
        Astronauta("Astro 1"),
        Astronauta("Astro 2"),
        Astronauta("Astro 3"),
        Astronauta("Astro 4")
    ]


def main():
    try:
        inicializar()
    except Exception as e:
        print(f"Erro ao inicializar o jogo: {e}")
        input("Pressione Enter para fechar...")
        sys.exit()

    clock = pygame.time.Clock()
    astronautas = criar_astronautas()
    dia = 1
    selecionado = 0
    game_over = False
    score_final = None
    menu = True
    running = True

    while running:
        if menu:
            tela_inicial()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    astronautas = criar_astronautas()
                    dia = 1
                    selecionado = 0
                    game_over = False
                    score_final = None
                    menu = False
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if not game_over and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        dia += 1
                        for astro in astronautas:
                            astro.passar_dia()
                    if event.key == pygame.K_1:
                        selecionado = 0
                    if event.key == pygame.K_2:
                        selecionado = 1
                    if event.key == pygame.K_3:
                        selecionado = 2
                    if event.key == pygame.K_4:
                        selecionado = 3
                    if astronautas[selecionado].vivo:
                        if event.key == pygame.K_a:
                            astronautas[selecionado].coletar_agua()
                        if event.key == pygame.K_c:
                            astronautas[selecionado].comer()
                if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    astronautas = criar_astronautas()
                    dia = 1
                    selecionado = 0
                    game_over = False
                    score_final = None
                    menu = True

            if not game_over and all(not astro.vivo for astro in astronautas):
                game_over = True
                score_final = dia

            desenhar_tela(dia, astronautas, selecionado, game_over, score_final)

        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

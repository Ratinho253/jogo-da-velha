import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da tela
largura, altura = 500, 500
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo da Velha")

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (255, 0, 0)
azul = (0, 0, 255)
cor_borda = (255, 255, 0)  # Cor da borda (amarelo)
espessura_borda = 17

# Variáveis do jogo
tabuleiro = [['' for _ in range(3)] for _ in range(3)]
jogador_atual = 'X'
jogo_ativo = True
vencedor = None
pontuacao_x = 0
pontuacao_o = 0

# Funções do jogo

def desenhar_tabuleiro():
    tela.fill(branco)
    # Desenhar linhas do tabuleiro
    for linha in range(1, 3):
        pygame.draw.line(tela, preto, (0, linha * altura // 3), (largura, linha * altura // 3), 5)
        pygame.draw.line(tela, preto, (linha * largura // 3, 0), (linha * largura // 3, altura), 5)
    
    # Desenhar bordas
    pygame.draw.rect(tela, cor_borda, [0, 0, largura, espessura_borda])  # Topo
    pygame.draw.rect(tela, cor_borda, [0, altura - espessura_borda, largura, espessura_borda])  # Base
    pygame.draw.rect(tela, cor_borda, [0, 0, espessura_borda, altura])  # Esquerda
    pygame.draw.rect(tela, cor_borda, [largura - espessura_borda, 0, espessura_borda, altura])  # Direita

def desenhar_pecas():
    for linha in range(3):
        for coluna in range(3):
            if tabuleiro[linha][coluna] == 'X':
                pygame.draw.line(tela, vermelho, 
                                 (coluna * largura // 3 + 50, linha * altura // 3 + 50), 
                                 (coluna * largura // 3 + largura // 3 - 50, linha * altura // 3 + altura // 3 - 50), 5)
                pygame.draw.line(tela, vermelho, 
                                 (coluna * largura // 3 + largura // 3 - 50, linha * altura // 3 + 50), 
                                 (coluna * largura // 3 + 50, linha * altura // 3 + altura // 3 - 50), 5)
            elif tabuleiro[linha][coluna] == 'O':
                pygame.draw.circle(tela, azul, 
                                   (coluna * largura // 3 + largura // 6, linha * altura // 3 + altura // 6), 
                                   largura // 6 - 50, 5)

def desenhar_pontuacao():
    fonte = pygame.font.SysFont("Helvetica", 17)
    texto_pontuacao = fonte.render(f"Pontuação = X : {pontuacao_x}                 O : {pontuacao_o}", True, preto)
    tela.blit(texto_pontuacao, (6, 1))  # Posiciona a pontuação no canto superior esquerdo

def verificar_vencedor():
    global jogo_ativo, vencedor
    for linha in range(3):
        if tabuleiro[linha][0] == tabuleiro[linha][1] == tabuleiro[linha][2] != '':
            vencedor = tabuleiro[linha][0]
            jogo_ativo = False
    for coluna in range(3):
        if tabuleiro[0][coluna] == tabuleiro[1][coluna] == tabuleiro[2][coluna] != '':
            vencedor = tabuleiro[0][coluna]
            jogo_ativo = False
    if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] != '':
        vencedor = tabuleiro[0][0]
        jogo_ativo = False
    if tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] != '':
        vencedor = tabuleiro[0][2]
        jogo_ativo = False
    if '' not in tabuleiro[0] and '' not in tabuleiro[1] and '' not in tabuleiro[2] and vencedor is None:
        vencedor = 'Empate'
        jogo_ativo = False

def mostrar_tela_vencedor(vencedor):
    global pontuacao_x, pontuacao_o

    # Atualiza a pontuação antes de mostrar a tela do vencedor
    if vencedor == 'X':
        pontuacao_x += 1
    elif vencedor == 'O':
        pontuacao_o += 1

    tela.fill(branco)
    fonte = pygame.font.SysFont("Helvetica", 30)
    texto_vencedor = f"Jogador {vencedor} venceu!" if vencedor != 'Empate' else "Empate!"
    texto = fonte.render(texto_vencedor, True, preto)
    tela.blit(texto, (largura // 2 - texto.get_width() // 2, altura // 2 - texto.get_height() // 2))
    
    fonte_menor = pygame.font.SysFont("Helvetica", 25)
    texto_reiniciar = fonte_menor.render("Clique para reiniciar", True, preto)
    tela.blit(texto_reiniciar, (largura // 2 - texto_reiniciar.get_width() // 2, altura // 2 + 40))

    pygame.display.update()
    
    esperar_entrada()

def esperar_entrada():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                reiniciar_jogo()
                return  # Sair do loop após reiniciar

def reiniciar_jogo():
    global tabuleiro, jogador_atual, jogo_ativo, vencedor
    tabuleiro = [['' for _ in range(3)] for _ in range(3)]
    jogador_atual = 'X'
    jogo_ativo = True
    vencedor = None

def main():
    global jogador_atual

    while True:
        desenhar_tabuleiro()
        desenhar_pecas()
        desenhar_pontuacao()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and jogo_ativo:
                x, y = pygame.mouse.get_pos()
                linha = y // (altura // 3)
                coluna = x // (largura // 3)
                if tabuleiro[linha][coluna] == '':
                    tabuleiro[linha][coluna] = jogador_atual
                    jogador_atual = 'O' if jogador_atual == 'X' else 'X'
                    verificar_vencedor()
                    if not jogo_ativo:
                        mostrar_tela_vencedor(vencedor)

        pygame.display.update()

if __name__ == "__main__":
    main()

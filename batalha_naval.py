import random  # Importa o módulo random para usar funções de aleatoriedade

# Símbolos visuais usados no tabuleiro
AGUA = "🌊"
TIRO_AGUA = "🔫"
ACERTO_NAVIO = "🔥"
NAVIO = "🚢"
NAVIO_AFUNDADO = "💥"

# Dimensões do tabuleiro
TOTAL_LINHAS = 5
TOTAL_COLUNAS = 10

# Tipos de navios e seus respectivos tamanhos
TIPOS_NAVIOS = {
    "Porta-Aviões": 5,
    "Navio-Tanque": 4,
    "Contratorpedeiro": 3,
    "Submarino": 2,
    "Destroier": 1
}

# Cria um tabuleiro vazio (só com água)
def criar_tabuleiro():
    return [[AGUA for _ in range(TOTAL_COLUNAS)] for _ in range(TOTAL_LINHAS)]

# Exibe o tabuleiro na tela com um título
def mostrar_tabuleiro(tabuleiro, titulo):
    print(f"\n--- {titulo.upper()} ---")
    print("   " + " ".join(f"{indice:2}" for indice in range(TOTAL_COLUNAS)))  # Cabeçalho com números das colunas
    for indice_linha, linha in enumerate(tabuleiro):
        print(f"{indice_linha:2} |", end=" ")  # Índice da linha
        print(" ".join(linha))  # Células da linha
    print()

# Permite o jogador posicionar seus navios manualmente
def posicionar_navios_jogador(tabuleiro_jogador, navios_jogador):
    print("⚓ Posicione suas embarcações:")
    for nome_navio, tamanho_navio in TIPOS_NAVIOS.items():  # Para cada navio...
        while True:
            try:
                print(f"\n{nome_navio} ({tamanho_navio} células)")
                linha_inicial = int(input("Linha inicial (0 a 4): "))
                coluna_inicial = int(input("Coluna inicial (0 a 9): "))
                direcao_navio = input("Direção (H para horizontal, V para vertical): ").upper()

                # Validação da direção
                if direcao_navio not in ["H", "V"]:
                    print("⚠️ Direção inválida. Use H ou V.")
                    continue

                # Valida se o navio cabe no tabuleiro
                if direcao_navio == "H" and coluna_inicial + tamanho_navio > TOTAL_COLUNAS:
                    print("⚠️ Número inválido. Tente novamente.")
                    continue
                if direcao_navio == "V" and linha_inicial + tamanho_navio > TOTAL_LINHAS:
                    print("⚠️ Número inválido. Tente novamente.")
                    continue

                # Calcula as posições do navio com base na direção
                posicoes_navio = [(linha_inicial + i if direcao_navio == "V" else linha_inicial,
                                   coluna_inicial + i if direcao_navio == "H" else coluna_inicial)
                                  for i in range(tamanho_navio)]

                # Verifica se todas as posições estão livres (água)
                if all(tabuleiro_jogador[linha][coluna] == AGUA for linha, coluna in posicoes_navio):
                    # Coloca o navio no tabuleiro
                    for linha, coluna in posicoes_navio:
                        tabuleiro_jogador[linha][coluna] = NAVIO
                    # Armazena os dados do navio
                    navios_jogador.append({"nome": nome_navio, "posicoes": posicoes_navio, "afundado": False})
                    mostrar_tabuleiro(tabuleiro_jogador, "Seu tabuleiro atual")
                    break
                else:
                    print("⚠️ Posição ocupada. Tente novamente.")
            except (ValueError, IndexError):
                print("⚠️ Número inválido. Tente novamente.")

# Posiciona os navios do computador aleatoriamente
def posicionar_navios_computador(tabuleiro_computador, navios_computador):
    for nome_navio, tamanho_navio in TIPOS_NAVIOS.items():
        while True:
            direcao_navio = random.choice(["H", "V"])  # Direção aleatória
            max_linha = TOTAL_LINHAS - tamanho_navio if direcao_navio == "V" else TOTAL_LINHAS - 1
            max_coluna = TOTAL_COLUNAS - tamanho_navio if direcao_navio == "H" else TOTAL_COLUNAS - 1
            linha_inicial = random.randint(0, max_linha)
            coluna_inicial = random.randint(0, max_coluna)
            posicoes_navio = [(linha_inicial + i if direcao_navio == "V" else linha_inicial,
                               coluna_inicial + i if direcao_navio == "H" else coluna_inicial)
                              for i in range(tamanho_navio)]
            # Verifica se as posições estão livres
            if all(tabuleiro_computador[linha][coluna] == AGUA for linha, coluna in posicoes_navio):
                for linha, coluna in posicoes_navio:
                    tabuleiro_computador[linha][coluna] = NAVIO
                navios_computador.append({"nome": nome_navio, "posicoes": posicoes_navio, "afundado": False})
                break

# Atualiza o status de navios afundados
def atualizar_navio_afundado(tabuleiro, navios):
    for navio in navios:
        if not navio["afundado"]:
            # Se todas as posições do navio foram atingidas
            if all(tabuleiro[linha][coluna] == ACERTO_NAVIO for linha, coluna in navio["posicoes"]):
                navio["afundado"] = True
                for linha, coluna in navio["posicoes"]:
                    tabuleiro[linha][coluna] = NAVIO_AFUNDADO

# Conta quantos navios ainda não foram afundados
def contar_navios_restantes(navios):
    return sum(1 for navio in navios if not navio["afundado"])

# Turno de ataque do jogador
def turno_ataque_jogador(tabuleiro_inimigo_real, tabuleiro_inimigo_visivel, navios_inimigo):
    print("🎯 Sua vez de atacar!")
    while True:
        try:
            linha_ataque = int(input("Linha (0 a 4): "))
            coluna_ataque = int(input("Coluna (0 a 9): "))
            # Verifica se é uma posição válida e ainda não atacada
            if 0 <= linha_ataque < TOTAL_LINHAS and 0 <= coluna_ataque < TOTAL_COLUNAS and tabuleiro_inimigo_visivel[linha_ataque][coluna_ataque] == AGUA:
                # Se acertou um navio
                if tabuleiro_inimigo_real[linha_ataque][coluna_ataque] == NAVIO:
                    print(f">> 💥 ACERTOU em ({linha_ataque}, {coluna_ataque})!")
                    tabuleiro_inimigo_real[linha_ataque][coluna_ataque] = ACERTO_NAVIO
                    tabuleiro_inimigo_visivel[linha_ataque][coluna_ataque] = ACERTO_NAVIO
                    navios_antes = contar_navios_restantes(navios_inimigo)

                    atualizar_navio_afundado(tabuleiro_inimigo_real, navios_inimigo)

                    # Atualiza o tabuleiro visível com 💥 se afundou
                    for navio in navios_inimigo:
                        if navio["afundado"]:
                            for linha, coluna in navio["posicoes"]:
                                tabuleiro_inimigo_visivel[linha][coluna] = NAVIO_AFUNDADO

                    navios_depois = contar_navios_restantes(navios_inimigo)
                    # Se afundou um navio, jogador joga de novo
                    if navios_depois < navios_antes:
                        print("🚢 Você afundou um navio! Jogue novamente! 🔁")
                        return True
                else:
                    print(f">> 💦 ERROU em ({linha_ataque}, {coluna_ataque}).")
                    tabuleiro_inimigo_visivel[linha_ataque][coluna_ataque] = TIRO_AGUA
                break
            else:
                print("⚠️ Coordenada inválida ou já atacada.")
        except ValueError:
            print("⚠️ Entrada inválida.")
    return False

# Turno de ataque do computador (aleatório)
def turno_ataque_computador(tabuleiro_jogador_real, navios_jogador):
    print("🤖 Computador está atacando...")
    while True:
        linha_ataque = random.randint(0, TOTAL_LINHAS - 1)
        coluna_ataque = random.randint(0, TOTAL_COLUNAS - 1)
        if tabuleiro_jogador_real[linha_ataque][coluna_ataque] in [NAVIO, AGUA]:
            if tabuleiro_jogador_real[linha_ataque][coluna_ataque] == NAVIO:
                print(f">> 💥 Computador ACERTOU em ({linha_ataque}, {coluna_ataque})!")
                tabuleiro_jogador_real[linha_ataque][coluna_ataque] = ACERTO_NAVIO
            else:
                print(f">> 💦 Computador ERROU em ({linha_ataque}, {coluna_ataque}).")
                tabuleiro_jogador_real[linha_ataque][coluna_ataque] = TIRO_AGUA
            atualizar_navio_afundado(tabuleiro_jogador_real, navios_jogador)
            break

# Função principal que roda o jogo
def iniciar_jogo():
    print("\n🌊 BEM-VINDO AO BATALHA NAVAL 🌊")

    # Criação dos tabuleiros
    tabuleiro_jogador_real = criar_tabuleiro()
    tabuleiro_computador_real = criar_tabuleiro()
    tabuleiro_computador_visivel = criar_tabuleiro()

    # Listas para armazenar os navios
    navios_jogador = []
    navios_computador = []

    # Jogador posiciona os navios
    mostrar_tabuleiro(tabuleiro_jogador_real, "Tabuleiro do Jogador")
    posicionar_navios_jogador(tabuleiro_jogador_real, navios_jogador)
    # Computador posiciona os navios
    posicionar_navios_computador(tabuleiro_computador_real, navios_computador)

    print("\n🚢 Embarcações posicionadas. Prepare-se!")

    # Loop principal do jogo
    while True:
        print("\n===== NOVA RODADA =====")
        print(f"🚨 Seus navios restantes: {contar_navios_restantes(navios_jogador)}")
        print(f"🎯 Navios inimigos restantes: {contar_navios_restantes(navios_computador)}")

        mostrar_tabuleiro(tabuleiro_jogador_real, "Seu Tabuleiro (Posições reais e ataques do computador)")
        mostrar_tabuleiro(tabuleiro_computador_visivel, "Tabuleiro para você atacar (Posições visíveis do computador)")

        repetir_turno = True
        while repetir_turno:
            repetir_turno = turno_ataque_jogador(tabuleiro_computador_real, tabuleiro_computador_visivel, navios_computador)
            if contar_navios_restantes(navios_computador) == 0:
                print("\n🏆 PARABÉNS! Você venceu a batalha!")
                print("🎉 Obrigado por jogar Batalha Naval. Até a próxima!")
                return

        turno_ataque_computador(tabuleiro_jogador_real, navios_jogador)
        if contar_navios_restantes(navios_jogador) == 0:
            mostrar_tabuleiro(tabuleiro_jogador_real, "Seu Tabuleiro Final")
            print("\n💀 Você perdeu. O computador venceu.")
            print("🎮 Obrigado por jogar Batalha Naval. Tente novamente e vença na próxima!")
            return

# Executa o jogo se o script for rodado diretamente
if __name__ == "__main__":
    iniciar_jogo()

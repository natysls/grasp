import random
import time


def ler_arquivo(arquivo):
    with open(arquivo, "r", encoding="utf-8-sig") as f:
        lines = f.readlines()

    n_variaveis, n_clausulas = map(int, lines[0].split())
    clauses = [list(map(int, line.split())) for line in lines[1:]]

    return n_variaveis, clauses


def avaliando_solucao(solution, clauses):
    """Avaliar quantas cláusulas são satisfeitas por uma solução (atribuição de valores às variáveis)."""
    satisfatoria = 0
    for clause in clauses:
        for literal in clause:
            var_index = abs(literal) - 1
            if var_index >= len(solution):
                continue
            if (literal > 0 and solution[var_index]) or (
                literal < 0 and not solution[var_index]
            ):
                satisfatoria += 1
                break
    return satisfatoria


def obj(e, pos_occ, neg_occ):
    """
    Para uma variável e, calcula o número de cláusulas em que ela aparece positivamente (pos_occ[e]) e negativamente (neg_occ[e])
    Retorna o máximo entre essas duas contagens, indicando a importância da variável na satisfação das cláusulas.
    """
    return max(len(pos_occ[e]), len(neg_occ[e]))


def greedy_randomized_construction(n_variaveis, clauses, pos_occ, neg_occ, alfa):
    """Fase de Construção: Um novo elemento é inserido na solução corrente, de forma gulosa,
    sendo selecionado de um conjunto restrito de candidatos."""
    S = [None] * n_variaveis
    C = list(range(n_variaveis))  # Conjunto de variáveis candidatos para uma solução
    while C:
        valores_obj = {e: obj(e, pos_occ, neg_occ) for e in C}

        c_min = min(valores_obj.values())
        c_max = max(valores_obj.values())

        # Construir a Lista de Candidatos Restrita (RCL) usando valores_obj já calculado
        limite = c_max - alfa * (c_max - c_min)
        RCL = [e for e in C if valores_obj[e] >= limite]
        if not RCL:
            break  # Evita erro caso RCL fique vazia

        escolhido = random.choice(RCL)

        # Atribuir valor para a variável escolhida
        temp_solution = S.copy()
        temp_solution[escolhido] = True
        valor_true = avaliando_solucao(temp_solution, clauses)

        temp_solution[escolhido] = False
        valor_false = avaliando_solucao(temp_solution, clauses)

        S[escolhido] = (
            valor_true >= valor_false
        )  # Escolhe True se for melhor, senão False

        # Remover a variável escolhida do conjunto de candidatos
        C.remove(escolhido)

    return S


def local_search(solution, clauses, n_variaveis):
    """Melhorar a solução inicial através de uma busca local, explorando a vizinhança da solução atual"""

    melhor_solucao = solution[:]
    melhor_valor = avaliando_solucao(melhor_solucao, clauses)

    improvavel_otimo_lugar = True
    while improvavel_otimo_lugar:
        improvavel_otimo_lugar = False
        for i in range(n_variaveis):
            melhor_solucao[i] = not melhor_solucao[i]  # Troca a variável in-place
            novo_valor = avaliando_solucao(melhor_solucao, clauses)

            if novo_valor > melhor_valor:  # Atualiza
                melhor_valor = novo_valor
                improvavel_otimo_lugar = True
            else:
                melhor_solucao[i] = not melhor_solucao[i]  # Reverte a troca

    return melhor_solucao


def pre_computar_infos(n_variaveis, clauses):
    """Verifica dentro das clausulas ocorrencias negativas e positivas de cada"""
    ocorrencias_positivas = [[] for _ in range(n_variaveis)]
    ocorrencias_negativas = [[] for _ in range(n_variaveis)]

    # Percorre cada cláusula e seus literais
    for clause_index, clause in enumerate(clauses):
        for literal in clause:
            var_index = abs(literal) - 1  # converte para índice (0-indexado)
            if literal > 0:
                ocorrencias_positivas[var_index].append(clause_index)
            else:
                ocorrencias_negativas[var_index].append(clause_index)

    return ocorrencias_positivas, ocorrencias_negativas


def grasp_max_3sat(n_variaveis, clauses, pos_occ, neg_occ, max_iter, alfa):
    melhor_solucao = None
    melhor_valor = 0
    cont = 0

    for _ in range(max_iter):
        solution = greedy_randomized_construction(
            n_variaveis, clauses, pos_occ, neg_occ, alfa
        )
        primeira_solucao = avaliando_solucao(solution, clauses)
        if cont == 0:
            print(f"Solução Inicial {primeira_solucao}")
        solution = local_search(solution, clauses, n_variaveis)
        solution_valor = avaliando_solucao(solution, clauses)

        if solution_valor > melhor_valor:
            melhor_solucao = solution
            melhor_valor = solution_valor
        cont += 1

    return melhor_solucao, melhor_valor


def main():
    arquivos = ["SAT1.txt", "SAT2.txt", "SAT3.txt"]
    iter = [25, 50, 75, 100]
    alfa = [0.3, 0.4, 0.5, 0.7]
    for arquivo in arquivos:
        print("=======================================================================")
        print(f"Iniciando {arquivo}")
        for i in range(4):
            for j in range(4):

                inicio_contador = time.time()

                n_variaveis, clauses = ler_arquivo(arquivo=arquivo)

                oco_pos, oco_neg = pre_computar_infos(n_variaveis, clauses)
                melhor_solucao, melhor_valor = grasp_max_3sat(
                    n_variaveis,
                    clauses,
                    oco_pos,
                    oco_neg,
                    max_iter=iter[i],
                    alfa=alfa[j],
                )

                fim_contador = time.time()
                tempo_total = fim_contador - inicio_contador
                print(
                    f"Usando {iter[i]} iterações e um alfa igual a {alfa[j]}, melhor solução encontrada satisfaz {melhor_valor} cláusulas. Tempo \t{tempo_total:.4f}S"
                )
        print("=======================================================================")


if __name__ == "__main__":
    main()

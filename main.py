import random
import time


def ler_arquivo(arquivo):
    """Lê o arquivo contendo o problema 3-SAT e extrai as variáveis e cláusulas."""
    with open(arquivo, "r", encoding="utf-8-sig") as f:
        lines = f.readlines()

    # Lê a primeira linha contendo o número de variáveis e cláusulas
    n_variaveis, n_clausulas = map(int, lines[0].split())
    # Lê as cláusulas a partir da segunda linha
    clauses = [list(map(int, line.split())) for line in lines[1:]]

    return n_variaveis, clauses


def avaliando_solucao(solution, clauses):
    """Avalia quantas cláusulas são satisfeitas por uma solução (atribuição de valores às variáveis)."""
    satisfatoria = 0
    for clause in clauses:
        for literal in clause:
            var_index = abs(literal) - 1
            if var_index >= len(solution):
                continue
            # Se o literal é positivo e verdadeiro ou se é negativo e falso, a cláusula é satisfeita
            if (literal > 0 and solution[var_index]) or (
                literal < 0 and not solution[var_index]
            ):
                satisfatoria += 1
                break
    return satisfatoria


def obj(e, pos_occ, neg_occ):
    """Calcula a importância de uma variável na satisfação das cláusulas."""
    return max(len(pos_occ[e]), len(neg_occ[e]))


def greedy_randomized_construction(n_variaveis, clauses, pos_occ, neg_occ, alfa):
    """Fase de construção da solução inicial utilizando uma abordagem gulosa e aleatória."""
    S = [None] * n_variaveis  # Solução inicial
    C = list(range(n_variaveis))  # Conjunto de variáveis candidatos
    while C:
        valores_obj = {e: obj(e, pos_occ, neg_occ) for e in C}
        c_min = min(valores_obj.values())
        c_max = max(valores_obj.values())

        # Definição do limite para restrição da lista de candidatos (RCL)
        limite = c_max - alfa * (c_max - c_min)
        RCL = [e for e in C if valores_obj[e] >= limite]
        if not RCL:
            break

        escolhido = random.choice(RCL)

        # Avaliação da escolha do valor booleano para a variável selecionada
        temp_solution = S.copy()
        temp_solution[escolhido] = True
        valor_true = avaliando_solucao(temp_solution, clauses)

        temp_solution[escolhido] = False
        valor_false = avaliando_solucao(temp_solution, clauses)

        # Atribui True se for melhor, caso contrário False
        S[escolhido] = valor_true >= valor_false

        C.remove(escolhido)  # Remove a variável escolhida do conjunto de candidatos

    return S


def local_search(solution, clauses, n_variaveis):
    """Melhora a solução inicial por meio de busca local."""
    melhor_solucao = solution[:]
    melhor_valor = avaliando_solucao(melhor_solucao, clauses)
    improvavel_otimo_lugar = True

    while improvavel_otimo_lugar:
        improvavel_otimo_lugar = False
        for i in range(n_variaveis):
            melhor_solucao[i] = not melhor_solucao[i]  # Inverte o valor
            novo_valor = avaliando_solucao(melhor_solucao, clauses)

            if novo_valor > melhor_valor:
                melhor_valor = novo_valor
                improvavel_otimo_lugar = True
            else:
                melhor_solucao[i] = not melhor_solucao[i]  # Reverte a troca

    return melhor_solucao


def pre_computar_infos(n_variaveis, clauses):
    """Pré-processa as ocorrências positivas e negativas de cada variável nas cláusulas."""
    ocorrencias_positivas = [[] for _ in range(n_variaveis)]
    ocorrencias_negativas = [[] for _ in range(n_variaveis)]

    for clause_index, clause in enumerate(clauses):
        for literal in clause:
            var_index = abs(literal) - 1  # Índice baseado em zero
            if literal > 0:
                ocorrencias_positivas[var_index].append(clause_index)
            else:
                ocorrencias_negativas[var_index].append(clause_index)

    return ocorrencias_positivas, ocorrencias_negativas


def grasp_max_3sat(n_variaveis, clauses, pos_occ, neg_occ, max_iter, alfa):
    """Executa a meta-heurística GRASP para resolver o problema 3-SAT."""
    melhor_solucao = None
    melhor_valor = 0
    cont = 0

    for _ in range(max_iter):
        solution = greedy_randomized_construction(
            n_variaveis, clauses, pos_occ, neg_occ, alfa
        )
        primeira_solucao = avaliando_solucao(solution, clauses)
        if cont == 0:
            print(f"Solução Inicial satisfaz {primeira_solucao} cláusulas")

        solution = local_search(solution, clauses, n_variaveis)
        solution_valor = avaliando_solucao(solution, clauses)

        if solution_valor > melhor_valor:
            melhor_solucao = solution
            melhor_valor = solution_valor
        cont += 1

    return melhor_solucao, melhor_valor


def main():
    """Executa o algoritmo para diferentes arquivos de entrada e configurações."""
    arquivos = ["SAT1.txt", "SAT2.txt", "SAT3.txt"]
    iter = [25, 50, 75, 100]
    alfa = [0.3, 0.4, 0.5, 0.7]

    for arquivo in arquivos:
        print("=======================================================================")
        print(f"Iniciando {arquivo}")

        for i in range(4):
            for j in range(4):
                inicio_contador = time.time()

                n_variaveis, clauses = ler_arquivo(arquivo)
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
                    f"Usando {iter[i]} iterações e um alfa igual a {alfa[j]}, melhor solução encontrada satisfaz {melhor_valor} cláusulas. Tempo {tempo_total:.4f}S\n"
                )
        print("=======================================================================")


if __name__ == "__main__":
    main()

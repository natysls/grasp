import random

def ler_arquivo(arquivo):
    with open(arquivo, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
    
    n_variaveis, n_clausulas = map(int, lines[0].split())
    clauses = [list(map(int, line.split())) for line in lines[1:]]
    
    return n_variaveis, clauses

def avaliando_solucao(solution, clauses, n_variantes):
    """ Avalia a solução contando quantas cláusulas são satisfeitas. """
    satisfatoria = 0  # Contador de cláusulas satisfeitas

    # Garante que solution tem tamanho n_variantes (se for menor, preenche com False)
    if len(solution) < n_variantes:
        solution = solution[:] + [False] * (n_variantes - len(solution))

    for clause in clauses:
        clause_satisfatoria = False  # Flag para verificar se a cláusula foi satisfeita
        for literal in clause:
            var_index = abs(literal) - 1  # Convertendo para índice da lista (começa do 0)
            valor_esperado = (literal > 0) 
            valor_atual = solution[var_index]
            
            print(f"Verificando literal {literal}: esperado={valor_esperado}, atual={valor_atual}")
            
            if valor_atual == valor_esperado:
                clause_satisfatoria = True
                break  # Sai do loop, pois a cláusula já foi satisfeita
        
        if clause_satisfatoria:
            satisfatoria += 1

    return satisfatoria  # Retorna o total de cláusulas satisfeitas

def positivos_e_negativos(e, clauses):
    """ Estima a influência da variável e contando quantas vezes aparece positiva/negativa. """
    # Estimativa com alto desempenho, mas imprecisa e superficial
    count_pos = sum(1 for clause in clauses if (e + 1) in clause)
    count_neg = sum(1 for clause in clauses if -(e + 1) in clause)

    return max(count_pos, count_neg)

def obj(solution, clauses):
    """ A função objetiva escolhida vai determinar a melhor eficiencia do algoritmo
    Retorna a pontuação da solução (quantidade de cláusulas satisfeitas). """
    return positivos_e_negativos(solution, clauses)

def greedy_randomized_construction(n_variaveis, clauses, alfa):
    """ Fase de Construção: Um novo elemento é inserido na solução corrente, de forma gulosa, 
        sendo selecionado de um conjunto restrito de candidatos. """
    S = [None] * n_variaveis 
    C = list(range(n_variaveis))  # Conjunto de variáveis candidatos para uma solução
    while C:  
        valores_obj = {e: obj(e, clauses) for e in C}

        c_min = min(valores_obj.values())
        c_max = max(valores_obj.values())

        # Construir a Lista de Candidatos Restrita (RCL) usando valores_obj já calculado
        limite = c_max - alfa * (c_max - c_min)
        RCL = [e for e in C if valores_obj[e] >= limite]
        if not RCL:
            break  # Evita erro caso RCL fique vazia

        escolhido = random.choice(RCL)

        # Atribuir valor para a variável escolhida
        valor_true = avaliando_solucao(S[:escolhido] + [True] + S[escolhido+1:], clauses, n_variaveis)
        valor_false = avaliando_solucao(S[:escolhido] + [False] + S[escolhido+1:], clauses, n_variaveis)

        S[escolhido] = valor_true >= valor_false  # Escolhe True se for melhor, senão False

        # Remover a variável escolhida do conjunto de candidatos
        C.remove(escolhido)

    return S

def local_search(solution, clauses, n_variaveis):
    """ Fase de Busca Local: Passada a fase anterior, é realizada uma busca local partindo 
        da vizinhança da solução corrente, até que seja encontrado um ótimo local. 
        Realiza busca local trocando valores de variáveis para melhorar a solução. """
    melhor_solucao = solution[:]
    melhor_valor = avaliando_solucao(melhor_solucao, clauses, n_variaveis)
    
    improvavel_otimo_lugar = True
    while improvavel_otimo_lugar:
        improvavel_otimo_lugar = False
        for i in range(n_variaveis):
            new_solution = melhor_solucao[:]
            new_solution[i] = not new_solution[i]  # Troca a variável
            novo_valor = avaliando_solucao(new_solution, clauses, n_variaveis)
            
            if novo_valor > melhor_valor:  # Atualiza
                melhor_solucao = new_solution[:]
                melhor_valor = novo_valor
                improvavel_otimo_lugar = True
    
    return melhor_solucao

def grasp_max_3sat(arquivo, max_iter, alfa):
    n_variaveis, clauses = ler_arquivo(arquivo)
    melhor_solucao = None
    melhor_valor = 0
    
    for _ in range(max_iter):
        solution = greedy_randomized_construction(n_variaveis, clauses, alfa)
        solution = local_search(solution, clauses, n_variaveis)
        solution_valor = avaliando_solucao(solution, clauses, n_variaveis)
        
        if solution_valor > melhor_valor:
            melhor_solucao = solution
            melhor_valor = solution_valor
    
    return melhor_solucao, melhor_valor

def main():
    arquivo = 'SAT1.txt'
    best_solution, best_value = grasp_max_3sat(arquivo, max_iter=50, alfa=0.3)
    print(f'Melhor solução encontrada satisfaz {best_value} cláusulas.')

if __name__ == '__main__':
    main()

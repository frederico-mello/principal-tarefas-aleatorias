import secrets
from calendar import monthrange
from datetime import datetime, time

import mercado
from app.database import db

agora = datetime.now()

# Importar o módulo de banco de dados


VALE_ALIMENTACAO = 1500

novoSorteado = []
listaUnesp = []

# Global set to track shown activities
shown_activities = set()


def horario(argumento):
    data_atual = datetime.now()
    horario_map = {
        "dia_do_mes": lambda: data_atual.day,
        "dia_da_semana": lambda: data_atual.weekday(),
        "dias_mes": lambda: monthrange(data_atual.year, data_atual.month)[1],
        "hora": lambda: data_atual.hour,
    }
    return horario_map.get(argumento, lambda: None)()


def saldo_vale_alimentacao(saldo):
    print("\n")

    dia_atual = horario("dia_do_mes")

    saldo = float(saldo)

    if dia_atual is not None:
        restante_projetado = int(VALE_ALIMENTACAO - (VALE_ALIMENTACAO / 30) * dia_atual)
        saldo_final = int(
            saldo - (VALE_ALIMENTACAO - (VALE_ALIMENTACAO / 30) * dia_atual)
        )

    print(
        "\n"
        + "O valor restante projetado seria R$"
        + str(restante_projetado)
        + ". O saldo remanescente é de R$ "
        + str(saldo_final)
    )
    print("\n")

    return saldo_final


def aleatorio(lista):
    return secrets.choice(lista)


def gerar_amigos():
    import amigos

    novoSorteado = []
    novoSorteado = aleatorio(amigos.Amigos.amigos_locais)
    print(novoSorteado)


def gerarAriane():
    novoSorteado = db.get_random_activity("ariane")
    print(novoSorteado)
    if novoSorteado == "Assistir a um filme em casa":
        print(gerar_multimidia())
    if novoSorteado == "Comprar um presente":
        print(gerarCompras())


def gerar_musica():
    """Gera uma música aleatória do banco de dados."""
    musica = db.get_random_activity("multimidia")
    return musica if musica else "Nenhuma música encontrada no banco de dados."


def gerarCasa(tempo_disponivel):
    # Carregar atividades do banco de dados
    atividades_casa = db.get_all_items("atividades_casa")
    # Excluir exercícios físicos entre 7h e 17h
    hora_atual = horario("hora")
    if hora_atual is not None and 7 <= hora_atual < 17:
        atividades_casa.pop("Praticar exercícios físicos", None)

    # Obter os últimos 10 itens sorteados para evitar repetição
    historico_recente = db.obter_historico_sorteios(2)

    # Lógica de seleção de atividades revisada para evitar repetições

    # 1. Filtra todas as atividades que se encaixam no tempo disponível
    atividades_base = [
        atividade
        for atividade, tempo in atividades_casa.items()
        if int(tempo_disponivel) >= int(tempo)
    ]

    # Se for entre 6h e 16h, adiciona atividades do dia
    hora_atual = horario("hora")
    if 6 <= hora_atual < 16:
        atividades_dia = db.get_all_items("atividades_casa_dia")
        for atividade, tempo in atividades_dia.items():
            if int(tempo_disponivel) >= int(tempo) and atividade not in atividades_base:
                atividades_base.append(atividade)

    if not atividades_base:
        return "Nenhuma atividade disponível para o tempo informado."

    # 2. Tenta encontrar uma atividade que não esteja na sessão atual NEM no histórico recente
    atividades_viaveis = [
        atv
        for atv in atividades_base
        if atv not in shown_activities and atv not in itens_recentes
    ]

    # 3. Se não encontrar, limpa o histórico da sessão e tenta novamente, ainda evitando o histórico recente
    if not atividades_viaveis:
        shown_activities.clear()
        atividades_viaveis = [
            atv for atv in atividades_base if atv not in itens_recentes
        ]

    # 4. Se ainda assim não houver opções, significa que todas as atividades possíveis são recentes.
    if not atividades_viaveis:
        return (
            "Nenhuma nova atividade disponível. Tente com um tempo maior ou mais tarde."
        )

    # Sortear uma atividade
    atividade_escolhida = aleatorio(atividades_viaveis)

    # Adicionar a atividade escolhida ao conjunto de mostradas
    shown_activities.add(atividade_escolhida)

    # Tratar atividades especiais
    if atividade_escolhida == "Jogos eletrônicos":
        jogos_casa_dia_semana = db.get_all_activities("jogos_casa_dia_semana")
        nintendo_switch = db.get_all_activities("nintendo_switch")
        android = db.get_all_activities("android")

        db.registrar_item_sorteado(atividade_escolhida, "casa")

        consoles = ("PC", "Nintendo Switch", "Android")
        console_sorteado = aleatorio(consoles)

        def sortear_jogo(lista_jogos):
            # Se for uma lista de listas, achata para uma única lista
            if lista_jogos and isinstance(lista_jogos[0], list):
                lista_achatada = [jogo for sublista in lista_jogos for jogo in sublista]
                lista_jogos = lista_achatada

            opcoes = [j for j in lista_jogos if j not in itens_recentes]
            if not opcoes:
                opcoes = lista_jogos
            if not opcoes:
                return None
            jogo_sorteado = aleatorio(opcoes)
            return jogo_sorteado

        if console_sorteado == "PC":
            jogo = None
            # Combinar as listas de jogos
            jogo = sortear_jogo(jogos_casa_dia_semana)

            if not jogo:
                return "Nenhum jogo disponível para sortear."
            return f"Jogar no PC: {jogo}"

        elif console_sorteado == "Nintendo Switch" and nintendo_switch:
            jogo_switch = sortear_jogo(nintendo_switch)
            if jogo_switch:
                return f"Jogar no Nintendo Switch: {jogo_switch}"
        elif console_sorteado == "Android":
            jogo_android = sortear_jogo(android)
            if jogo_android:
                return f"Jogar no Android: {jogo_android}"

    elif atividade_escolhida == "Jogar no celular":
        jogo_escolhido = db.get_random_activity("ios")
        jogo = "Jogar no celular: " + (jogo_escolhido or "(nenhum jogo encontrado)")

        db.registrar_item_sorteado(jogo, "ios")
        return jogo

    # Registrar a atividade no banco de dados
    db.registrar_item_sorteado(atividade_escolhida, "casa")

    # Tratamento para outras atividades especiais
    if atividade_escolhida == "Ouvir música":
        musica = "Ouvir música da playlist: " + gerar_musica()
        return musica

    elif atividade_escolhida == "Entretenimento":
        try:
            valor_input = (
                input("Quanto você quer gastar? R$ ").strip().replace(",", ".")
            )
            if not valor_input.replace(".", "", 1).isdigit():
                return "Valor inválido. Por favor, insira um número válido."

            valor_maximo = float(valor_input)
            entretenimento = db.get_random_item("entretenimento_centro", valor_maximo)

            if not entretenimento:
                return "Nenhuma atividade de entretenimento encontrada dentro do orçamento informado."

            nome_atividade, valor = entretenimento
            db.registrar_item_sorteado(nome_atividade, "entretenimento")
            valor_formatado = f"R$ {float(valor):.2f}".replace(".", ",")

            if nome_atividade == "Assistir filme":
                tipo_filme = db.get_random_activity("series_e_filmes")

            return f"Atividade de entretenimento: {nome_atividade} - {tipo_filme} (Valor: {valor_formatado})"

        except Exception as e:
            print(f"Erro: {e}")
            return "Ocorreu um erro ao processar sua solicitação. Tente novamente."

    elif atividade_escolhida == "Praticar exercícios físicos":
        exercicio = gerarExercicios()
        db.registrar_item_sorteado(exercicio, "exercicios")
        return exercicio

    # Retorno padrão para atividades sem tratamento especial
    return atividade_escolhida


def gerarComida(valor_maximo=None):
    if not novoSorteado:
        if valor_maximo is not None:
            item, valor = db.get_random_item("almoco", valor_maximo)
        else:
            item, valor = db.get_random_item("almoco")
        print(f"\nVocê pode comer: {item} (R$ {valor:.2f})")
        db.registrar_item_sorteado(item, "almoco")
        novoSorteado.append(item)
    else:
        print(f"\nVocê já escolheu: {novoSorteado[0]}")


def gerarEntretenimento():
    if novoSorteado:
        message = f"Você já escolheu: {novoSorteado[0]}"
        print(f"\n{message}")
        return message

    try:
        valor_input = input("Quanto você quer gastar? R$ ").strip().replace(",", ".")
        if not valor_input.replace(".", "", 1).isdigit():
            return "Valor inválido. Por favor, insira um número válido."
        valor_maximo = float(valor_input)

        result = db.get_random_item("entretenimento_centro", valor_maximo)
        if not result:
            return "Nenhuma atividade de entretenimento encontrada dentro do orçamento informado."

        item, valor = result
        db.registrar_item_sorteado(item, "entretenimento")
        valor_formatado = f"R$ {valor:.2f}".replace(".", ",")

        message = f"Você pode se entreter com: {item} (Valor: {valor_formatado})"
        print(f"\n{message}")
        novoSorteado.append(item)
        return message

    except Exception as e:
        print(f"Erro: {e}")
        return "Ocorreu um erro ao processar sua solicitação. Tente novamente."


def gerarCompras():
    novoSorteado = []
    novoSorteado = aleatorio(db.get_all_activities("itens_compra"))
    print(novoSorteado)
    if novoSorteado == "Item pessoal":
        print(aleatorio(db.get_all_activities("canais_compra")))
    elif novoSorteado == "Presente":
        pessoa_sorteada = aleatorio(["Aparecida Mara", "Ariane", "Gabriel", "Júlio"])
        print(pessoa_sorteada)

        if pessoa_sorteada == "Ariane" or pessoa_sorteada == "Aparecida Mara":
            print(aleatorio(db.get_all_activities("canais_compra")))
        elif pessoa_sorteada == "Gabriel":
            print(aleatorio(db.get_all_activities("canais_gabriel")))
        elif pessoa_sorteada == "Júlio":
            print(aleatorio(db.get_all_activities("canais_julio")))

    if novoSorteado == "Bebida alcoólica":
        print(aleatorio(db.get_all_activities("bebidas_alcoolicas")))
    if novoSorteado == "Viagem":
        print(aleatorio(db.get_all_items("viagens")))


def gerarRefeicao():
    if not novoSorteado:
        itens_refeicao = db.get_all_items("refeicao")
        if not itens_refeicao:
            print("\nNenhum item de refeição encontrado no banco de dados.")
            return "Erro: Nenhum item de refeição cadastrado."
        item = secrets.choice(list(itens_refeicao.keys()))
        print(f"\nVocê pode comer: {item}")
        db.registrar_item_sorteado(item, "refeicao")
        novoSorteado.append(item)
        return item
    else:
        print(f"\nVocê já escolheu: {novoSorteado[0]}")
        return novoSorteado[0]


def gerarTarefasUnesp():

    # Obter os últimos 10 itens sorteados para evitar repetição
    historico_recente = db.obter_historico_sorteios(10)

    # Carregar e combinar as listas de atividades
    listaUnesp = []
    listaUnesp.extend(db.get_all_activities("diversao_unesp"))
    listaUnesp.extend(db.get_all_activities("tarefasUnesp"))

    # 1. Tenta encontrar uma atividade não recente e não mostrada na sessão
    atividades_viaveis = [
        atv
        for atv in listaUnesp
        if atv not in shown_activities and atv not in itens_recentes
    ]

    # 2. Se não encontrar, tenta uma não mostrada na sessão (ignorando o histórico recente)
    if not atividades_viaveis:
        atividades_viaveis = [atv for atv in listaUnesp if atv not in shown_activities]

    # 3. Se ainda não encontrar, limpa o histórico da sessão e pega qualquer uma
    if not atividades_viaveis:
        shown_activities.clear()
        atividades_viaveis = listaUnesp

    if not atividades_viaveis:
        return "Nenhuma tarefa disponível"

    # Sortear uma atividade
    atividade_escolhida = aleatorio(atividades_viaveis)

    # Tratar casos especiais
    if atividade_escolhida == "Estudos":
        tarefa_final = gerar_estudos()  # Gera a tarefa de estudo específica
        shown_activities.add(tarefa_final)
        db.registrar_item_sorteado(
            tarefa_final, "estudos"
        )  # Registra a tarefa específica no histórico
        return tarefa_final
    elif atividade_escolhida == "Atualizar a planilha Mercado":
        tarefa_final = db.get_random_activity("planilha_mercado")
        shown_activities.add(atividade_escolhida)
        db.registrar_item_sorteado(atividade_escolhida, "planilha_mercado")
        return tarefa_final
    elif atividade_escolhida == "Contribuir com o Family Search":
        tarefa_final = db.get_random_activity("family_search")
        shown_activities.add(atividade_escolhida)
        db.registrar_item_sorteado(atividade_escolhida, "family_search")
        return tarefa_final
    elif atividade_escolhida == "Jogar no celular":
        jogo = db.get_random_activity("android")
        if jogo:
            tarefa_final = f"Jogar no celular: {jogo}"
            db.registrar_item_sorteado(tarefa_final, "android")
            return tarefa_final
        else:
            return "Jogar no celular: (nenhum jogo encontrado)"
    elif atividade_escolhida == "Interagir nas redes sociais":
        redes_sociais = db.get_all_activities("redes_sociais_unesp")
        if redes_sociais:
            rede_escolhida = secrets.choice(redes_sociais)
            tarefa_final = f"{atividade_escolhida}: {rede_escolhida}"
            shown_activities.add(tarefa_final)
            return tarefa_final
    elif atividade_escolhida == "Estudar sobre o mercado financeiro":
        topicos_financeiros = db.get_all_activities("financas")
        if topicos_financeiros:
            topico_escolhido = secrets.choice(topicos_financeiros)
            shown_activities.add(topico_escolhido)
            db.registrar_item_sorteado(topico_escolhido, "financas")
            return topico_escolhido
    elif atividade_escolhida == "Atualizar playlist de música":
        itens_multimidia = db.get_all_activities("multimidia")
        if itens_multimidia:
            item_escolhido = secrets.choice(itens_multimidia)
            tarefa_final = f"{atividade_escolhida}: {item_escolhido}"
            shown_activities.add(tarefa_final)
            db.registrar_item_sorteado(atividade_escolhida, "multimidia")
            return tarefa_final

    # Para todas as outras tarefas, registrar normalmente
    shown_activities.add(atividade_escolhida)
    db.registrar_item_sorteado(atividade_escolhida, "tarefas_unesp")

    if atividade_escolhida == "Jogar no Android":
        jogo_android = db.get_random_activity("android")
        return jogo_android if jogo_android else "Jogar no Android"
    elif atividade_escolhida == "Jogar no PC":
        return "Jogar paciência no YouTube Games"

    return atividade_escolhida


def gerar_babbel():
    return db.get_random_activity("babbel")


def gerar_duolingo():
    return db.get_random_activity("duolingo")


def gerar_estudos():
    """
    Gera uma atividade de estudo aleatória (exceto finanças) e não a registra no banco de dados.

    De segunda a sexta, das 8h às 17h, busca no banco 'estudos_unesp'.
    Nos outros horários, busca no banco 'estudos_casa'.
    """
    # Verificar se está no horário comercial (8h-17h) de segunda a sexta
    horario_comercial = time(8, 0) <= agora.time() <= time(17, 0)
    dia_util = agora.weekday() < 5  # 0-4 = segunda a sexta

    # Escolher o banco de dados com base no horário
    tabela = "estudos_unesp" if (horario_comercial and dia_util) else "estudos_casa"

    # Obter todos os estudos disponíveis da tabela apropriada
    estudos_disponiveis = db.get_all_activities(tabela)

    # Obter histórico recente
    historico_recente = db.obter_historico_sorteios(20)

    # Garantir que "Estudar sobre o mercado financeiro" não seja tratado aqui
    estudos_disponiveis = [
        e for e in estudos_disponiveis if e != "Estudar sobre o mercado financeiro"
    ]

    if not estudos_disponiveis:
        return (
            f"Nenhuma atividade de estudo disponível no momento na tabela '{tabela}'."
        )

    # Tentar encontrar um estudo que não esteja no histórico recente
    estudos_nao_recentes = [e for e in estudos_disponiveis if e not in itens_recentes]

    # Escolher um estudo
    estudo_sorteado = (
        secrets.choice(estudos_nao_recentes)
        if estudos_nao_recentes
        else secrets.choice(estudos_disponiveis)
    )

    # Lógica para outros tipos de estudos
    if estudo_sorteado == "Estudar no Babbel":
        return gerar_babbel()
    elif estudo_sorteado == "Estudar no Duolingo":
        return gerar_duolingo()

    return estudo_sorteado


def gerarExercicios():
    # Não permitir sorteio de exercícios entre 7h e 17h
    hora_atual = horario("hora")
    if hora_atual is not None and 7 <= hora_atual < 17:
        return "Exercícios físicos não são sugeridos entre 7h e 17h."

    # Obter histórico recente de exercícios
    historico_recente = db.obter_historico_sorteios(10)

    exercicio_fisico = db.get_random_activity("exercicios_fisicos")

    if exercicio_fisico == "Fazer um exercício avulso no Ring Fit Adventure":
        return f"{db.get_random_activity('ring_fit')} | {exercicio_fisico}"
    else:
        return exercicio_fisico


def gerar_modais(carro=False):
    modais = db.get_all_activities("modais")
    if carro == True and "Locomover-se de carro" not in modais:
        modais.append("Locomover-se de carro")
    elif carro == False and "Locomover-se de carro" in modais:
        modais.remove("Locomover-se de carro")

    # def sem_onibus (elemento):
    #     return elemento != "Locomover-se de ônibus"

    def sem_bike(elemento):
        return elemento != "Locomover-se de bicicleta"

    def sem_carro(elemento):
        return elemento != "Locomover-se de carro"

    modal_ida = aleatorio(modais)

    # lista_modais_volta_sem_onibus = list(filter(sem_onibus, modais))

    if modal_ida == "Locomover-se de bicicleta":
        modal_volta = modal_ida
    elif modal_ida == "Locomover-se de carro":
        modal_volta = modal_ida
    else:
        lista_modais_volta_sem_bike = list(filter(sem_bike, modais))
        lista_modais_volta_sem_bike_e_carro = list(
            filter(sem_carro, lista_modais_volta_sem_bike)
        )
        modal_volta = aleatorio(lista_modais_volta_sem_bike_e_carro)
    return "Ida: " + modal_ida + " | " + "Volta: " + modal_volta


def gerar_multimidia():
    multimidia = db.get_random_activity("series_e_filmes")
    tv = db.get_random_activity("tv")
    return f"{tv}\n{multimidia}"


def gerar_redes_sociais():
    dia_semana_atual = horario("dia_da_semana")
    hora_atual = horario("hora")

    if dia_semana_atual == 5 or dia_semana_atual == 6:  # Fim de semana
        redes = db.get_all_activities("redes_sociais_casa") + db.get_all_activities(
            "redes_sociais_unesp"
        )
    elif hora_atual < 8 or hora_atual > 17:  # Fora do horário da UNESP
        redes = db.get_all_activities("redes_sociais_casa")
    else:  # Horário da UNESP
        redes = db.get_all_activities("redes_sociais_unesp")

    return secrets.choice(redes) if redes else "Nenhuma rede social disponível"


def ver_historico():
    """Exibe o histórico de itens sorteados"""
    print("\n=== HISTÓRICO DE SORTEIOS ===")
    historico = db.obter_historico_sorteios(10)  # Últimos 10 itens

    if not historico:
        print("Nenhum item sorteado ainda.")
        return

    for item in historico:
        print(f"{item[2]} - {item[1]}: {item[0]}")
    print("")


respostas = [
    "amigos",
    # "aposta",
    "ariane",
    "babbel",
    "casa",
    "comida",
    "duolingo",
    "estudos",
    "unesp",
    "entretenimento",
    "lanche",
    "lanches",
    "mercado",
    "modal",
    "multimidia",
    "ofertas",
    "compras",
    "saldo",
    "redes",
    "refeicao",
    "historico",
]

sorteadoAnterior = "Esta fera"
resposta = "casa"

while resposta in respostas:
    data_atual = datetime.now()
    resposta = input("Qual tipo de afazer você deseja?")

    # if resposta == "dinamica":
    #     gerarDinamica()

    if resposta == "unesp":
        # Primeiro, obtemos o sorteado uma única vez
        sorteado = gerarTarefasUnesp()
        print("\n\n")

        # Verificamos se é o mesmo do anterior
        if sorteadoAnterior == sorteado:
            sorteado = gerarTarefasUnesp()
            print("\n")

        # Exibição do resultado
        print("\n")
        print(sorteado)
        sorteadoAnterior = sorteado
        print("\n")
        listaUnesp = []
        novoSorteado = []

    elif resposta == "casa":
        tempo_disponivel = input("Qual o tempo disponível?")
        sorteado = gerarCasa(tempo_disponivel)
        print(sorteado)
        sorteadoAnterior = sorteado
        print("\n")

    elif resposta == "exercicios":
        print(gerarExercicios())
        print("\n")
        novoSorteado = []
    elif resposta == "entretenimento":
        entretenimento = gerarEntretenimento()
        print("\n")
        print(entretenimento)
        novoSorteado = []
    elif resposta == "amigos":
        gerar_amigos()
        print("\n")
        novoSorteado = []
    # elif resposta == "aposta":
    #     saldo = input("Qual o saldo disponível?" + "\n")
    #     gerar_aposta(saldo)
    #     print("\n")
    elif resposta == "refeicao":
        print(gerarRefeicao())
        print("\n")
        novoSorteado = []
    elif resposta == "comida":
        gerarComida()
        print("\n")
        novoSorteado = []
    elif resposta == "mercado":
        mercado.gerarMercado("normal")
        print("\n")
        novoSorteado = []
    elif resposta == "lanche" or resposta == "lanches":
        mercado.gerarMercado("lanche")
        print("\n")
        novoSorteado = []
    elif resposta == "ofertas":
        mercado.gerarMercado("ofertas")
        print("\n")
        novoSorteado = []
    elif resposta == "compras":
        gerarCompras()
        print("\n")
        novoSorteado = []
    elif resposta == "ariane":
        gerarAriane()
        print("\n")
        novoSorteado = []
    elif resposta == "saldo":
        saldo = input("Qual é o saldo restante disponível?")
        saldo = float(saldo)
        saldo_vale_alimentacao(saldo)
    elif resposta == "redes":
        print(gerar_redes_sociais())
        print("\n")
        novoSorteado = []
    elif resposta == "estudos":
        print(gerar_estudos())
        print("\n")
        novoSorteado = []
    elif resposta == "modal":
        print(gerar_modais())
        print("\n")
        novoSorteado = []
    elif resposta == "multimidia":
        print(gerar_multimidia())
        print("\n")
        novoSorteado = []
    elif resposta == "babbel":
        print(gerar_babbel())
        print("\n")
        novoSorteado = []
    elif resposta == "duolingo":
        print(gerar_duolingo())
        print("\n")
        novoSorteado = []
    elif resposta == "historico":
        ver_historico()
        resposta = ""
        continue
    else:
        break

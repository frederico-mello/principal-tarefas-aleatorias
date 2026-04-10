import random
from datetime import datetime

from flask import Blueprint, jsonify, render_template, request

from app import db

bp = Blueprint("main", __name__)

# Dicionário para armazenar atividades mostradas na sessão atual
shown_activities = set()


def aleatorio(lista):
    """Função auxiliar para sortear um item aleatório de uma lista"""
    if not lista:
        return None
    return random.choice(lista)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/casa", methods=["GET"])
def get_atividade_casa():
    try:
        # Obter parâmetro de tempo disponível, padrão é 60 minutos
        tempo_disponivel = request.args.get("tempo", default=60, type=int)
        filtrar_musica = request.args.get("filtrar_musica", "false").lower() == "true"

        # Carregar atividades do banco de dados
        # Usar get_all_items para buscar da tabela dicionarios (nome -> atividade, valor -> tempo)
        atividades_dict = db.get_all_items(
            "atividades_casa"
        )  # Retorna um dicionário {nome: valor}
        jogos_dia_semana_dict = db.get_all_items("jogos_casa_dia_semana")
        jogos_fim_semana_dict = db.get_all_items("jogos_casa_fim_semana")
        nintendo_switch_dict = db.get_all_items("nintendo_switch")

        # Adiciona atividades do dia de acordo com o horário
        hora_atual = datetime.now().hour
        if hora_atual < 8:
            atividades_dia_dict = db.get_all_items("atividades_casa_dia")
            for atividade, tempo in atividades_dia_dict.items():
                if atividade not in atividades_dict:  # Evita duplicatas
                    atividades_dict[atividade] = tempo

        # Aplicar filtro de música se necessário
        if filtrar_musica:
            atividades_dict = {
                k: v
                for k, v in atividades_dict.items()
                if "música" not in k.lower()
                and "musica" not in k.lower()
                and "ler livro" not in k.lower()
                and "assistir tv" not in k.lower()
            }

        # Converter para lista de tuplas (atividade, tempo)
        atividades_casa = list(atividades_dict.items())
        # Excluir exercícios físicos entre 7h e 17h
        hora_atual = datetime.now().hour
        if 7 <= hora_atual < 17:
            atividades_casa = [
                (a, t) for a, t in atividades_casa if a != "Praticar exercícios físicos"
            ]
        jogos_casa_dia_semana = list(jogos_dia_semana_dict.items())
        jogos_casa_fim_semana = list(jogos_fim_semana_dict.items())
        nintendo_switch = list(nintendo_switch_dict.items())

        # Obter histórico recente de itens sorteados (últimos 3 itens)
        historico_recente = db.obter_historico_sorteios(3)
        itens_recentes = (
            [item[0] for item in historico_recente] if historico_recente else []
        )

        # Função para verificar se um item está nos itens recentes
        def item_nao_recente(item):
            # Jogos eletrônicos podem ser repetidos, então são sempre "não recentes"
            if item == "Jogos eletrônicos":
                return True
            return item not in itens_recentes

        # 1. Tenta encontrar uma atividade não recente, não mostrada na sessão e dentro do tempo
        atividade_viavel = [
            (atividade, tempo)
            for atividade, tempo in atividades_casa
            if atividade not in shown_activities
            and item_nao_recente(atividade)
            and tempo <= tempo_disponivel
        ]

        # 2. Se não encontrar, tenta ignorando o histórico da sessão (mas ainda verificando itens recentes)
        if not atividade_viavel:
            atividade_viavel = [
                (atividade, tempo)
                for atividade, tempo in atividades_casa
                if item_nao_recente(atividade) and tempo <= tempo_disponivel
            ]

        # 3. Se ainda não encontrar, limpa o histórico da sessão e verifica apenas itens recentes
        if not atividade_viavel:
            shown_activities.clear()
            atividade_viavel = [
                (atividade, tempo)
                for atividade, tempo in atividades_casa
                if item_nao_recente(atividade) and tempo <= tempo_disponivel
            ]

        # 4. Se ainda assim não encontrar, permite itens recentes (último recurso)
        if not atividade_viavel:
            atividade_viavel = [
                (a, t) for a, t in atividades_casa if t <= tempo_disponivel
            ]

        if not atividade_viavel:
            return jsonify(
                {
                    "erro": "Nenhuma atividade disponível para o tempo informado.",
                    "sugestao": "Aumente o tempo disponível ou adicione mais atividades.",
                    "tempo_solicitado": tempo_disponivel,
                }
            ), 404

        # Sortear uma atividade
        atividade_escolhida, tempo_estimado = aleatorio(atividade_viavel)

        # Adicionar a atividade escolhida ao conjunto de mostradas
        shown_activities.add(atividade_escolhida)

        # Log para depuração
        print(f"DEBUG - Atividade escolhida: '{atividade_escolhida}'")
        print(f"DEBUG - Tipo de atividade_escolhida: {type(atividade_escolhida)}")
        print(
            f"DEBUG - Comparação exata: {atividade_escolhida == 'Praticar exercícios físicos'}"
        )

        # Se a atividade for "Praticar exercícios físicos", sempre exibe um exercício específico
        if atividade_escolhida == "Praticar exercícios físicos":
            print("DEBUG - Entrou no bloco de exercícios físicos")
            # Sorteia exercício físico principal
            exercicio = db.get_random_activity("exercicios_fisicos")
            # Se for Ring Fit Adventure, sortear na categoria correta
            if exercicio == "Fazer um exercício avulso no Ring Fit Adventure":
                exercicio = db.get_random_activity("ring_fit")
            # Garante exibição mesmo que não haja exercício encontrado
            exercicio = exercicio or "Nenhum exercício encontrado"
            atividade_escolhida = f"{atividade_escolhida}: {exercicio}"

        # Registrar no banco de dados
        db.registrar_item_sorteado(atividade_escolhida, "casa")

        # Se a atividade for "Ouvir música", chama a rota de música
        if atividade_escolhida.lower() in ["ouvir música", "ouvir musica"]:
            from flask import url_for

            musica_response = get_musica()
            return musica_response

        # Verificar se é "Assistir TV"
        if atividade_escolhida == "Assistir TV":
            programa = db.get_random_activity("tv")
            serie_ou_filme = db.get_random_activity("series_e_filmes")

            return jsonify(
                {
                    "atividade": atividade_escolhida,
                    "tempo_estimado": tempo_estimado,
                    "detalhes": {
                        "programa": programa,
                        "serie_ou_filme": serie_ou_filme,
                    },
                }
            )

        # Verificar se é "Navegar em redes sociais"
        if atividade_escolhida == "Navegar em redes sociais":
            redes_sociais_unesp = db.get_all_activities("redes_sociais_unesp")
            redes_sociais_casa = db.get_all_activities("redes_sociais_casa")
            redes_sociais = redes_sociais_unesp + redes_sociais_casa

            if redes_sociais:
                rede_escolhida = random.choice(redes_sociais)
                db.registrar_item_sorteado(rede_escolhida, "redes_sociais")
                return jsonify(
                    {
                        "atividade": atividade_escolhida,
                        "tempo_estimado": tempo_estimado,
                        "detalhes": {"rede_social": rede_escolhida},
                    }
                )

        # Tratar atividades especiais
        if atividade_escolhida == "Jogos eletrônicos":

            def sortear_jogo(lista_jogos, categoria):
                if not lista_jogos:
                    return None, 0

                # Filtra jogos que não são iguais ao último jogo jogado e estão dentro do tempo
                opcoes = [
                    (j, t)
                    for j, t in lista_jogos
                    if (not itens_recentes or j != itens_recentes[0])
                    and t <= tempo_disponivel
                ]

                if not opcoes:
                    opcoes = [(j, t) for j, t in lista_jogos if t <= tempo_disponivel]

                if not opcoes:
                    return None, 0

                jogo_sorteado, tempo_jogo = aleatorio(opcoes)
                if jogo_sorteado:
                    db.registrar_item_sorteado(jogo_sorteado, categoria)
                return jogo_sorteado, tempo_jogo

            # Verificar se é fim de semana e está entre 9h e 18h
            agora = datetime.now()
            eh_fim_de_semana = agora.weekday() >= 5  # 5 = sábado, 6 = domingo
            horario_comercial = 9 <= agora.hour < 15

            # Se for fim de semana e estiver no horário comercial, inclui jogos de fim de semana
            if eh_fim_de_semana and horario_comercial:
                todos_os_jogos = jogos_casa_dia_semana + jogos_casa_fim_semana
            else:
                todos_os_jogos = jogos_casa_dia_semana

            jogo, tempo_jogo = sortear_jogo(todos_os_jogos, "jogos_casa")

            if not jogo:
                return jsonify(
                    {
                        "erro": "Nenhum jogo disponível para o tempo informado.",
                        "tempo_solicitado": tempo_disponivel,
                    }
                ), 404

            if jogo == "Jogar no Nintendo Switch" and nintendo_switch:
                jogo_switch, tempo_switch = sortear_jogo(
                    nintendo_switch, "nintendo_switch"
                )
                if jogo_switch:
                    return jsonify(
                        {
                            "atividade": atividade_escolhida,
                            "tempo_estimado": tempo_estimado,
                            "detalhes": {
                                "jogo": jogo,
                                "tempo_jogo": tempo_jogo,
                                "nintendo_switch": jogo_switch,
                                "tempo_nintendo_switch": tempo_switch,
                            },
                        }
                    )

            return jsonify(
                {
                    "atividade": atividade_escolhida,
                    "tempo_estimado": tempo_estimado,
                    "detalhes": {"jogo": jogo, "tempo_jogo": tempo_jogo},
                }
            )

        # Para outras atividades, retornar a atividade básica
        return jsonify(
            {"atividade": atividade_escolhida, "tempo_estimado": tempo_estimado}
        )

    except Exception as e:
        import traceback

        traceback.print_exc()
        return jsonify(
            {"erro": "Erro ao processar a solicitação", "detalhes": str(e)}
        ), 500


@bp.route("/musica", methods=["GET"])
def get_musica():
    try:
        musica = db.get_random_activity("multimidia") or "Nenhuma música encontrada"
        db.registrar_item_sorteado(musica, "musica")
        return jsonify({"atividade": "Ouvir música", "detalhes": {"musica": musica}})
    except Exception as e:
        return jsonify({"erro": "Erro ao buscar música", "detalhes": str(e)}), 500

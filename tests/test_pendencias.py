"""testes da interpretação das linhas do Studeo"""

from pendencias import formatar_mensagem, interpretar_linha

LINHA_COM_PENDENCIA = "PROGRAMAÇÃO AVANÇADA 1 Próxima atividade encerra em 9 dias. | 25/10/26 23:59 Acessar"


def test_linha_com_pendencia_vira_dicionario():
    resultado = interpretar_linha(LINHA_COM_PENDENCIA)

    assert resultado == {
        "disciplina": "PROGRAMAÇÃO AVANÇADA",
        "quantidade": 1,
        "prazo": "9 dias",
        "data": "25/10/26 23:59",
    }


def test_linha_sem_pendencia_devolve_none():
    assert interpretar_linha("BANCO DE DADOS Sem atividades pendentes Acessar") is None


def test_cabecalho_da_tabela_devolve_none():
    assert interpretar_linha("DISCIPLINA(S)") is None


def test_espacos_extras_nao_quebram_a_leitura():
    # Regressao: um espaço a mais ja quebrou o parsing uma vez.
    linha = "   PROGRAMAÇÃO AVANÇADA 1   Próxima atividade encerra em 9 dias. |  25/10/26 23:59    Acessar"
    resultado = interpretar_linha(linha)

    assert resultado["disciplina"] == "PROGRAMAÇÃO AVANÇADA"
    assert resultado["quantidade"] == 1


def test_linha_sem_numero_conta_uma_pendencia():
    linha = "BANCO DE DADOS Próxima atividade encerra em 3 dias.    | 20/10/26 23:59 Acessar"
    resultado = interpretar_linha(linha)

    assert resultado["disciplina"] == "BANCO DE DADOS"
    assert resultado["quantidade"] == 1


def test_mensagem_sem_pendencias():
    assert formatar_mensagem([]) == "✅ Studeo: nenhuma atividade pendente."


def test_mensagem_com_pendencias_mostra_disciplina_e_prazo():
    pendencia = interpretar_linha(LINHA_COM_PENDENCIA)
    mensagem = formatar_mensagem([pendencia])

    assert "PROGRAMAÇÃO AVANÇADA (1 pendência(s))" in mensagem
    assert "encerra em 9 dias (25/10/26 23:59)" in mensagem

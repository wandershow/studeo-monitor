"""Testes da memória entre execuções."""

import historico


def pendencia(prazo="9 dias", quantidade=1, data="25/10/26 23:59"):
    """Cria uma pendência de exemplo, só mudando o que o teste precisar."""
    return {
        "disciplina": "PROGRAMAÇÃO AVANÇADA",
        "quantidade": quantidade,
        "prazo": prazo,
        "data": data,
    }


def test_primeira_execucao_sempre_avisa(tmp_path, monkeypatch):
    monkeypatch.setattr(historico, "ARQUIVO", tmp_path / "estado.json")

    assert historico.houve_mudanca([pendencia()]) is True


def test_sem_mudanca_nao_avisa(tmp_path, monkeypatch):
    monkeypatch.setattr(historico, "ARQUIVO", tmp_path / "estado.json")
    historico.salvar_atual([pendencia()])

    assert historico.houve_mudanca([pendencia()]) is False


def test_prazo_em_dias_mudando_nao_conta_como_mudanca(tmp_path, monkeypatch):
    monkeypatch.setattr(historico, "ARQUIVO", tmp_path / "estado.json")
    historico.salvar_atual([pendencia(prazo="9 dias")])

    assert historico.houve_mudanca([pendencia(prazo="8 dias")]) is False


def test_nova_quantidade_conta_como_mudanca(tmp_path, monkeypatch):
    monkeypatch.setattr(historico, "ARQUIVO", tmp_path / "estado.json")
    historico.salvar_atual([pendencia(quantidade=1)])

    assert historico.houve_mudanca([pendencia(quantidade=2)]) is True


def test_nova_data_conta_como_mudanca(tmp_path, monkeypatch):
    monkeypatch.setattr(historico, "ARQUIVO", tmp_path / "estado.json")
    historico.salvar_atual([pendencia(data="25/10/26 23:59")])

    assert historico.houve_mudanca([pendencia(data="30/10/26 23:59")]) is True

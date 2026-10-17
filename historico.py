"""guarda as pendencias da ultima execuçãp para avisar so quando algo mudar."""

import json
from pathlib import Path

ARQUIVO = Path(__file__).resolve().parent / "ultimo estado json"


def resumo(pendencias: list[dict]) -> list[dict]:
    """Fica só com o que identifica pendencia. O o prazo em dias muda todo dia"""
    return [
        {
            "disciplina": p["disciplina"],
            "quantidade": p["quantidade"],
            "data": p["data"],
        }
        for p in pendencias
    ]


def carregar_anterior() -> list[dict] | None:
    """Lê o estado salvo na ultima execuçao, ou None se for a primeira vez"""
    if not ARQUIVO.exists():
        return None
    return json.loads(ARQUIVO.read_text(encoding="utf-8"))


def salvar_atual(pendencias: list[dict]) -> None:
    """Grava o estado atual para a proxima comparação"""

    texto = json.dumps(resumo(pendencias), ensure_ascii=False, indent=2)
    ARQUIVO.write_text(texto, encoding="utf-8")


def houve_mudanca(pendencias: list[dict]) -> bool:
    """True se as dempendencias de agora são diferentes das da ultima vez"""
    return resumo(pendencias) != carregar_anterior()

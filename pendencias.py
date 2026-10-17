"""Interpreta as linhas da tabela de atividades do Studeo."""

SEPARADOR = "Próxima atividade encerra em"


def interpretar_linha(texto: str) -> dict | None:
    """Transforma uma linha da tabela num dicionário, ou None se não houver pendência."""
    if SEPARADOR not in texto:
        return None

    antes, depois = texto.split(SEPARADOR, 1)
    antes = antes.strip()
    depois = depois.strip()

    # "PROGRAMAÇÃO AVANÇADA 1" -> disciplina e quantidade
    partes = antes.rsplit(" ", 1)
    if len(partes) == 2 and partes[1].isdigit():
        disciplina, quantidade = partes
    else:
        disciplina, quantidade = antes, "1"

    # "9 dias. | 25/10/26 23:59 Acessar" -> prazo e data
    prazo, data = depois.split("|", 1)
    prazo = prazo.strip().rstrip(".")
    data = data.strip().removesuffix("Acessar").strip()

    return {
        "disciplina": disciplina,
        "quantidade": int(quantidade),
        "prazo": prazo,
        "data": data,
    }


def formatar_mensagem(pendencias: list[dict]) -> str:
    """Monta o texto do aviso a partir da lista de pendências."""
    if not pendencias:
        return "✅ Studeo: nenhuma atividade pendente."

    linhas = ["📚 Studeo: atividades pendentes", ""]
    for p in pendencias:
        linhas.append(f"• {p['disciplina']} ({p['quantidade']} pendência(s))")
        linhas.append(f"  encerra em {p['prazo']} ({p['data']})")

    return "\n".join(linhas)


if __name__ == "__main__":
    exemplo = "PROGRAMAÇÃO AVANÇADA 1 Próxima atividade encerra em 9 dias. | 25/10/26 23:59 Acessar"
    print(interpretar_linha(exemplo))
    print(interpretar_linha("BANCO DE DADOS Sem atividades pendentes Acessar"))

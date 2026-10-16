"""Carrega e valida as configuraçoes do projeto a partir do arquivo .env."""

import os
import sys
from pathlib import Path 

from dotenv import load_dotenv

# Pasta onde este arquivo esta, para o .env mesmo rodando de outro lugar.
PASTA_PROJETO = Path(__file__).resolve().parent

#Le o .env e coloca cada linha CHAVE=valor nas variaveis de ambiente.
load_dotenv(PASTA_PROJETO / ".env")

VARIAVEIS_OBRIGATORIAS =[
    "STUDEO_USUARIO",
    "STUDEO_SENHA",
    "WHATSAPP_NUMERO",
    "CALLMEBOT_APIKEY",
]

def carregar_config() ->dict:
    """devolve um dicionario com as configurações, ou encerra se faltar alguma."""
    config = {nome: os.getenv(nome) for nome in VARIAVEIS_OBRIGATORIAS}

    faltando = [nome for nome, valor in config.items() if not valor]
    if faltando:
        sys.exit(f"faltam variaveis no .env: {', '.join(faltando)}")

    return config 


if __name__ == "__main__":
    config = carregar_config()
    print("configuração carregada:")
    for nome, valor in config.items():
        # Nunca mostre segredos no Terminal.
        segredo = "SENHA" in nome or "APIKEY" in nome
        print(f"    {nome} = {'********' if segredo else valor}")

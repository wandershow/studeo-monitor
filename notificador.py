"""Envia mensagens para o meu whatsapp usando a API gratuita CallMeBot. """

import requests

from config import carregar_config

URL_CALLMEBOT = "https://api.callmebot.com/whatsapp.php"


def enviar_whatsapp(texto: str) -> None:
    """envia texto para o numero configurado no .env"""
    config = carregar_config()


    # Enquanto a apikey não chega, só mostra a mensagem no terminal.
    if config["CALLMEBOT_APIKEY"]  == "pendente":
        print("[apikey pendente] mensagem que seria enviada:\n" + texto)
        return

    parametros = {
        "phone": config["WHATSAPP_NUMERO"],
        "text": texto,
        "apikey": config["CALLMEBOT_APIKEY"],
    }

    resposta = requests.get(URL_CALLMEBOT, params=parametros, timeout=30)
    resposta.raise_for_status()

    if "error" in resposta.text.lower():
        raise RuntimeError(f"O CallMeBot recusou a mensagem: {resposta.text[:200]}")
    print("mensagem negada")


if __name__ == "__main__":
    enviar_whatsapp("🤖 Olá! Esta é a primeira mensagem enviada pelo meu código Python.")

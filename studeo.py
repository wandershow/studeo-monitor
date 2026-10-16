"""Automaçao do navegador para acessar o Studeo."""

from playwright.sync_api import sync_playwright

URL_LOGIN = "https://studeo.unicesumar.edu.br/#!/access/login"


def abrir_pagina_login() -> None:
    """Abre a pagina de login, tira um print e fecha."""
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=False, slow_mo=500)
        pagina = navegador.new_page()

        pagina.goto(URL_LOGIN)
        pagina.wait_for_timeout(5000) #Espera 5 segundos para a pagina carregar

        pagina.screenshot(path="login.png")
        print("Titulo da pagina:", pagina.title())


        navegador.close

if __name__ == "__main__":
    abrir_pagina_login()
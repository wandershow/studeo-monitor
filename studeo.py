"""Automação do navegador para acessar o studeo"""

from playwright.sync_api import sync_playwright

from config import carregar_config

URL_LOGIN = "https://studeo.unicesumar.edu.br/#!/access/login"


def fazer_login(pagina, usuario: str, senha: str) ->None:
    """preenche o formulario de login e espera sair da tela de login"""
    pagina.goto(URL_LOGIN)

    pagina.get_by_role("textbox", name="Usuário/CPF").fill(usuario)
    pagina.get_by_role("textbox", name="Senha").fill(senha)
    pagina.get_by_role("button", name="ENTRAR").click()

    #Se o login deu certo, o endereço deixa de ter "access/login".
    pagina.wait_for_url(lambda url: "access/login" not in url, timeout=30000)


def main() -> None:
    config = carregar_config()

    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=False, slow_mo=500)
        pagina = navegador.new_page()

        fazer_login(pagina, config["STUDEO_USUARIO"], config["STUDEO_SENHA"])
        print("lOGIN FEITO! endereço atual:", pagina.url)

        pagina.wait_for_timeout(5000)
        pagina.screenshot(path="pos_login.png")

        navegador.close()

if __name__ == "__main__":
    main()


"""Automação do navegador para acessar o studeo"""

from playwright.sync_api import sync_playwright

from config import carregar_config

URL_LOGIN = "https://studeo.unicesumar.edu.br/#!/access/login"


def fazer_login(pagina, usuario: str, senha: str) -> None:
    """preenche o formulario de login e espera sair da tela de login"""
    pagina.goto(URL_LOGIN)

    pagina.get_by_role("textbox", name="Usuário/CPF").fill(usuario)
    pagina.get_by_role("textbox", name="Senha").fill(senha)
    pagina.get_by_role("button", name="ENTRAR").click()

    # Se o login deu certo, o endereço deixa de ter "access/login".
    pagina.wait_for_url(lambda url: "access/login" not in url, timeout=30000)


def ler_atividades(pagina) -> list[str]:
    """Abre o painel de atividades e devolve o texto de cada linha da tabela."""
    pagina.get_by_role("link", name="Acompanhamento de Atividades").click()

    tabela = pagina.get_by_role("table")
    tabela.wait_for(timeout=15000)

    atividades = []
    for linha in tabela.get_by_role("row").all():
        texto = " ".join(linha.inner_text().split())
        if texto:
            atividades.append(texto)

    return atividades


def main() -> None:
    config = carregar_config()

    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=False, slow_mo=500)
        pagina = navegador.new_page()

        fazer_login(pagina, config["STUDEO_USUARIO"], config["STUDEO_SENHA"])
        print("LOGIN FEITO! endereço atual:", pagina.url)

        atividades = ler_atividades(pagina)
        print(f"\n{len(atividades)} linha(s) encontradas:")
        for item in atividades:
            print("-", item)

        navegador.close()


if __name__ == "__main__":
    main()

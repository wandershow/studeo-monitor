"""Automação do navegador para acessar o Studeo."""

from playwright.sync_api import sync_playwright

from config import carregar_config
from notificador import enviar_whatsapp
from pendencias import formatar_mensagem, interpretar_linha

from historico import houve_mudanca, salvar_atual

URL_LOGIN = "https://studeo.unicesumar.edu.br/#!/access/login"


def fazer_login(pagina, usuario: str, senha: str) -> None:
    """Preenche o formulário de login e espera sair da tela de login."""
    pagina.goto(URL_LOGIN)

    pagina.get_by_role("textbox", name="CPF").fill(usuario)
    pagina.get_by_role("textbox", name="Senha").fill(senha)
    pagina.get_by_role("button", name="Entrar").click()

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
        linhas = ler_atividades(pagina)

        navegador.close()
    # Daqui para baixo nao precisamos mais usar o navegador
    pendencias = []
    for linha in linhas:
        item = interpretar_linha(linha)
        if item:
            pendencias.append(item)

    if houve_mudanca(pendencias):
        enviar_whatsapp(formatar_mensagem(pendencias))
        salvar_atual(pendencias)
    else:
        print("Nada mudou desde o ultimo aviso. nenhuma mensagem Enviada")


if __name__ == "__main__":
    main()

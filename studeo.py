"""Automação do navegador para acessar o Studeo."""

from playwright.sync_api import sync_playwright

from config import carregar_config
from notificador import enviar_whatsapp
from pendencias import formatar_mensagem, interpretar_linha

from historico import houve_mudanca, salvar_atual
import sys
from datetime import datetime

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
    print(f"\n=== Execução em {datetime.now():%d/%m/%Y %H:%M} ===")
    config = carregar_config()

    # com "--visivel" o navegador aparece.sem isso, roda invisivel.
    visivel = "--visivel" in sys.argv

    with sync_playwright() as p:
        navegador = p.chromium.launch(
            headless=not visivel, slow_mo=500 if visivel else 0
        )
        pagina = navegador.new_page()

        try:
            fazer_login(pagina, config["STUDEO_USUARIO"], config["STUDEO_SENHA"])
            linhas = ler_atividades(pagina)
        except Exception as erro:
            pagina.screenshot(path="erro.png")
            enviar_whatsapp(f"⚠️ O monitor do Studeo falhou: {str(erro)[:300]}")
            raise
        finally:
            navegador.close()

    # Daqui para baixo não usamos mais o navegador, então pode ficar fora do "with".
    pendencias = []
    for linha in linhas:
        item = interpretar_linha(linha)
        if item:
            pendencias.append(item)

    if houve_mudanca(pendencias):
        enviar_whatsapp(formatar_mensagem(pendencias))
        salvar_atual(pendencias)
    else:
        print("Nada mudou desde o ultimo aviso. Nenhuma mensagem enviada.")


if __name__ == "__main__":
    main()

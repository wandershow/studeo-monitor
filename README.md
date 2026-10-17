
---

## Sobre o desenvolvimento

Projeto feito em paralelo à graduação em Análise e Desenvolvimento de Sistemas,
com o **Claude** (IA da Anthropic) como mentor: explicando cada conceito, revisando
o código e ajudando a interpretar cada mensagem de erro.

Todo o código foi digitado à mão, como faziam os Incas e os Maias. Quando eu travava,
comparava minha versão com a sugestão do mentor e ajustava o meu código, na tentativa
e erro, até entender a diferença. Cada erro de digitação, indentação e parêntese
esquecido foi lido, entendido e corrigido por mim, e muitos viraram lições (e testes)
deste projeto.

Feito por **Wanderson Silva**.


# Studeo Monitor

Robô em Python que acessa o Studeo (ambiente de estudos da Unicesumar), verifica as
atividades pendentes de todas as disciplinas e me avisa pelo WhatsApp **somente quando
algo muda**: uma atividade nova, uma entrega feita ou um prazo alterado.

> O robô apenas **lê** a tela de acompanhamento de atividades. Ele não abre, não
> responde e não envia nenhuma atividade.

## Exemplo de aviso

```
📚 Studeo: atividades pendentes

- PROGRAMAÇÃO AVANÇADA (1 pendência(s))
  encerra em 8 dias (25/10/26 23:59)
- PROJETO DE ENSINO - LGPD NAS ORGANIZAÇÕES E EMPRESAS (1 pendência(s))
  encerra em um mês (29/11/26 23:59)
```

## Como funciona

1. **Login automático** com Playwright, usando credenciais guardadas no `.env`.
2. **Leitura** da tabela "Acompanhamento de Atividades".
3. **Interpretação** de cada linha em dados estruturados (disciplina, quantidade, prazo, data).
4. **Comparação** com a execução anterior, salva em JSON. O prazo em dias muda todo dia,
   então a comparação usa só disciplina, quantidade e data de entrega.
5. **Aviso** pelo WhatsApp (via CallMeBot), apenas quando há mudança.
6. **Agendamento** diário pelo Agendador de Tarefas do Windows, rodando em modo invisível.

Se algo falhar (site fora do ar, mudança na página), o robô envia um aviso de erro, salva
um print da tela no momento da falha e registra tudo em `execucoes.log`.

## Tecnologias

- **Python 3**
- **Playwright**: automação do navegador
- **requests**: integração com a API do CallMeBot
- **python-dotenv**: configuração segura com variáveis de ambiente
- **pytest**: testes automáticos

## Estrutura

```
studeo-monitor/
├── studeo.py          # orquestra tudo: login, leitura e aviso
├── pendencias.py      # interpreta as linhas da tabela e monta a mensagem
├── historico.py       # memória entre execuções (JSON)
├── notificador.py     # envio pelo WhatsApp
├── config.py          # carrega e valida o .env
├── rodar.bat          # execução agendada no Windows
└── tests/             # testes automáticos
```

O código que mexe com o navegador fica separado do código que só trata dados.
Por isso a lógica principal pode ser testada em menos de 1 segundo, sem abrir navegador.

## Como rodar

```bash
git clone https://github.com/SEU-USUARIO/studeo-monitor.git
cd studeo-monitor
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements-dev.txt
playwright install chromium
```

Copie `.env.example` para `.env` e preencha com seus dados. Depois:

```bash
python studeo.py              # roda invisível
python studeo.py --visivel    # mostra o navegador
pytest -v                     # roda os testes
```

## Segurança

- Credenciais ficam só no `.env`, que está no `.gitignore` e nunca vai para o GitHub.
- Prints, log e o arquivo de estado também ficam fora do repositório, porque contêm dados pessoais.

## O que aprendi

- Automação de navegador com Playwright: seletores por *role*, espera automática e leitura do *Call log* para depurar.
- Consumo de APIs HTTP, códigos de status e por que sempre usar `timeout`.
- Tratamento de dados reais: um único espaço a mais no texto quebrava a leitura.
  Isso virou um teste de regressão.
- `try / except / finally` para garantir que o navegador sempre fecha e que erros sejam avisados.
- Persistência simples com JSON e a decisão de projeto sobre o que conta como "mudança".
- Testes automáticos com pytest, usando `tmp_path` e `monkeypatch` para não tocar em arquivos reais.
- Git com commits pequenos e mensagens no padrão Conventional Commits.

## Próximos passos

- [ ] Busca do texto das pendências sem diferenciar maiúsculas e minúsculas
- [ ] Destacar atividades que vencem em poucos dias
- [ ] Rodar na nuvem com GitHub Actions

---

Feito por **Wanderson Silva** durante a graduação em Análise e Desenvolvimento de Sistemas.


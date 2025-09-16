# Discord KeyAdmin Bot

Bot de Discord integrado ao seu backend KeyAdmin. Inclui slash commands, logs configuráveis, checks de permissão e um wrapper de API isolado.

## Recursos
- Slash commands com `discord.py` 2.x
- Sincronização de comandos por servidor (desenvolvimento) ou global (produção)
- Wrapper `KeyAdminAPI` com métodos para criação, status, banimento, desbloqueio, reset de HWID e remoção de chaves
- Estrutura extensível em Cogs
- Configuração por `.env`

## Pré‑requisitos
- Python 3.10+
- Uma aplicação de bot criada no Developer Portal do Discord (token do bot)
- Endpoints HTTP do seu painel KeyAdmin (ex.: `/criar_key.php`, `/status.php`, `/banir_key.php`, `/desbanir_key.php`, `/reset_hwid.php`, `/deletar_key.php`). Ajuste as rotas em `keyadmin_api.py` conforme seu painel.

## Configuração
1. Copie `.env.example` para `.env` e preencha:
   - `DISCORD_TOKEN`: token do bot no Discord
   - `DEV_GUILD_ID`: opcional, ID do seu servidor de teste para sincronização imediata dos comandos
   - `KEYADMIN_BASE_URL`: base da sua API (ex.: `https://seu-dominio.com.br/api`)
   - `KEYADMIN_CLIENTE_HASH`, `KEYADMIN_API_KEY`, `KEYADMIN_SOFTWARE_ID`: credenciais do seu painel

2. Instale dependências:
   ```bash
   python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Execute:
   ```bash
   python bot.py
   ```

## Comandos
Os comandos ficam no grupo `/ka`:
- `/ka status key:<texto>` — Consulta status da key
- `/ka gerar validade:<dia|semana|mes|vitalicia> qtd:<int> [prefixo] [sufixo] [tamanho]` — Gera novas chaves
- `/ka ban key:<texto> [motivo]` — Bane a key
- `/ka unban key:<texto>` — Desbane a key
- `/ka reset_hwid key:<texto>` — Reseta HWID
- `/ka deletar key:<texto>` — Exclui a key

Por padrão, somente administradores do servidor podem usar. Você pode liberar usuários específicos editando a verificação em `utils/checks.py`.

## Ajustando Endpoints
Em `keyadmin_api.py` existem constantes com os caminhos dos endpoints. Caso seu painel use rotas diferentes, altere ali. O corpo das requisições usa JSON por padrão.

## Estrutura
```
discord-keyadmin-bot/
├─ .gitignore
├─ .env.example
├─ README.md
├─ requirements.txt
├─ LICENSE
├─ bot.py
├─ keyadmin_api.py
├─ utils/
│  └─ checks.py
└─ cogs/
   └─ licenses.py
```

## Deploy
- GitHub: crie um repositório e faça push deste projeto
- VPS/Local: mantenha o `.env` fora do Git. Para serviço, use systemd ou PM2 (via `pm2 start "python bot.py"` com interprete correto)

## Segurança
- Não faça commit do `.env`
- Restrinja o uso dos comandos apenas a administradores ou a uma lista explícita de usuários
# 🤖 Discord Bot — Python + discord.py

Bot profissional para Discord com comandos de informação, pronto para deploy.

## ✨ Comandos disponíveis
| Comando | Descrição |
|---|---|
| `!ping` | Latência WebSocket do bot |
| `!serverinfo` | Info do servidor (nome, membros, dono, data de criação) |
| `!user [@membro]` | Info do usuário (nome, ID, data que entrou) |
| `!avatar [@membro]` | Avatar em alta resolução com links de download |
| `!help` | Lista todos os comandos |

## 🚀 Como rodar em 2 minutos
1. `git clone https://github.com/andreiniciantepython/bot-discord-python.git`
2. `cd bot-discord-python`
3. `pip install -r requirements.txt`
4. config.py → TOKEN = "SEU_TOKEN"
5. `python main.py`

**Token Discord**: discord.com/developers/applications → New App → Bot → Reset Token

## 📁 Estrutura
bot-discord-python/
├── main.py
├── config.py
├── requirements.txt
├── README.md
└── cogs/
├── __init__.py(vazio)
└── commands.py

text

## 🛠️ Tech
- Python 3.10+
- discord.py 2.x (cogs + embeds)
- Intents all + asyncio

## ⚙️ Customizar
- Prefixo: config.py → PREFIX
- Cor embed: config.py → COLOR  
- +Comandos: cogs/commands.py

## 🔒 Segurança
**.gitignore**: config.py, .env

MIT License © 2026 André — Freelancer R$30-100
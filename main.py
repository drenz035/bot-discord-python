# main.py — Ponto de entrada do bot

import asyncio
import logging
import os

import discord
from discord.ext import commands

import config

# ── Logging ─────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("bot")

# ── Intents ─────────────────────────────────────────────────
intents = discord.Intents.all()   # Habilita todos os intents

# ── Bot ──────────────────────────────────────────────────────
bot = commands.Bot(
    command_prefix=config.PREFIX,
    intents=intents,
    help_command=commands.DefaultHelpCommand(no_category="Comandos"),
    case_insensitive=True,            # !PING == !ping
)

# ── Cogs a carregar ──────────────────────────────────────────
COGS = [
    "cogs.commands",
]

# ── Eventos ─────────────────────────────────────────────────
@bot.event
async def on_ready():
    log.info(f"Bot conectado como {bot.user} (ID: {bot.user.id})")
    log.info(f"Servidores: {len(bot.guilds)}")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{config.PREFIX}help | {len(bot.guilds)} servers",
        )
    )

@bot.event
async def on_command_error(ctx: commands.Context, error):
    """Handler global de erros (fallback)."""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"❓ Comando não encontrado. Use `{config.PREFIX}help` para ver os disponíveis.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"⚠️ Argumento faltando: `{error.param.name}`. Use `{config.PREFIX}help {ctx.command}` para mais info.")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ Aguarde **{error.retry_after:.1f}s** antes de usar este comando novamente.")

# ── Setup e start ────────────────────────────────────────────
async def main():
    async with bot:
        for cog in COGS:
            try:
                await bot.load_extension(cog)
                log.info(f"Cog carregado: {cog}")
            except Exception as e:
                log.error(f"Falha ao carregar {cog}: {e}")

        await bot.start(config.TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
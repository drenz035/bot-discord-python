
# cogs/commands.py — Todos os comandos do bot organizados em Cog

import discord
from discord.ext import commands
from datetime import timezone
import config


class Commands(commands.Cog, name="Comandos Gerais"):
    """Cog principal com os comandos gerais do bot."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ----------------------------------------------------------
    # !ping — Latência do bot
    # ----------------------------------------------------------
    @commands.command(name="ping", help="Mostra a latência do bot.")
    async def ping(self, ctx: commands.Context):
        latency_ms = round(self.bot.latency * 1000)

        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latência WebSocket: **{latency_ms} ms**",
            color=config.COLOR,
        )
        embed.set_footer(text=f"Solicitado por {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

    # ----------------------------------------------------------
    # !serverinfo — Informações do servidor
    # ----------------------------------------------------------
    @commands.command(name="serverinfo", help="Exibe informações do servidor.")
    @commands.guild_only()
    async def serverinfo(self, ctx: commands.Context):
        guild = ctx.guild

        # Data de criação sem microsegundos
        created_at = guild.created_at.replace(tzinfo=timezone.utc)
        created_str = discord.utils.format_dt(created_at, style="D")   # ex: 12 de janeiro de 2021
        created_rel = discord.utils.format_dt(created_at, style="R")   # ex: há 4 anos

        embed = discord.Embed(
            title=f"🏠 {guild.name}",
            color=config.COLOR,
        )

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        embed.add_field(name="👑 Dono", value=guild.owner.mention if guild.owner else "Desconhecido", inline=True)
        embed.add_field(name="👥 Membros", value=f"{guild.member_count:,}", inline=True)
        embed.add_field(name="🆔 ID do Servidor", value=f"`{guild.id}`", inline=True)
        embed.add_field(name="📅 Criado em", value=f"{created_str}\n({created_rel})", inline=True)
        embed.add_field(name="💬 Canais de Texto", value=len(guild.text_channels), inline=True)
        embed.add_field(name="🔊 Canais de Voz", value=len(guild.voice_channels), inline=True)
        embed.add_field(name="🎭 Cargos", value=len(guild.roles), inline=True)
        embed.add_field(name="😀 Emojis", value=len(guild.emojis), inline=True)

        embed.set_footer(text=f"Solicitado por {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

    # ----------------------------------------------------------
    # !user — Informações do usuário que enviou
    # ----------------------------------------------------------
    @commands.command(name="user", aliases=["userinfo", "eu"], help="Exibe suas informações no servidor.")
    @commands.guild_only()
    async def user(self, ctx: commands.Context, membro: discord.Member = None):
        # Se nenhum membro for mencionado, usa quem enviou
        member = membro or ctx.author

        joined_at = member.joined_at.replace(tzinfo=timezone.utc) if member.joined_at else None
        joined_str = discord.utils.format_dt(joined_at, style="D") if joined_at else "Desconhecido"
        joined_rel = discord.utils.format_dt(joined_at, style="R") if joined_at else ""

        created_at = member.created_at.replace(tzinfo=timezone.utc)
        created_str = discord.utils.format_dt(created_at, style="D")

        # Cargos (exceto @everyone)
        roles = [r.mention for r in reversed(member.roles) if r.name != "@everyone"]
        roles_str = " ".join(roles) if roles else "Nenhum cargo"

        embed = discord.Embed(
            title=f"👤 {member.display_name}",
            color=member.color if member.color.value != 0 else config.COLOR,
        )
        embed.set_thumbnail(url=member.display_avatar.url)

        embed.add_field(name="🏷️ Nome Completo", value=str(member), inline=True)
        embed.add_field(name="🆔 ID", value=f"`{member.id}`", inline=True)
        embed.add_field(name="🤖 É Bot?", value="Sim" if member.bot else "Não", inline=True)
        embed.add_field(name="📅 Conta Criada", value=created_str, inline=True)
        embed.add_field(name="📥 Entrou no Server", value=f"{joined_str}\n({joined_rel})", inline=True)
        embed.add_field(name="🎭 Cargos", value=roles_str[:1024], inline=False)

        embed.set_footer(text=f"Solicitado por {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

    # ----------------------------------------------------------
    # !avatar — Envia o avatar do usuário
    # ----------------------------------------------------------
    @commands.command(name="avatar", aliases=["av", "foto"], help="Exibe o avatar de um usuário.")
    async def avatar(self, ctx: commands.Context, membro: discord.Member = None):
        member = membro or ctx.author
        avatar_url = member.display_avatar.url

        embed = discord.Embed(
            title=f"🖼️ Avatar de {member.display_name}",
            color=config.COLOR,
            url=avatar_url,           # Clicável
        )
        embed.set_image(url=avatar_url)

        # Links de download em diferentes tamanhos
        sizes = [128, 256, 512, 1024]
        links = " | ".join(
            f"[{s}px]({member.display_avatar.with_size(s).url})"
            for s in sizes
        )
        embed.add_field(name="📥 Download", value=links, inline=False)
        embed.set_footer(text=f"Solicitado por {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

    # ----------------------------------------------------------
    # Tratamento de erros por comando
    # ----------------------------------------------------------
    @ping.error
    @serverinfo.error
    @user.error
    @avatar.error
    async def command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("❌ Este comando só pode ser usado em servidores.")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("❌ Membro não encontrado. Mencione alguém válido.")
        else:
            await ctx.send(f"❌ Erro inesperado: `{error}`")
            raise error  # Mantém o log no console para debug


async def setup(bot: commands.Bot):
    """Função chamada pelo bot ao carregar o cog."""
    await bot.add_cog(Commands(bot))

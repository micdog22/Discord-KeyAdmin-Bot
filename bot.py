import os
import logging
from typing import Optional

import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN", "").strip()
DEV_GUILD_ID = os.getenv("DEV_GUILD_ID", "").strip()
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
log = logging.getLogger("keyadmin.bot")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

async def sync_commands(tree: app_commands.CommandTree, guild_id: Optional[int]):
    if guild_id:
        guild = discord.Object(id=guild_id)
        await tree.sync(guild=guild)
        log.info("Slash commands sincronizados para guild %s", guild_id)
    else:
        await tree.sync()
        log.info("Slash commands sincronizados globalmente")

@bot.event
async def on_ready():
    guild_id = int(DEV_GUILD_ID) if DEV_GUILD_ID.isdigit() else None
    await sync_commands(bot.tree, guild_id)
    log.info("Logado como %s (%s)", bot.user, bot.user.id)

async def main():
    await bot.load_extension("cogs.licenses")
    await bot.start(TOKEN)

if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError("Defina DISCORD_TOKEN no arquivo .env")
    import asyncio
    asyncio.run(main())
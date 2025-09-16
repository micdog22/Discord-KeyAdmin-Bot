from typing import Optional
            import json
            import discord
            from discord import app_commands, Interaction
            from discord.ext import commands

            from keyadmin_api import KeyAdminAPI, KeyAdminConfig
            from utils.checks import has_admin_or_allowed

            class KeyAdminCog(commands.Cog):
                def __init__(self, bot: commands.Bot):
                    self.bot = bot
                    self.api = KeyAdminAPI(KeyAdminConfig.from_env())

                group = app_commands.Group(name="ka", description="Comandos KeyAdmin")

                @group.command(name="status", description="Consulta status de uma key")
                @app_commands.describe(key="Chave a consultar")
                async def status(self, interaction: Interaction, key: str):
                    if not has_admin_or_allowed(interaction):
                        return await interaction.response.send_message("Acesso negado.", ephemeral=True)
                    await interaction.response.defer(thinking=True, ephemeral=True)
                    data = await self.api.status_key(key)
                    text = json.dumps(data, ensure_ascii=False, indent=2)
                    await interaction.followup.send(f"Status da key:
```json
{text}
```", ephemeral=True)

                @group.command(name="gerar", description="Gera novas chaves")
                @app_commands.describe(
                    validade="dia | semana | mes | vitalicia",
                    qtd="Quantidade de chaves",
                    prefixo="Opcional",
                    sufixo="Opcional",
                    tamanho="Tamanho total desejado (com prefixo+sufixo)"
                )
                async def gerar(self, interaction: Interaction, validade: str, qtd: int, prefixo: Optional[str] = "", sufixo: Optional[str] = "", tamanho: Optional[int] = 20):
                    if not has_admin_or_allowed(interaction):
                        return await interaction.response.send_message("Acesso negado.", ephemeral=True)
                    await interaction.response.defer(thinking=True, ephemeral=True)
                    data = await self.api.create_keys(validade=validade, qtd=qtd, prefixo=prefixo or "", sufixo=sufixo or "", tamanho=tamanho or 20)
                    text = json.dumps(data, ensure_ascii=False, indent=2)
                    await interaction.followup.send(f"Resultado da geração:
```json
{text}
```", ephemeral=True)

                @group.command(name="ban", description="Bane uma key")
                @app_commands.describe(key="Chave", motivo="Motivo opcional")
                async def ban(self, interaction: Interaction, key: str, motivo: Optional[str] = None):
                    if not has_admin_or_allowed(interaction):
                        return await interaction.response.send_message("Acesso negado.", ephemeral=True)
                    await interaction.response.defer(thinking=True, ephemeral=True)
                    data = await self.api.ban_key(key, motivo)
                    text = json.dumps(data, ensure_ascii=False, indent=2)
                    await interaction.followup.send(f"Resultado do banimento:
```json
{text}
```", ephemeral=True)

                @group.command(name="unban", description="Desbane uma key")
                @app_commands.describe(key="Chave")
                async def unban(self, interaction: Interaction, key: str):
                    if not has_admin_or_allowed(interaction):
                        return await interaction.response.send_message("Acesso negado.", ephemeral=True)
                    await interaction.response.defer(thinking=True, ephemeral=True)
                    data = await self.api.unban_key(key)
                    text = json.dumps(data, ensure_ascii=False, indent=2)
                    await interaction.followup.send(f"Resultado do desbanimento:
```json
{text}
```", ephemeral=True)

                @group.command(name="reset_hwid", description="Reseta HWID de uma key")
                @app_commands.describe(key="Chave")
                async def reset_hwid(self, interaction: Interaction, key: str):
                    if not has_admin_or_allowed(interaction):
                        return await interaction.response.send_message("Acesso negado.", ephemeral=True)
                    await interaction.response.defer(thinking=True, ephemeral=True)
                    data = await self.api.reset_hwid(key)
                    text = json.dumps(data, ensure_ascii=False, indent=2)
                    await interaction.followup.send(f"Resultado do reset de HWID:
```json
{text}
```", ephemeral=True)

                @group.command(name="deletar", description="Deleta uma key")
                @app_commands.describe(key="Chave")
                async def deletar(self, interaction: Interaction, key: str):
                    if not has_admin_or_allowed(interaction):
                        return await interaction.response.send_message("Acesso negado.", ephemeral=True)
                    await interaction.response.defer(thinking=True, ephemeral=True)
                    data = await self.api.delete_key(key)
                    text = json.dumps(data, ensure_ascii=False, indent=2)
                    await interaction.followup.send(f"Resultado da exclusão:
```json
{text}
```", ephemeral=True)

            async def setup(bot: commands.Bot):
                await bot.add_cog(KeyAdminCog(bot))
                bot.tree.add_command(KeyAdminCog.group)
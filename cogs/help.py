import discord
from discord.ext import commands
from discord_components import DiscordComponents, ComponentsBot, Button, SelectOption, Select


class HelpCog(commands.HelpCommand):
    def __init__(self, **options):
        super().__init__(**options)
        self.color = discord.Color(0x2F3136)

    async def send_bot_help(self, mapping):
        ctx = self.context
        prefix = ctx.prefix

        embed = discord.Embed(title="Ajuda do Eco DJ", color=self.color)
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)

        description = f"Para obter ajuda mais detalhada escreva: `{prefix}help <comando>` \n\n"
        description += "**Comandos de Música** \n`!play` Pesquise e reproduza qualquer música\n\n`!skip` Pule para a próxima música ou pare a música atual\n\n`!pause` Pausar a música\n\n`!resume` Volte onde a música parou\n\n`!seek` Avançar ou retroceder tantos segundos da música\n\n`!volume` Alterar o volume do bot\n\n`!loop` Loop the music with 3 possible options\n\n`!nowplaying` Veja a música que está tocando atualmente\n\n`!queue` Mostrar a lista de músicas\n\n`!equalizer` Altere a equalização da música com 3 opções diferentes\n\n`!lyrics` Veja a letra da música\n\n"
        description += "**Comandos de Nível** \n`!rank` Mostre seu nível no servidor\n\n`!leaderboard` Mostrar a tabela de classificação do servidor\n\n "
        description += "**Comandos de Games** \n Jogo da Velha:\n `!tictactoe` Comece o jogo da velha com um jogador\n\n `!place` Informa a posição do local escolhido de 1 a 9\n\n Tetris:\n `!tetris` Começa o jogo tetris\n\n"
        description += "**Comandos de Meme** \n`!meme` Receba um meme haha\n\n"
        description += "Desenvolvido por: Carlos Bezerra | Eco#0745 \n\n"
        description += "*para mais informações acione o [desenvolvedor](https://www.devcbezerra.com/#contact)*"

        embed.description = description

        await ctx.send(embed=embed, components=[
            [Button(label="Convide-me", style=5,url="https://discord.com/api/oauth2/authorize?client_id=941379078475362344&permissions=8&scope=bot", custom_id="button1"), 
             Button(label="Donate",style=5,url="https://www.buymeacoffee.com/ecodj", custom_id="button2"),
             Button(label="Reportar Bug",style=5,url="https://www.devcbezerra.com/#contact", custom_id="button3")]
        ])

    async def send_cog_help(self, cog):
        ctx = self.context
        pre = self.clean_prefix

        embed = discord.Embed(
            color=self.color, timestamp=ctx.message.created_at, description=""
        )

        if await ctx.bot.is_owner(ctx.author):
            shown_commands = [command for command in cog.get_commands()]
        else:
            shown_commands = [
                command
                for command in cog.get_commands()
                if command.hidden == False and command.enabled == True
            ]

        if len(shown_commands) == 0:
            return await ctx.send("Sem comandos.")

        if cog.description:
            cog_help = cog.description
        else:
            cog_help = "Sem comandos fornecidos"

        embed.title = f"{cog.qualified_name}"
        embed.description += f"{cog_help}\nUse `{pre}help <comando>` para mais detalhes.\n\n**Comandos :** \n"

        for command in shown_commands:
            embed.description += f"▪︎ {pre}{command.qualified_name} "
            if command.signature:
                embed.description += f"{command.signature} \n"
            else:
                embed.description += "\n"

        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        await ctx.send(embed=embed)

    # Command Help
    async def send_command_help(self, command):
        ctx = self.context

        embed = discord.Embed(
            color=self.color,
            timestamp=ctx.message.created_at,
            description="",
        )

        if (
            command.hidden == True or command.enabled == False
        ) and await ctx.bot.is_owner(ctx.author) == False:
            return await ctx.send(
                f'Nenhum comando chamado "{command.qualified_name}" encontrado.'
            )

        if command.signature:
            embed.title = f"{command.qualified_name} {command.signature} \n"
        else:
            embed.title = f"{command.qualified_name}\n"

        embed.description = command.help or "Nenhuma descrição fornecida."

        if len(command.aliases) > 0:
            embed.description += "\nAbreviação : " + ", ".join(command.aliases)

        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        await ctx.send(embed=embed)

    # Group Help
    async def send_group_help(self, group):
        ctx = self.context
        pre = ctx.clean_prefix

        embed = discord.Embed(color=self.color, timestamp=ctx.message.created_at)

        if group.signature:
            embed.title = f"{group.qualified_name} {group.signature}"
        else:
            embed.title = group.qualified_name + " - group"

        embed.description = group.help or "Nenhuma descrição fornecida."
        embed.description += f"\nUse `{pre}help {group.qualified_name} <sub_command>` para mais detalhes do grupo de comandos. \n\n**Subcommands : **\n"

        if await ctx.bot.is_owner(ctx.author):
            group_commands = [command for command in group.commands]
            if len(group_commands) == 0:
                return await ctx.send("Este grupo não tem nenhum subcomando")
        else:
            group_commands = [
                command
                for command in group.commands
                if command.hidden == False and command.enabled == True
            ]

        if len(group_commands) == 0:
            return await ctx.send(f'Nenhum comando chamado "{group.qualified_name}" encontrado.')

        for command in group_commands:
            if command.signature:
                command_help = (
                    f"▪︎ {pre}{command.qualified_name} {command.signature} \n"
                )
            else:
                command_help = f"▪︎ {pre}{command.qualified_name} \n"

            embed.description += command_help

        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        await ctx.send(embed=embed)


class Help(commands.Cog):
    """Comandos de ajuda"""

    def __init__(self, client):
        self.client = client
        self.client._original_help_command = client.help_command
        client.help_command = HelpCog()
        client.help_command.cog = self

    def cog_unload(self):
        self.client.help_command = self.client._original_help_command


def setup(client):
    client.add_cog(Help(client))

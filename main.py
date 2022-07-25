import disnake
from disnake.ext import commands
from disnake.embeds import Embed

from keep_alive import keep_alive

import os
import dotenv
import colorama

import emojiset

COLOR = 0xf2ae1c


class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot # sets the client variable so we can use it in cogs
    
    @commands.Cog.listener()
    async def on_ready(self):
        # print with color blue
        print(f"{colorama.Fore.RED}[+] {colorama.Fore.BLUE}{self.bot.user.name} is online {colorama.Style.RESET_ALL}")
        pass

    @commands.command(help="Get latency in miliseconds", aliases=["p"])
    async def ping(self, ctx):
        """Show latency in milliseconds"""

        await ctx.send(
            embed=Embed(
                title="Bot is active",
                description=(
                    "**Latency:** "
                    + f"{round(self.bot.latency*1000, 3)} ms"
                ),
                color=COLOR
            )
        )
    
    @commands.command(help="Get information about server", aliases=["serverinfo"])
    async def server(self, ctx: commands.Context) -> None:
        """Shows you information about this server."""

        guild = ctx.guild

        offline_members = 0
        online_members = 0
        for member in guild.members:
            if member.status is not disnake.Status.offline:
                online_members += 1
            else:
                offline_members += 1

        embed = Embed(
            title=guild.name,
            colour=COLOR,
        )
        embed.set_thumbnail(guild.icon if guild.icon else 'https://cdn.discordapp.com/embed/avatars/1.png')
        embed.add_field(name="Total Members", value=guild.member_count, inline=False)
        embed.add_field(
            name="Members Status",
            value=f"⚪ Offline: {offline_members}\n🟢 Online: {online_members}",
            inline=False,
        )
        await ctx.send(embed=embed)
    
    @commands.command(help="Get information about user", aliases=["userinfo"])
    async def user(self, ctx: commands.Context, arg: disnake.Member = None):
        """Shows you information about yourself or the user given."""
        user = ctx.author if arg is None else arg
        
        embed = Embed(
            title=user.name + ' [BOT]' if user.bot else '',
            colour=COLOR,
        )
        
        embed.set_thumbnail(user.avatar if user.avatar else 'https://cdn.discordapp.com/embed/avatars/1.png')
        embed.add_field(name="ID", value=user.id, inline=False)
        embed.add_field(name="Status", value=user.status, inline=False)
        embed.add_field(name="Created At", value=disnake.utils.format_dt(user.created_at), inline=False)
        embed.add_field(name="Joined At", value=disnake.utils.format_dt(user.joined_at), inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(help="Add the word with reactions to the replied message")
    async def ew(self, ctx: commands.Context, *words):
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)

        # add reaction to meessage, the emoji of letter
        for letter in ''.join(words):
            await message.add_reaction(emojiset.get_emoji(letter))



intents = disnake.Intents.default()
intents.members = True
intents.presences = True
intents.messages = True
bot = commands.Bot(
    command_prefix=".",
    intents=intents
)
bot.add_cog(Main(bot))

# for f in os.listdir("./cogs"):
# 	if f.endswith(".py")
# 		client.load_extension("cogs." + f[:-3])

# keep_alive()
dotenv.load_dotenv()
bot.run(os.getenv("TOKEN"))

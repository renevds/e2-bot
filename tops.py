import discord
from discord.ext import commands
from countryinfo import CountryInfo
import pycountry
import requests
import json

class tops(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='self-destruct')
    async def self_destruct(self, ctx):
        await ctx.send('beep boop bop **explodes**')

    @commands.command(name='help')
    async def help(self, ctx):
        embed = discord.Embed(title="www.earth2stats.xyz", url="https://www.earth2stats.xyz/",
                              description="**List of commands:**", colour=0x7289da)

        leftcol = '\n**E2 country [Belgium, Be, ...]**\nShow stats for this country.'\
                  '\n**E2 topsold [15m/hour/24h]** \n Displays top 10 countries sold in given period.'\
                  '\n**E2 topinjected [15m/hour/24h]** \n Displays top 10 countries with most money spent on new tiles.'

        embed.set_thumbnail(url="https://www.earth2stats.xyz/static/main/img/small.png")
        embed.add_field(name="Commands", value=leftcol, inline=True)
        await ctx.send(embed=embed)

    @commands.command(name='topsold')
    async def topsold(self, ctx, arg1):
        valid = True
        if arg1 == '24h':
            title = '24 hours'
            urlend = 'h24'
        elif arg1 == 'hour':
            title = 'hour'
            urlend = 'h'
        elif arg1 == '15m':
            title = '15 minutes'
            urlend = 'm'
        else:
            embed = discord.Embed(title='Not a valid period', colour=0x7289da)
            await ctx.send(embed=embed)
            valid = False

        if valid:
            data = json.loads(requests.get('https://www.earth2stats.xyz/bot/toptiles/' + urlend).text)
            print(data)

            leftcol = ''
            rightcol = ''

            for idx, val in enumerate(data):
                leftcol += str(idx) + ". " + val[2] + '\n'
                rightcol += '+' + str(val[1]) + '\n'

            embed = discord.Embed(title="www.earth2stats.xyz", url="https://www.earth2stats.xyz/", description="**Top tiles sold in " + title +  "**", colour=0x7289da)
            embed.set_thumbnail(url="https://www.earth2stats.xyz/static/main/img/small.png")
            embed.add_field(name="Country", value=leftcol, inline=True)
            embed.add_field(name="Tiles", value=rightcol, inline=True)
            await ctx.send(embed=embed)

    @commands.command(name='topinjected')
    async def topinjected(self, ctx, arg1):
        valid = True
        if arg1 == '24h':
            title = '24 hours'
            urlend = 'h24'
        elif arg1 == 'hour':
            title = 'hour'
            urlend = 'h'
        elif arg1 == '15m':
            title = '15 minutes'
            urlend = 'm'
        else:
            embed = discord.Embed(title='Not a valid period', colour=0x7289da)
            await ctx.send(embed=embed)
            valid = False

        if valid:
            data = json.loads(requests.get('https://www.earth2stats.xyz/bot/toptiles/' + urlend).text)
            print(data)

            leftcol = ''
            rightcol = ''

            data.sort(key=lambda x: x[3], reverse=True)

            for idx, val in enumerate(data):
                leftcol += str(idx) + ". " + val[2] + '\n'
                rightcol += '+' + str(val[3]) + '$\n'

            embed = discord.Embed(title="www.earth2stats.xyz", url="https://www.earth2stats.xyz/",
                                  description="**Top money injected in last " + title + "**", colour=0x7289da)
            embed.set_thumbnail(url="https://www.earth2stats.xyz/static/main/img/small.png")
            embed.add_field(name="Country", value=leftcol, inline=True)
            embed.add_field(name="Tiles", value=rightcol, inline=True)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(tops(bot))

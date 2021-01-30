import discord
from discord.ext import commands
from countryinfo import CountryInfo
import pycountry
import requests
import json

class country(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='country')
    async def country(self, ctx, *args):
        argword = ' '.join(args)
        valid = True
        try:
            ct = pycountry.countries.search_fuzzy(argword)[0]
        except LookupError:
            valid = False
            embed = discord.Embed(title='Not a valid country', colour=0x7289da)
            await ctx.send(embed=embed)

        if valid:
            data = json.loads(requests.get('https://www.earth2stats.xyz/bot/country/' + ct.alpha_2).text)['stats']
            embed = discord.Embed(title="www.earth2stats.xyz", url="https://www.earth2stats.xyz/",
                                  description="**Stats for  " + ct.name + "**", colour=0x7289da)

            percent =  str(data['percentIncrease']) if data['percentIncrease'] < 0 else '+' + str(data['percentIncrease'])

            embed.add_field(name="Growth", value=percent + '%', inline=False)

            embed.add_field(name="Trade average", value=str(data['tradeAverage']) + '$/T', inline=False)

            embed.add_field(name="New tile price", value=str(data['value']) + '$', inline=False)

            embed.add_field(name="Total tiles sold", value=str(data['totalTilesSold']), inline=False)

            cls = 1
            if data['totalTilesSold'] > 500000:
                cls = 4
            elif data['totalTilesSold'] > 300000:
                cls = 3
            elif data['totalTilesSold'] > 100000:
                cls = 2

            embed.add_field(name="Class", value=str(cls), inline=False)

            embed.set_thumbnail(url='https://www.earth2stats.xyz/static/main/flags/' + ct.alpha_2 + '.png')

            await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(country(bot))

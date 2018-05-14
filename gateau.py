import discord, logging, configparser
import cake
from discord.ext import commands


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(name)s:%(message)s')

config = configparser.ConfigParser()
config.read('config.ini')
discord_key = str(config['auth']['discord'])
weather_key = str(config['auth']['weather'])

bot = commands.Bot(command_prefix='!', activity=discord.Game(name='Complex Form Active!'))
client = discord.Client()


@bot.command()
async def weather(ctx, arg):
    await ctx.send(cake.read_weather(arg, weather_key, 'conditions'))


@bot.command()
async def forecast(ctx, arg):
    await ctx.send(cake.read_weather(arg,weather_key, 'forecast'))


@bot.command()
async def define(ctx, arg):
    await ctx.send(cake.read_single_definition(arg))


@bot.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'true' in message.content.lower():
        await message.add_reaction('disc_true:445053952027787275')

    if 'same' in message.content.lower():
        await message.add_reaction('disc_same:445050329331925007')

    if 'nice' in message.content.lower():
        await message.add_reaction('disc_nice:445054000019275787')

    if 'real' in message.content.lower():
        await message.add_reaction('disc_real:445054014405738498')

    if 'cute' in message.content.lower():
        await message.add_reaction('disc_cute:445053981719265282')

    if 'rude' in message.content.lower():
        await message.add_reaction('disc_rude:445054026904633361')

    if 'bong' in message.content.lower():
        await message.add_reaction('snoop:445053916598763520')
    elif 'weed' in message.content.lower():
        await message.add_reaction('snoop:445053916598763520')

    if 'gateau' in message.content.lower():
        await message.channel.send(cake.random_response_line())

    await bot.process_commands(message)


bot.run(discord_key)

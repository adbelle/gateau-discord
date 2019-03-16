import discord, logging, configparser, googlemaps, cake, asyncio
from discord.ext import commands
from darksky import forecast


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(name)s:%(message)s')

config = configparser.ConfigParser()
config.read('config.ini')
discord_key = str(config['auth']['discord'])
weather_key = str(config['auth']['weather'])
maps_key = str(config['auth']['maps'])
gameplay = str(config['personality']['playing'])

bot = commands.Bot(command_prefix='!', activity=discord.Game(name=gameplay))
client = discord.Client()


@bot.command()
async def weather(ctx, arg):
    gmaps = googlemaps.Client(key=maps_key)
    gtarget = str(arg)
    geolat = str(gmaps.geocode(gtarget)[0]['geometry']['location']['lat'])
    geolng = str(gmaps.geocode(gtarget)[0]['geometry']['location']['lng'])
    geonam = str(gmaps.geocode(gtarget)[0]['formatted_address'])

    dsdata = forecast(weather_key, geolat, geolng)

    try:
        condout = str(dsdata.minutely.summary)
    except AttributeError:
        condout = str(dsdata.hourly.summary)
    try:
        tempout = str(dsdata.temperature) + "°F, " + str(round(float(dsdata.temperature) - 32 * 5 / 9, 2)) + " °C"
    except AttributeError:
        tempout = "Unknown."
    try:
        windout = str(dsdata.windBearing) + "° at " + str(dsdata.windSpeed) + " mph (" + str(round(dsdata.windSpeed * 1.609, 2)) + " km/h)"
    except AttributeError:
        windout = "Unknown."
    try:
        presout = str(dsdata.pressure) + " mb"
    except AttributeError:
        presout = "Unknown."
    try:
        visiout = str(dsdata.visibility) + " mi"
    except AttributeError:
        visiout = "Unknown."
    try:
        precout = str("{0:.0%}".format(float(dsdata.precipProbability)))
    except AttributeError:
        precout = "Unknown."
    try:
        strmout = str(dsdata.nearestStormDistance) + " mi"
    except AttributeError:
        strmout = "Unknown."
    respout = 'Requested by ' + str(ctx.message.author.display_name) + '. Query took ' + str(dsdata.response_headers['X-response-Time']) + ' to process.'

    config = configparser.ConfigParser()
    config.read('config.ini')
    try:
        discicon = str(config['weather'][str(dsdata.icon)])
    except AttributeError:
        discicon = str(config['weather']['clear-day'])

    footericon = str(ctx.message.author.avatar_url_as(format=None, static_format='png', size=1024))

    eheader = str(discicon + " Current Conditions for " + geonam)

    embed = discord.Embed(title=eheader, colour=discord.Colour(0x7289da), description=condout)

    embed.set_thumbnail(url="https://darksky.net/dev/img/attribution/poweredby-darkbackground.png")
    embed.set_footer(text=respout, icon_url=footericon)

    embed.add_field(name="<:Thermometer50:556351518387732481> Temperature", value=tempout, inline=True)
    embed.add_field(name="<:Wind:556349822014062618> Wind", value=windout, inline=True)
    embed.add_field(name="<:Cloud_Download:556356419780214785> Pressure", value=presout, inline=True)
    embed.add_field(name="<:Cloud_Download:556359914017128467> Visibility", value=visiout, inline=True)
    embed.add_field(name="<:Umbrella:556358404638113801> Precipitation Chance", value=precout, inline=True)
    embed.add_field(name="<:Compass:556359903976095765> Nearest Storm Distance", value=strmout, inline=True)

    await ctx.send(embed=embed)


@bot.command()
async def define(ctx, arg):
    await ctx.send(cake.read_single_definition(arg))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if 'true' in str(message.content.lower()).split():
        await message.add_reaction('disc_true:445053952027787275')

    if 'same' in str(message.content.lower()).split():
        await message.add_reaction('disc_same:445050329331925007')

    if 'nice' in str(message.content.lower()).split():
        await message.add_reaction('disc_nice:445054000019275787')

    if 'real' in str(message.content.lower()).split():
        await message.add_reaction('disc_real:445054014405738498')

    if 'cute' in str(message.content.lower()).split():
        await message.add_reaction('disc_cute:445053981719265282')

    if 'rude' in str(message.content.lower()).split():
        await message.add_reaction('disc_rude:445054026904633361')

    if 'bong' in str(message.content.lower()).split():
        await message.add_reaction('snoop:445053916598763520')
    elif 'weed' in str(message.content.lower()).split():
        await message.add_reaction('snoop:445053916598763520')

    if 'gateau' in str(message.content.lower()).split():
        if 'ilu' in str(message.content.lower()).split():
            await message.channel.send(str('ilu2 ' + message.author.mention))
        else:
            await message.channel.send(cake.random_response_line())

    await bot.process_commands(message)


bot.run(discord_key)

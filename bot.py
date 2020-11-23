import discord
import random
from discord import Embed
from discord.ext import commands, tasks
from itertools import cycle

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)

client = commands.Bot(command_prefix='!', intents=intents)
status = cycle(['Autor bota: Polixon', 'Nazwa bota: Bubuś'])


@client.event
async def on_ready():
    change_status.start()
    print('Bot jest gotowy!')

@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game(next(status)))

@client.event
async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(title="Nieprawidłowe polecenie", colour=discord.Colour.purple())
            embed.add_field(name="Nie znaleziono takiej komendy", value="Sprawdź listę komend wpisując !help", inline=False)
            await ctx.send(embed=embed)
            pass

#Ping
@client.command()
async def ping(ctx):
    embed = discord.Embed(title='Pong!', colour=discord.Colour.dark_blue())

    embed.add_field(name='Ping bota:', value=f'{round(client.latency * 1000)}ms')
    await ctx.send(embed=embed)
    pass

#8ball
@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['Napewno!',
                 'Zdecydowanie tak!',
                 'Bez wątpienia!',
                 'Tak, zdecydowanie',
                 'Możesz na tym polegać',
                 'Tak, widzę to',
                 'Najprawdopodobniej',
                 'Całkiem możliwe',
                 'Wszystko wskazuje, że tak',
                 'Ciężko stwierdzić',
                 'Spróbuj jeszcze raz',
                 'Zapytaj później',
                 'Lepiej teraz nie mówić',
                 'Nie mogę tego przewidzieć',
                 'Skoncentruj się i zapytaj ponownie',
                 'Nie licz na to',
                 'Moja odpowiedź to nie',
                 'Moje źródła mówią, że nie',
                 'Niezbyt dobrze to wygląda',
                 'Raczej niemożliwe']

    embed = discord.Embed(title=f'Pytanie: {question}', colour=discord.Colour.dark_blue())
    embed.add_field(name=f'Odpowiedź:', value=f'{random.choice(responses)}')
    await ctx.send(embed=embed)
    pass

#Clear
@client.command()
async def clear(ctx, amount: int):
    authorperms = ctx.author.permissions_in(ctx.channel)
    if authorperms.manage_messages:
        await ctx.channel.purge(limit=amount+1)
        embed = discord.Embed(title="Usunięto wiadomości", colour=discord.Colour.red())
        embed.add_field(name="Usunięto:", value=f"{amount} wiadomości", inline=False)
        embed.add_field(name="Przez", value=f"{ctx.author.mention}", inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f'{ctx.author.mention} Aby skorzystać z komendy "clear" musisz posiadać uprawnienia do zarządzania wiadomościami')
        pass

#Kick
@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    authorperms = ctx.author.permissions_in(ctx.channel)
    if authorperms.kick_members:
        await member.kick(reason=reason)
        embed = discord.Embed(title="Wyrzucono członka", colour=discord.Colour.red())
        embed.add_field(name="Wyrzucono:", value=f"{member.mention}", inline=False)
        embed.add_field(name="Przez", value=f"{ctx.author.mention}", inline=False)
        embed.add_field(name="Powód:", value=f"{reason}", inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send(
            f'{ctx.author.mention} Aby skorzystać z komendy "kick" musisz posiadać uprawnienia do wyrzucania członków!')
        pass

#Ban
@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    authorperms = ctx.author.permissions_in(ctx.channel)
    if authorperms.ban_members:
        await member.ban(reason=reason)
        embed = discord.Embed(title="Zbanowano członka", colour=discord.Colour.red())
        embed.add_field(name="Zbanowano:", value=f"{member.mention}", inline=False)
        embed.add_field(name="Przez", value=f"{ctx.author.mention}", inline=False)
        embed.add_field(name="Powód:", value=f"{reason}", inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f'{ctx.author.mention} Aby skorzystać z komendy "ban" musisz posiadać uprawnienia do banowania członków!')
        pass

#Unban
@commands.has_permissions(administrator=True)
@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

    if (user.name, user.discriminator) == (member_name, member_discriminator):
        await ctx.guild.unban(user)
        await ctx.send(f"{user} został odbanowany")
        pass

#IQ
@client.command(pass_context=True)
async def iq(ctx, *, member: discord.Member=None):
    if member:
        embed = discord.Embed(title=f"IQ {member.name} wynosi:", description=(random.randint(0, 200)), colour=discord.Colour.dark_blue())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"{ctx.author.name} Twoje IQ wynosi:", description=(random.randint(0, 200)), colour=discord.Colour.dark_blue())
        await ctx.send(embed=embed)
        pass

#Opinion
@client.command()
async def opinia(ctx, *, member: discord.Member=None):
    odpowiedzi = ['**Znienawidzony** 1/10',
                  '**Nielubiany** 2/10',
                  '**Gnębiony** 3/10',
                  '**Lubiany bo ma hajs** 4/10',
                  '**Ziomek, który pożyczy 2zł** 5/10',
                  '**Nawet lubiany** 6/10',
                  '**Jest spoko** 7/10',
                  '**Można mu ufać** 8/10',
                  '**Przyjacielski** 9/10',
                  '**Najlepsza osoba jaką można poznać** 10/10']

    if member:
        embed = discord.Embed(title="Opinia", colour=discord.Colour.red())
        embed.add_field(name=f"Średnia opinia dotycząca {member.name}:", value=f"{random.choice(odpowiedzi)}", inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Opinia", colour=discord.Colour.red())
        embed.add_field(name=f"Średnia opinia dotycząca {ctx.author.name}:", value=f"{random.choice(odpowiedzi)}", inline=False)
        await ctx.send(embed=embed)
        pass








#Errory
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Nieprawidłowa liczba", colour=discord.Colour.purple())
        embed.add_field(name="Aby skorzystać z komendy clear użyj ją w ten sposób:", value="!clear <liczba wiadomości do usunięcia>", inline=False)
        await ctx.send(embed=embed)
        pass

@_8ball.error
async def _8ball_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Nieprawidłowe pytanie", colour=discord.Colour.purple())
        embed.add_field(name="Aby skorzystać z komendy 8ball zadaj pytanie w ten sposób:", value="!8ball <pytanie>", inline=False)
        await ctx.send(embed=embed)
        pass

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Nieprawidłowy użytkownik", colour=discord.Colour.purple())
        embed.add_field(name="Aby skorzystać z komendy kick oznacz jakiego użytkownika chcesz wyrzucić w ten sposób:", value="!kick <oznaczenie użytkownika np. @Polixon#1111>", inline=False)
        await ctx.send(embed=embed)
        pass

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Nieprawidłowy użytkownik", colour=discord.Colour.purple())
        embed.add_field(name="Aby skorzystać z komendy ban oznacz jakiego użytkownika chcesz zbanować w ten sposób:", value="!ban <oznaczenie użytkownika np. @Polixon#1111>", inline=False)
        await ctx.send(embed=embed)
        pass

client.run('Nzc5MzA2OTQxNjE2NjE5NTQw.X7eoJQ.Y73htJDKQb1_77WAmHiNR7e_reE')


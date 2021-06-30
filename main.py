import discord
import os
from string import ascii_letters
from discord.ext import commands, tasks
from discord import DMChannel
import pandas as pd
from discord_slash import SlashCommand, SlashContext
import random
from random import randint
import asyncio
import string

intents = discord.Intents().all()
intents.members = True
intents.presences = True

client = commands.Bot(command_prefix='/', intents=intents)
TOKEN = 'ODQ5OTA3MzQxNjUwMjk2ODky.YLh_5A.3-CNeuYUy2hiGAGTDEb-X0EjQJY'
slash = SlashCommand(client, sync_commands=True)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("DeedHacks 2021"))
    print(f'Logged in as {client.user}.\n-----------')
    while True:
        await asyncio.sleep(10)
        with open("spam.txt", 'r+') as file:
            file.seek(0)
            file.truncate(0)
            file.close()


@client.event
async def on_message(message):
    counter = 0
    author_id = message.author.id
    channel = client.get_channel(849961738417078292)
    user = await client.fetch_user(f"{author_id}")
    with open('swearWords.txt', 'r') as file:
        word_list = file.read().splitlines()
    messageContent = message.content

    if message.author.id == 849907341650296892:
        return
    if len(messageContent) > 0:
        thing = messageContent
        for word in word_list:
            if (word in messageContent) or (word.upper() in messageContent) or (word.lower() in messageContent):
                await message.delete()
                e = discord.Embed(color=0x4b087a)
                await channel.send(user.mention + " said " + thing)
                e.add_field(name='Your message was removed!',
                            value='Any communication (verbal or written) considered hateful or discriminatory will '
                                  'not be tolerated during the hackathon. Please refer to our rules and guidelines to '
                                  'understand DEEDhacks’ values and the use of appropriate language. Sorry please '
                                  'refrain from saying ' + thing + ' or any profanity!')
                await DMChannel.send(user, embed=e)
    with open("spam.txt", 'r+') as file:
        for lines in file:
            if lines.strip("\n") == str(message.author.id):
                counter += 1

        file.writelines(f"{str(message.author.id)}\n")
        if counter > 10:
            await channel.send(user.mention + " Has been kicked from the server for spamming!")
            e = discord.Embed(color=0x4b087a)
            e.add_field(name='Sorry you have been kicked!',
                        value='As a hacker, you have violated the rules for inclusive language and behaviour. '
                              'Thus, the DEEDhacks team has decided to remove you from this hackathon. You now have '
                              'been kicked from the server DeedHacks due to spamming! An organizer will contact you '
                              'shortly, if you believe this is a mistake contact Sharanjit Virdi **(SharanjitV#2577)** '
                              'to further discuss this issue.')
            await DMChannel.send(user, embed=e)
            await asyncio.sleep(1)
            await message.guild.ban(message.author, reason="Spam")
            await asyncio.sleep(2)
            await message.guild.unban(message.author)
            print("oof")
    await client.process_commands(message)


@client.event
async def on_command_error(ctx, error):
    moderator = discord.utils.get(ctx.guild.roles, name="admins")
    if isinstance(error, commands.MissingRole):
        await ctx.send(ctx.author.mention + " you need " + moderator.mention + " to use this command!")


@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Unverified")  # finds the unverified role in the guild
    await member.add_roles(role)  # adds the unverified role to the member


def is_channel(ctx):
    return ctx.channel.id == 849957341872128014
#
# async def on_message(message):
#     await message.delete(message)
#


options = [
    {
        "name": "email",
        "description": "Use registered email for verification",
        "type": 3,
        "required": True
    }
]


@slash.slash(
    name="Verify",
    description="User Verification via email ",
    guild_ids=[849957341583376395],
    options=options)
@commands.check(is_channel)  # checks if the channel the command is being used in is the verify channel
async def verify(ctx: SlashContext, email: str):
    check_in = discord.utils.get(ctx.guild.channels, name="check-in-details")
    if ctx.channel.id == 849957341872128014:
        my_file = open("verified.txt", "r+")
        my_file2 = open("verified_ids.txt", "r+")
        verified_mails = my_file.readlines()
        verified_ids = my_file2.readlines()
        moderator = discord.utils.get(ctx.guild.roles, name="admins")
        Member_Details = pd.read_json('Members.json')
        Data1 = Member_Details.values.tolist
        Num1 = len(Data1()) - 1
        Mentor_Details = pd.read_json('Mentors.json')
        Data2 = Mentor_Details.values.tolist
        Num2 = len(Data2()) - 1

        unverified = discord.utils.get(ctx.guild.roles, name="Unverified")  # finds the unverified role in the guild
        if unverified in ctx.author.roles:  # checks if the user running the command has the un-verified role
            email = str(email)
            for Members in range(len(verified_mails)):
                if email == verified_mails[Members]:
                    used = True
                    break
                else:
                    used = False
            if not used:
                for Members in range(Num1):
                    if email == Data1()[Members][2]:
                        result1 = True
                        uid = Members
                        break
                    elif email != Data1()[Members][2]:
                        result1 = False
                if not result1:
                    for Members in range(Num2):
                        if email == Data2()[Members][2]:
                            result2 = True
                            uid2 = Members
                            break
                        elif email != Data2()[Members][2]:
                            result2 = False

            if used:
                await ctx.send(hidden=True, content="Sorry " + ctx.author.mention + " you can't use an email that is already used/verified!")
            elif result1:
                my_file.write("\n")
                my_file.write(email)
                my_file2.write("\n")
                my_file2.write(str(ctx.author))
                first_mame = Data1()[uid][0]
                last_name = Data1()[uid][1]
                verify_member = discord.utils.get(ctx.guild.roles, name="Member")
                e = discord.Embed(color=0x4b087a)
                await ctx.author.remove_roles(unverified)
                e.add_field(name='Thank you for verifying!',
                            value=' You now have access to the server. Welcome to DeedHacks '
                                  + first_mame + " " + last_name + '!')
                await ctx.author.send(embed=e)
                await ctx.author.add_roles(verify_member)  # adds the verified role to the member
                await ctx.send(ctx.author.mention + " Please check your discord inbox for more info!")
            elif result2:
                my_file.write("\n")
                my_file.write(email)
                my_file2.write("\n")
                my_file2.write(str(ctx.author))
                first_mame = Data2()[uid2][0]
                last_name = Data2()[uid2][1]
                verify_member = discord.utils.get(ctx.guild.roles, name="Mentor")
                e = discord.Embed(color=0x4b087a)
                await ctx.author.remove_roles(unverified)
                e.add_field(name='Thank you for verifying!',
                            value='Welcome to DEEDhacks 2021 '
                                  + first_mame + " " + last_name + '!' + 'DEEDhacks is '
                                                                         'organized by SFU Women in Engineering, '
                                                                         'but you can call us WiE! WiE SFU is '
                                                                         'committed to increasing representation and '
                                                                         'awareness of nonconforming groups in the '
                                                                         'engineering profession and is actively '
                                                                         'working to ensure that the engineering '
                                                                         'field is more diverse, inclusive and '
                                                                         'reflective of the future.  WiE hope you '
                                                                         'have a great experience at DEEDhacks this '
                                                                         'weekend and WiE encourage you to '
                                                                         'participate in the activities throughout '
                                                                         'the event!  Happy hacking!! Please read '
                                                                         'through our community guidelines in the '
                                                                         '#rules channel. By now you should have '
                                                                         'verified yourself in the #check-in-details '
                                                                         'channel with your email to access the rest '
                                                                         'of the server. If you are having issues, '
                                                                         'ping @admins for help!')
                await ctx.author.send(embed=e)
                await ctx.author.add_roles(verify_member)  # adds the verified role to the member
                await ctx.send(hidden=True, content=(ctx.author.mention + " Please check your discord inbox for more info!"))
            else:
                await ctx.send(hidden=True, content=("You may not be registered or something went wrong please contact the server moderators using "
                    + moderator.mention))

        else:
            await ctx.send(hidden=True, content='You are already verified! Contact the server moderators '
                           + moderator.mention + ' if you think there is a mistake.')
    else:
        await ctx.send("Wrong channel " + ctx.author.mention + ", please use the the " + check_in.mention)


@slash.slash(description="Provides information about WIE bot and DeedHacks!!", guild_ids=[849957341583376395])
async def information(ctx):
    if ctx.channel.id != 849957341872128014:
        await ctx.send(hidden=True, content="Hello, " + ctx.author.mention + ". I am WIE bot, and I wanna welcome you to DeedHacks!")
    else:
        await ctx.send(hidden=True, content="Wrong channel, please use a different channel " + ctx.author.mention)


@slash.slash(description="Provides information about how to verify yourself!", guild_ids=[849957341583376395])
async def verification(ctx):
    check_in = discord.utils.get(ctx.guild.channels, name="check-in-details")
    if ctx.channel.id == 849957341872128014:
        sponsor = discord.utils.get(ctx.guild.roles, name="Sponsor")
        moderator = discord.utils.get(ctx.guild.roles, name="admins")
        await ctx.send(hidden=True, content="Hello, " + ctx.author.mention + ". I am WIE bot, and I wanna welcome you to DeedHacks!" +
                       "\n" + "Here is some information on how to verify: " + "\n"
                       +
                       "Gain full access to this server by verifying yourself! Use the /verify command followed by the"
                       " email you used to apply to DeedHacks to verify yourself. All emails will get deleted when you "
                       "verify! Please note only hackers and mentors need to be verified. If you are an"
                       + sponsor.mention + ", reach out to the " + moderator.mention
                       + " in the " + check_in.mention + " channel "
                       + "directly for assistance or feel free to dm one of them!" + "\n" + "\n"
                       + "Example: /verify info@sfu.ca " + "\n\n"
                       + "If you have trouble verifying yourself, please ask the " + moderator.mention + "for help!")
    else:
        await ctx.send(hidden=True, content="Wrong channel " + ctx.author.mention + ", please use the the " + check_in.mention)


@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    channel = client.get_channel(payload.channel_id)
    if message_id == 858295134242996224:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        if payload.emoji.name == 'Git':
            role = discord.utils.get(guild.roles, name="Git")
        elif payload.emoji.name == 'Android':
            role = discord.utils.get(guild.roles, name="Android")
        elif payload.emoji.name == 'CC':
            role = discord.utils.get(guild.roles, name="CPP")
        elif payload.emoji.name == 'Webdev':
            role = discord.utils.get(guild.roles, name="Webdev")
        elif payload.emoji.name == 'Java':
            role = discord.utils.get(guild.roles, name="Java")
        elif payload.emoji.name == 'Linux':
            role = discord.utils.get(guild.roles, name="Linux")
        elif payload.emoji.name == 'Kotlin':
            role = discord.utils.get(guild.roles, name="Kotlin")
        elif payload.emoji.name == 'Py':
            role = discord.utils.get(guild.roles, name="Python")
        elif payload.emoji.name == 'JS':
            role = discord.utils.get(guild.roles, name="Javascript")
        elif payload.emoji.name == 'React':
            role = discord.utils.get(guild.roles, name="React JS")
        elif payload.emoji.name == 'swift':
            role = discord.utils.get(guild.roles, name="IOS")
        elif payload.emoji.name == 'GO':
            role = discord.utils.get(guild.roles, name="GOLang")
        elif payload.emoji.name == 'DB':
            role = discord.utils.get(guild.roles, name="Databases")
        elif payload.emoji.name == 'PHP':
            role = discord.utils.get(guild.roles, name="PHP")
        elif payload.emoji.name == 'DevOP':
            role = discord.utils.get(guild.roles, name="DevOPS")
        elif payload.emoji.name == 'Matlab':
            role = discord.utils.get(guild.roles, name="Matlab")
        elif payload.emoji.name == 'Customer':
            role = discord.utils.get(guild.roles, name="Customer Success")
        elif payload.emoji.name == 'Sales':
            role = discord.utils.get(guild.roles, name="Sales Development")
        elif payload.emoji.name == 'Management':
            role = discord.utils.get(guild.roles, name="Product Management")
        elif payload.emoji.name == 'Marketing':
            role = discord.utils.get(guild.roles, name="Product Marketing")
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role:
            member = payload.member
            if member:
                await member.add_roles(role)
                await member.send(f"{member.mention} You reacted with {payload.emoji} to receive the {role} role!")
            else:
                await channel.send(hidden=True, content="Error please mention a moderator!")
        else:
            print("rnf")
            await channel.send(hidden=True, content="Error please mention a moderator!")
    if message_id == 851249654829285377:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        if payload.emoji.name == 'Rose':
            role = discord.utils.get(guild.roles, name="Selfcare")

        if role:
            member = guild.get_member(payload.user_id)
            if member:
                await member.add_roles(role)
                await member.send(f"{member.mention} You reacted with {payload.emoji} to receive the {role} role!")
            else:
                await channel.send(hidden=True, content="Error please mention a moderator!")
        else:
            await channel.send(hidden=True, content="Error please mention a moderator!")


@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    channel = client.get_channel(payload.channel_id)
    if message_id == 858295134242996224:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        if payload.emoji.name == 'Git':
            role = discord.utils.get(guild.roles, name="Git")
        elif payload.emoji.name == 'Android':
            role = discord.utils.get(guild.roles, name="Android")
        elif payload.emoji.name == 'CC':
            role = discord.utils.get(guild.roles, name="CPP")
        elif payload.emoji.name == 'Webdev':
            role = discord.utils.get(guild.roles, name="Webdev")
        elif payload.emoji.name == 'Java':
            role = discord.utils.get(guild.roles, name="Java")
        elif payload.emoji.name == 'Linux':
            role = discord.utils.get(guild.roles, name="Linux")
        elif payload.emoji.name == 'Kotlin':
            role = discord.utils.get(guild.roles, name="Kotlin")
        elif payload.emoji.name == 'Py':
            role = discord.utils.get(guild.roles, name="Python")
        elif payload.emoji.name == 'JS':
            role = discord.utils.get(guild.roles, name="Javascript")
        elif payload.emoji.name == 'React':
            role = discord.utils.get(guild.roles, name="React JS")
        elif payload.emoji.name == 'swift':
            role = discord.utils.get(guild.roles, name="IOS")
        elif payload.emoji.name == 'GO':
            role = discord.utils.get(guild.roles, name="GOLang")
        elif payload.emoji.name == 'DB':
            role = discord.utils.get(guild.roles, name="Databases")
        elif payload.emoji.name == 'PHP':
            role = discord.utils.get(guild.roles, name="PHP")
        elif payload.emoji.name == 'DevOP':
            role = discord.utils.get(guild.roles, name="DevOPS")
        elif payload.emoji.name == 'Matlab':
            role = discord.utils.get(guild.roles, name="Matlab")
        elif payload.emoji.name == 'Customer':
            role = discord.utils.get(guild.roles, name="Customer Success")
        elif payload.emoji.name == 'Sales':
            role = discord.utils.get(guild.roles, name="Sales Development")
        elif payload.emoji.name == 'Management':
            role = discord.utils.get(guild.roles, name="Product Management")
        elif payload.emoji.name == 'Marketing':
            role = discord.utils.get(guild.roles, name="Product Marketing")
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role:
            member = guild.get_member(payload.user_id)
            if member:
                await member.remove_roles(role)
                await member.send(f"{member.mention} You reacted with {payload.emoji} to remove the {role} role!")
            else:
                await channel.send(hidden=True, content="Error please mention a moderator!")
        else:
            await channel.send(hidden=True, content="Error please mention a moderator!")
    if message_id == 851249654829285377:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        if payload.emoji.name == 'Rose':
            role = discord.utils.get(guild.roles, name="Selfcare")

        if role:
            member = guild.get_member(payload.user_id)
            if member:
                await member.remove_roles(role)
                await member.send(f"{member.mention} You reacted with {payload.emoji} to remove the {role} role!")
            else:
                await channel.send(hidden=True, content="Error please mention a moderator!")
        else:
            await channel.send(hidden=True, content="Error please mention a moderator!")


@client.command()
@commands.has_role("admins")
async def care_role(ctx):
    embedVar = discord.Embed(title="Gotta Care for yourself!!",
                             description="Hey there hackers! Please react to the following message with the correct emoji to receive the self-care role!",
                             color=0x4b087a)
    await ctx.channel.send(embed=embedVar)
    await ctx.send(hidden=True, content="The react to the rose below now! \n"
                   + "<:Rose:851247887996551218>: For those who care about themselves!! \n")


@client.command()
@commands.has_role("admins")
async def clear(ctx):
    admin = 849961738417078292
    role = 849957342317117464
    care = 851188943852798003
    current = ctx.channel.id
    if current == admin or current == role or current == care:
        await ctx.message.delete()
        await ctx.channel.send("Can't use this command here!")
    else:
        await ctx.channel.purge()


@client.command()
@commands.has_role("admins")
async def mroles(ctx):
    embedVar = discord.Embed(title="Mentor roles",
                             description="Hey there mentors! Please react to the following message with the correct emojis to receive roles!",
                             color=0x4b087a)
    await ctx.channel.send(embed=embedVar)
    await ctx.send(content="The roles are as follows: \n"
                   + "<:Linux:851189700533944341>: For Linux Mentors \n"
                   + "<:Git:851163737640534047>: For Git Mentors \n"
                   + "<:Android:851163699556122723>: For Android Studio Mentors \n"
                   + "<:Kotlin:851190168216272958>: For Kotlin Mentors \n"
                   + "<:Swift:851189669563859014>: For Swift (IOS dev) Mentors \n"
                   + "<:CC:851185868420284427>: For C/C++ Mentors \n"
                   + "<:Java:851190681477185557>: For Java Mentors \n"
                   + "<:Py:851189250619605053>: For Python Mentors \n"
                   + "<:JS:851189226485710858>: For Javascript Mentors \n"
                   + "<:React:851190328148623370>: For React JS Mentors \n"
                   + "<:Webdev:851189188216487956>: For Webdev (HTML5 and CSS) Mentors \n"
                   + "<:DB:851210525954015272>: For Database Mentors \n"
                   + "<:DevOP:851210630353518592>: For DevOPS Mentors \n"
                   + "<:GO:851210558091034676>: For GO Lang Mentors \n"
                   + "<:PHP:851210594765111326>: For PHP Mentors \n"
                   + "<:Matlab:858291678620286976>: For Matlab Mentors \n"
                   + "<:Marketing:858291788942016532>: For Product Marketing Mentors \n"
                   + "<:Sales:858291710856396830>: For Sales Development Mentors \n"
                   + "<:Management:858291737943343144>: For Product Management Mentors \n"
                   + "<:Customer:858291902696783872>: For Customer Success Mentors \n")


@tasks.loop(hours=1)
async def messages():
    channel = client.get_channel(851188943852798003)
    Quotes_list = open('Quotes.txt', 'r+')
    Quotes = Quotes_list.read().splitlines()
    Quotes_using = Quotes
    size = len(Quotes_using) - 1
    choice = randint(0, size)
    await channel.send('Hey! <@&851236665339150336>')
    embedVar = discord.Embed(title="Self-care Time!!",
                             description="Hey there hackers! " + str(Quotes_using[choice]),
                             color=0x4b087a)
    await channel.send(embed=embedVar)
    used = Quotes_using[choice]
    Quotes_using.remove(used)
    Quotes_list.seek(0)
    Quotes_list.truncate(0)
    Quotes_list.close()
    re_write = open('Quotes.txt', 'w')
    for quote in Quotes:
        re_write.write(quote + "\n")
    re_write.close()


@client.command()
@commands.has_role("admins")
async def start(ctx):
    messages.start()
    await ctx.send(hidden=True, content="Starting self-care now!")


@client.command()
@commands.has_role("admins")
async def stop(ctx):
    messages.stop()
    await ctx.send(hidden=True, content="Stopping self-care now!")


@slash.slash(
    name="Care",
    description="Start or Stop Self-care comments!",
    guild_ids=[849957341583376395],
    options=[
        {
            "name": "do",
            "description": "Use True to start and False to stop!",
            "type": 5,
            "required": False
        }
    ])
async def self_care(ctx: SlashContext, do: bool):
    # admin_chat = discord.utils.get(ctx.guild.channels, name="admin-chat")
    if ctx.channel.id == 849961738417078292:
        if do:
            messages.start()
            await ctx.send(hidden=True, content="Starting")
        if not do:
            messages.cancel()
            await ctx.send(hidden=True, content="Stopping")
    else:
        await ctx.send(hidden=True, content="Wrong channel " + ctx.author.mention + " only admins can use this command!")


@slash.slash(description="Provides information about self-care function!!", guild_ids=[849957341583376395])
async def caring(ctx):
    if ctx.channel.id == 849961738417078292:
        await ctx.send(hidden=True, content="Hello, " + ctx.author.mention + ". I am WIE bot, and to start self care simply use the /care do"
                                                        "function! Make sure you choose True or False!\n"
                                                        "True begins hourly self-care messages and False stop them!")
    else:
        await ctx.send(hidden=True, content="Wrong channel, only admins can use this command " + ctx.author.mention)


@slash.slash(
    name="8ball",
    description="Ask a question and test you fortune!",
    guild_ids=[849957341583376395],
    options=[
        {
            "name": "question",
            "description": "Your question",
            "type": 3,
            "required": True
        }
    ])
async def _8ball(ctx: SlashContext, question):
    channel = discord.utils.get(ctx.guild.channels, name="admin-chat")
    responses = ["As I see it, yes",
                 "Ask again later",
                 "Better not tell you now",
                 "Cannot predict now",
                 "Concentrate and ask again",
                 "Don’t count on it",
                 "It is certain",
                 "It is decidedly so",
                 "Most likely",
                 "My reply is no",
                 "My sources say no",
                 "Outlook not so good",
                 "Outlook good",
                 "Reply hazy, try again",
                 "Signs point to yes",
                 "Very doubtful",
                 "Without a doubt",
                 "Yes",
                 "Yes – definitely",
                 " You may rely on it"
                 ]
    if set(question).difference(ascii_letters):
        await ctx.send(hidden=True,
                       content=f"{ctx.author.mention} Asked: {question}\nFortune: **{random.choice(responses)}**")
    else:
        await ctx.send(hidden=True, content="Error Occurred. Please make sure you have asked a proper question!")
        await channel.send(f"{ctx.author} experienced a error using 8ball.")


@slash.slash(description="Flip a coin!", guild_ids=[849957341583376395])
async def coinflip(ctx):
    coin = random.randint(0, 1)
    if coin > 0:
        await ctx.send(hidden=True, content=f"{ctx.author.mention} You flipped: **Heads**!")
    else:
        await ctx.send(hidden=True, content=f"{ctx.author.mention} You flipped: **Tails**!")

client.run(TOKEN)  # runs the bot

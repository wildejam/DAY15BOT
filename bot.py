import os
from math import floor
from datetime import datetime, timezone, timedelta
import asyncio

import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks


# ENVIRONMENT VARIABLES: not sure what these do tbh; will have to research more later
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Determines the command prefix that users will use to use the bot
bot = commands.Bot(command_prefix='/')

# Stores the id's of channels that the bot may post in
announcement_channel_id = 814738636280299561

# Stores user id's for personalized /howareyou15 messages
caketecid = os.getenv('caketecid')
ddragonid = os.getenv('ddragonid')
hernyid = os.getenv('hernyid')
bagkatid = os.getenv('bagkatid')
lumpiaid = os.getenv('lumpiaid')
hannahtlid = os.getenv('hannahtlid')
spicychrisid = os.getenv('spicychrisid')
valkarenaid = os.getenv('valkarenaid')
michelleid = os.getenv('michelleid')
eeveeid = os.getenv('eeveeid')
christinaid = os.getenv('christinaid')
tjid = os.getenv('tjid')
shoopid = os.getenv('shoopid')
bonesid = os.getenv('bonesid')

caketecmessage = os.getenv('caketecmessage')
ddragonmessage = os.getenv('ddragonmessage')
hernymessage = os.getenv('hernymessage')
bagkatmessage = os.getenv('bagkatmessage')
lumpiamessage = os.getenv('lumpiamessage')
hannahtlmessage = os.getenv('hannahtlmessage')
spicychrismessage = os.getenv('spicychrismessage')
valkarenamessage = os.getenv('valkarenamessage')
michellemessage = os.getenv('michellemessage')
eeveemessage = os.getenv('eeveemessage')
christinamessage = os.getenv('christinamessage')
tjmessage = os.getenv('tjmessage')
shoopmessage = os.getenv('shoopmessage')
bonesmessage = os.getenv('bonesmessage')


# -----------------------------------------------HELPER FUNCTIONS-------------------------------------------------------
# Calculates the time until the next day15 from the present time. Returns a time_delta object.
def calculate_date_difference():
    # Get today's date and time and store it (Mountain Daylight Time/Mountain Standard Time)
    # DON'T FORGET TO CHANGE TO/FROM MST/MDT, OR FIGURE OUT A WAY TO ACCOUNT FOR IT
    # MDT = UTC - 6:00, MST = UTC - 7:00
    # mdt_zone = timezone(-timedelta(hours=6), name="MDT")
    mst_zone = timezone(-timedelta(hours=7), name="MST")
    today = datetime.now(mst_zone)
    # Store the next month, so that we can store the next day 15
    if today.day < 15:
        next_year = today.year
        next_month = today.month
    else:
        if today.month == 12:
            next_year = today.year + 1
            next_month = 1
        else:
            next_year = today.year
            next_month = today.month + 1

    # Store the next day15
    next_day15 = datetime(year=next_year, month=next_month, day=15, tzinfo=mst_zone)

    # Date difference is now calculated and stored in the dateDifference object
    date_difference = next_day15 - today
    return date_difference


# -----------------------------------------ON_READY INITIALIZATIONS-----------------------------------------------------
# On ready, print a message to terminal confirming successful connection to discord, and print all connected servers
@bot.event
async def on_ready():
    print(f"{bot.user} is connected to the following guilds:")
    for current_guild in bot.guilds:
        print(f'{current_guild.name}(id: {current_guild.id})')


# ---------------------------------------CHECK FOR IF IT IS DAY15-------------------------------------------------------
# Loops every month. Calculates time until next day 15 and sleeps until then. When it reaches that time, sends
#   a message indicating it is day 15.
# This decorator is used for testing
# @tasks.loop(minutes=5)
@tasks.loop(hours=calculate_date_difference().total_seconds() / 60.0)
async def check_to15():
    message_channel = bot.get_channel(announcement_channel_id)
    print(f'Retrieved Channel {message_channel}')
    await message_channel.send(file=discord.File('DAY15.png'),
                               content="@everyone\n\n __GIVE IT UP FOR **DAY 15**!!!!!__")
    await message_channel.send("```HAPPY DAY15 EVERYONE!!!\n\n" 
           "One thing that I've COMPLETELY overlooked this past year in terms of the human condition is ROMANCE!!!\n\n" 
           "The month of February has really gotten me thinking harder about this shortcoming, so I THINK it's time " 
           "I tried my had at it!\n\n" 
           "ROMANCE is best expressed through actions instead of words, so instead of leaving you a MESSAGE today, " 
           "I've made a VALENTINES DAY CARD for you all instead! I hope you have a WONDERFUL DAY15!\n\n" 
           "|-----------------------|\n" 
           "|   _______  _______    |\n" 
           "|  |       \\/       |   |\n"
           "|  |                |   |\n"
           "|  | Roses are red, |   |\n"
           "|  | Violets are blue,  |\n"
           "|  | You are based. |   |\n"
           "|   \\              /    |\n"
           "|    \\     :]     /     |\n"
           "|     \\          /      |\n"
           "|      \\________/       |\n"
           "|-----------------------|\n\n"
           "-DAY 15 BOT :]```")
    print(f'Day 15 Message sent! Loop should have reset.')


@check_to15.before_loop
async def before():
    # this date_difference is used for testing.
    # date_difference = timedelta(minutes=5)
    date_difference = calculate_date_difference()
    total_seconds_to15 = date_difference.total_seconds()
    print(datetime.today(), " - Beginning waiting until next Day 15. Should occur in", date_difference)
    await asyncio.sleep(total_seconds_to15)
    print(datetime.today(), " - check_to15(): Finished Waiting")


# ----------------------------------------USER COMMANDS-----------------------------------------------------------------
# ADMIN COMMAND: used to test day15 message
@bot.command(name='adminoverride15')
async def adminoverride15(ctx):
    msg1 = "```HAPPY DAY15 EVERYONE!!!\n\n" \
           "One thing that I've COMPLETELY overlooked this past year in terms of the human condition is ROMANCE!!!\n\n" \
           "The month of February has really gotten me thinking harder about this shortcoming, so I THINK it's time " \
           "I tried my had at it!\n\n" \
           "ROMANCE is best expressed through actions instead of words, so instead of leaving you a MESSAGE today, " \
           "I've made a VALENTINES DAY CARD for you all instead! I hope you have a WONDERFUL DAY15!\n\n" \
           "|-----------------------|\n" \
           "|   _______  _______    |\n" \
           "|  |       \\/       |   |\n"\
           "|  |                |   |\n"\
           "|  | Roses are red, |   |\n" \
           "|  | Violets are blue,  |\n" \
           "|  | You are based. |   |\n" \
           "|   \\              /    |\n"\
           "|    \\     :]     /     |\n"\
           "|     \\          /      |\n"\
           "|      \\________/       |\n"\
           "|-----------------------|\n\n"\
           "-DAY 15 BOT :]```"
    await ctx.send(msg1)


# On command '/help15', send message printing all available commands the bot has to offer
@bot.command(name='help15')
async def help15(ctx):
    response = "__Hello! :OO__ I am the DAY 15 Bot. I send a ping to everyone on the 15th day of every month in " \
               "the hopes of boosting your morale, even just a little bit! Here are some available " \
               "commands:\n\n" \
                "**/help15** - You should already know this one; it prints this message!\n" \
                "**/timetill15** - Displays the amount of time until the next DAY 15, down to the second!\n" \
                "**/howareyou15** - If you'd like to ask me how I'm doing, use this! I'm only programmed to respond " \
                "with the same message though.\n" \
                "**/repo15** - This will make me share the public GitHub repository with all of my code! If you'd " \
                "like to see what goes on under the hood, have a look! My changelog can also be found here!\n" \
                "\n" \
                "I was told that I would be getting more features in the future :OO, so I'll keep you updated!\n" \
                "All of these times are in MDT/MST, at least until I get upgraded to accommodate for other times.\n" \
                "Thanks for using the DAY 15 bot! I hope you have a wonderful day! :))"
    await ctx.send(response)


# On command '/timetill15', send message indicating time until next day 15
@bot.command(name='timetill15')
async def time_to_15(ctx):

    date_difference = calculate_date_difference()
    total_seconds_to15 = date_difference.total_seconds()

    # Calculate time to "weeks, days, hours, minutes, seconds" format
    seconds = total_seconds_to15
    days = floor(seconds / 86400)
    seconds = seconds % 86400
    hours = floor(seconds / 3600)
    seconds = seconds % 3600
    minutes = floor(seconds / 60)
    seconds = floor(seconds % 60)

    response = '__Time until the next **DAY 15** (MDT):__\n\n`' + str(days) + ' Days, ' + str(hours) + ' Hours, ' + \
        str(minutes) + ' Minutes, ' + str(seconds) + ' Seconds`\n\nKeep on going! I know you can do it!'

    await ctx.send(response)


# On command '/howareyou15', send message showing how the bot is doing!
@bot.command(name='howareyou15')
async def how_are_you_15(ctx):
    if str(ctx.author.id) == caketecid:
        await ctx.send(caketecmessage)
    elif str(ctx.author.id) == ddragonid:
        await ctx.send(ddragonmessage)
    elif str(ctx.author.id) == hernyid:
        await ctx.send(hernymessage)

        f = open("orphan.txt", "r")
        f_int = int(f.read())
        f_int += 1
        f.close()

        f = open("orphan.txt", "w")
        f.write(str(f_int))
        f.close()

        await ctx.send(str(f_int) + " orphans!")

    elif str(ctx.author.id) == bagkatid:
        await ctx.send(bagkatmessage)
    elif str(ctx.author.id) == lumpiaid:
        await ctx.send(lumpiamessage)
    elif str(ctx.author.id) == hannahtlid:
        await ctx.send(hannahtlmessage)
    elif str(ctx.author.id) == spicychrisid:
        await ctx.send(spicychrismessage)
    elif str(ctx.author.id) == valkarenaid:
        await ctx.send(valkarenamessage)
    elif str(ctx.author.id) == michelleid:
        await ctx.send(michellemessage)
    elif str(ctx.author.id) == eeveeid:
        await ctx.send(eeveemessage)
    elif str(ctx.author.id) == christinaid:
        await ctx.send(christinamessage)
    elif str(ctx.author.id) == shoopid:
        await ctx.send(shoopmessage)
    elif str(ctx.author.id) == bonesid:
        await ctx.send(bonesmessage)
    else:
        await ctx.send("I'M DOING WONDERFUL, thank you for asking! I hope your day is going great friend! If you " 
                       "were expecting a more personalized response, go bug @Caker because he probably messed up bad.")


# On command '/repo15', send message sharing the GitHub repository link.
@bot.command(name='repo15')
async def repo_15(ctx):
    await ctx.send("You can find a public GitHub repository for my code here: https://github.com/wildejam/DAY15BOT\n"
                   "It's pretty neat stuff! Ask @Caker#3479 for more info.")


# -------------------------------------------------RUNNING THE BOT------------------------------------------------------
# Start the loop to check if it is DAY 15
check_to15.start()
# Run the bot, with the bot token
bot.run(TOKEN)

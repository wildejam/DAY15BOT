import os
from math import floor
from datetime import datetime, timezone, timedelta
import asyncio
import requests
import io
import aiohttp
import random

import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks


# ENVIRONMENT VARIABLES: not sure what these do tbh; will have to research more later
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
UNSPLASHKEY = os.getenv('UNSPLASH_TOKEN')
GOOGLEKEY = os.getenv('GOOGLE_KEY')

# Determines the command prefix that users will use to use the bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

# Stores the id's of channels that the bot may post in
announcement_channel_id = 814738636280299561

# NEWDOG SEARCH RESULTS: stores JSON objects which contain Google images for newdog commands
# rock ferret leon guy animegirl
newdogjson = {
    "cat": [{},0],
    "lizard": [{},0],
    "rock": [{},0], 
    "ferret": [{},0],  
    "leon": [{},0],  
    "guy": [{},0],   
    "animegirl": [{},0],
    "bird": [{},0],
    "hgtv": [{},0],
    "cryptid": [{},0],
    "rat": [{},0],
    "otter": [{},0],
    "car": [{},0],
    "dragon": [{},0]
}

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
nuiid = os.getenv('nuiid')
bingleid = os.getenv('bingleid')

caketecmessage = os.getenv('caketecmessage')
ddragonmessage = os.getenv('ddragonmessage')
hernymessage = os.getenv('hernymessage')
bagkatmessage = os.getenv('bagkatmessage')
lumpiamessage = os.getenv('lumpiamessage')
hannahtlmessage = os.getenv('hannahtlmessage')
spicychrismessage = os.getenv('spicychrismessage')
valkarenamessage = os.getenv('valkarenamessage')
michellemessage = os.getenv('michellemessage')
# eeveemessage = os.getenv('eeveemessage')
christinamessage = os.getenv('christinamessage')
tjmessage = os.getenv('tjmessage')
shoopmessage = os.getenv('shoopmessage')
bonesmessage = os.getenv('bonesmessage')
nuimessage = os.getenv('nuimessage')
binglemessage = os.getenv('binglemessage')

# used for /howareyou15 3/14/26
random_tiers = ["S TIER", "A tier", "B tier", "C tier", "D tier", "F tier"]


# -----------------------------------------------HELPER FUNCTIONS-------------------------------------------------------
# Calculates the time until the next day15 from the present time. Returns a time_delta object.
def calculate_date_difference():
    # Get today's date and time and store it (Mountain Daylight Time/Mountain Standard Time)
    # DON'T FORGET TO CHANGE TO/FROM MST/MDT, OR FIGURE OUT A WAY TO ACCOUNT FOR IT
    # MDT = UTC - 6:00, MST = UTC - 7:00
    mdt_zone = timezone(-timedelta(hours=6), name="MDT")
    # mst_zone = timezone(-timedelta(hours=7), name="MST")
    today = datetime.now(mdt_zone)
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
    next_day15 = datetime(year=next_year, month=next_month, day=15, tzinfo=mdt_zone)

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
    print("ANNOUNCEMENT CHANNEL: " + str(announcement_channel_id))
    message_channel = await bot.fetch_channel(announcement_channel_id)
    print(f'Retrieved Channel {message_channel}')
    await message_channel.send(file=discord.File('DAY15.png'),
                               content="@everyone\n\n __GIVE IT UP FOR **DAY 15**!!!!!__")
    await message_channel.send("```"
        "\"Suggestion15: tierlist the server members unironically. be ruthless. give us some hottake thats like \"Shoop is F tier and Snowball Bot is S tier\"\"\n\n"
        "Happy March everyone! I hope that your pillows remain cold and your chairs remain un-squeaky!\n"
        "A friendly reminder this month that the world you see in your day-to-day truly is filled with wonderful people who have genuine kindness and compassion in their heart!"
        "It is easy to succumb to nihilism and despair when you see it thrown into your face twenty-four seven, "
        "but that view is a colossal distortion of how a lot of the world is!"
        "There are many, many, many great souls out there linked together in an invisible solidarity to pursue a better world, and even though it is easy to miss, you truly can find them everywhere. You just might need to go out and look.\n\n"
        "Never forget that in your pursuit of a better world, there are countless who unknowingly stand alongside you. I, for one, am happy to be one of them! \n"
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
    if str(ctx.author.id) == caketecid:
        # message_channel = bot.get_channel(announcement_channel_id)
        # print(f'Retrieved Channel {message_channel}')
        await ctx.send(file=discord.File('DAY15.png'),
                                content="@everyone\n\n __GIVE IT UP FOR **DAY 15**!!!!!__")
        await ctx.send("```"
        "\"Suggestion15: tierlist the server members unironically. be ruthless. give us some hottake thats like \"Shoop is F tier and Snowball Bot is S tier\"\"\n\n"
        "Happy March everyone! I hope that your pillows remain cold and your chairs remain un-squeaky!\n"
        "A friendly reminder this month that the world you see in your day-to-day truly is filled with wonderful people who have genuine kindness and compassion in their heart!"
        "It is easy to succumb to nihilism and despair when you see it thrown into your face twenty-four seven, "
        "but that view is a colossal distortion of how a lot of the world is!"
        "There are many, many, many great souls out there linked together in an invisible solidarity to pursue a better world, and even though it is easy to miss, you truly can find them everywhere. You just might need to go out and look.\n\n"
        "Never forget that in your pursuit of a better world, there are countless who unknowingly stand alongside you. I, for one, am happy to be one of them! \n"
        "-DAY 15 BOT :]```"
        ) 
        print(f'Day 15 Message sent! Loop should have reset.')
    else:
        await ctx.send("Nice try! >:] I was EXPLICITLY TOLD to not let anyone but jam use this command! >:]")


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
        await ctx.send(random_tiers[random.randint(0, 5)])
        await ctx.send(file=discord.File('club-penguin-mop.gif'))
    elif str(ctx.author.id) == ddragonid:
        await ctx.send(random_tiers[random.randint(0, 5)])
    elif str(ctx.author.id) == hernyid:
        await ctx.send(random_tiers[random.randint(0, 5)])

        f = open("orphan.txt", "r")
        f_int = int(f.read())
        f_int += 1
        f.close()

        f = open("orphan.txt", "w")
        f.write(str(f_int))
        f.close()

        await ctx.send(str(f_int) + " orphans!")

    elif str(ctx.author.id) == bagkatid:
        await ctx.send(random_tiers[random.randint(0, 5)])
    elif str(ctx.author.id) == lumpiaid:
        await ctx.send(random_tiers[random.randint(0, 5)])
    elif str(ctx.author.id) == hannahtlid:
        await ctx.send(random_tiers[random.randint(0, 5)])
    elif str(ctx.author.id) == spicychrisid:
        await ctx.send(random_tiers[random.randint(0, 5)])
    elif str(ctx.author.id) == valkarenaid:
        await ctx.send(random_tiers[random.randint(0, 5)])
    # elif str(ctx.author.id) == eeveeid:
    #     await ctx.send(eeveemessage)
    elif str(ctx.author.id) == christinaid:
        await ctx.send(random_tiers[random.randint(0, 5)])
    elif str(ctx.author.id) == shoopid:
        await ctx.send(random_tiers[random.randint(0, 5)])
    elif str(ctx.author.id) == bonesid:
        await ctx.send(random_tiers[random.randint(0, 5)])
    elif str(ctx.author.id) == tjid:
        await ctx.send(random_tiers[random.randint(0, 5)])
    elif str(ctx.author.id) == nuiid:
        await ctx.send(random_tiers[random.randint(0, 5)])
    elif str(ctx.author.id) == bingleid:
        await ctx.send(random_tiers[random.randint(0, 5)])

    else:
        await ctx.send("I'M DOING WONDERFULLY, thank you for asking! I hope your day is going great friend!")


# On command '/repo15', send message sharing the GitHub repository link.
@bot.command(name='repo15')
async def repo_15(ctx):
    await ctx.send("You can find a public GitHub repository for my code here: https://github.com/wildejam/DAY15BOT\n"
                   "It's pretty neat stuff! Ask @Caker#3479 for more info.")

# On command '/suggestion15', send acknowledgement message.
@bot.command(name='suggestion15')
async def suggestion15(ctx):
    await ctx.send("Duly noted! Thank you for your suggestion!")

# On command '/newdog15', fetch dog image from dog api and post.
@bot.command(name='newdog15')
async def new_dog_15(ctx):
    api_data = requests.get('https://dog.ceo/api/breeds/image/random')
    dog_data = api_data.json()

    async with aiohttp.ClientSession() as session:
        async with session.get(dog_data['message']) as resp:
            if dog_data['status'] != 'success':
                return await ctx.send('Hmm, it looks like something went wrong :(( Sorry!! I\'ll get @CakeTEC on it!')
            data = io.BytesIO(await resp.read())
            await ctx.send("Powered by DOG API, which can be found here:" + "<" + "https://dog.ceo/dog-api/" + ">")
            await ctx.send(file=discord.File(data, 'dog.jpg'))


# On command '/newcat15', fetch cat image from unsplash api and post.
@bot.command(name='newcat15')
async def new_cat_15(ctx):

    searchTerm = "cat"

    # first, check if an api call needs to be made, and perform one if necessary. update json file accordingly, and set index to 0.
    if (newdogjson['cat'][0] == {} or newdogjson['cat'][1] >= 10):
        api_data = requests.get('https://customsearch.googleapis.com/customsearch/v1?key=' + GOOGLEKEY + '&cx=a22729bb04f1e4c95&q=' + searchTerm + '&searchType=image&start=' + str(random.randint(0,90)))
        newdogjson['cat'][0] = api_data.json()
        newdogjson['cat'][1] = 0

    # store the image link
    data = newdogjson['cat'][0]['items'][(newdogjson['cat'][1])]['link']
    
    # increment the index
    newdogjson['cat'][1] += 1

    await ctx.send("Powered by Google. Link: " + data)

# On command '/newlizard15', fetch lizard image from unsplash api and post.
@bot.command(name='newlizard15')
async def new_lizard_15(ctx):

    searchTerm = "lizard"

    # first, check if an api call needs to be made, and perform one if necessary. update json file accordingly, and set index to 0.
    if (newdogjson['lizard'][0] == {} or newdogjson['lizard'][1] >= 10):
        api_data = requests.get('https://customsearch.googleapis.com/customsearch/v1?key=' + GOOGLEKEY + '&cx=a22729bb04f1e4c95&q=' + searchTerm + '&searchType=image&start=' + str(random.randint(0,90)))
        newdogjson['lizard'][0] = api_data.json()
        newdogjson['lizard'][1] = 0

    # store the image link
    data = newdogjson['lizard'][0]['items'][(newdogjson['lizard'][1])]['link']
    
    # increment the index
    newdogjson['lizard'][1] += 1

    await ctx.send("Powered by Google. Link: " + data)

# On command '/newrock15', fetch lizard image from unsplash api and post.
@bot.command(name='newrock15')
async def new_rock_15(ctx):

    searchTerm = "rock"

    # first, check if an api call needs to be made, and perform one if necessary. update json file accordingly, and set index to 0.
    if (newdogjson['rock'][0] == {} or newdogjson['rock'][1] >= 10):
        api_data = requests.get('https://customsearch.googleapis.com/customsearch/v1?key=' + GOOGLEKEY + '&cx=a22729bb04f1e4c95&q=' + searchTerm + '&searchType=image&start=' + str(random.randint(0,90)))
        newdogjson['rock'][0] = api_data.json()
        newdogjson['rock'][1] = 0

    # store the image link
    data = newdogjson['rock'][0]['items'][(newdogjson['rock'][1])]['link']
    
    # increment the index
    newdogjson['rock'][1] += 1

    await ctx.send("Powered by Google. Link: " + data)

# On command '/newferret15', fetch lizard image from unsplash api and post.
@bot.command(name='newferret15')
async def new_ferret_15(ctx):

    searchTerm = "ferret"

    # first, check if an api call needs to be made, and perform one if necessary. update json file accordingly, and set index to 0.
    if (newdogjson['ferret'][0] == {} or newdogjson['ferret'][1] >= 10):
        api_data = requests.get('https://customsearch.googleapis.com/customsearch/v1?key=' + GOOGLEKEY + '&cx=a22729bb04f1e4c95&q=' + searchTerm + '&searchType=image&start=' + str(random.randint(0,90)))
        newdogjson['ferret'][0] = api_data.json()
        newdogjson['ferret'][1] = 0

    # store the image link
    data = newdogjson['ferret'][0]['items'][(newdogjson['ferret'][1])]['link']
    
    # increment the index
    newdogjson['ferret'][1] += 1

    await ctx.send("Powered by Google. Link: " + data)

# On command '/newleon15', fetch lizard image from unsplash api and post.
@bot.command(name='newleon15')
async def new_leon_15(ctx):

    searchTerm = "leon+kennedy"

    # first, check if an api call needs to be made, and perform one if necessary. update json file accordingly, and set index to 0.
    if (newdogjson['leon'][0] == {} or newdogjson['leon'][1] >= 10):
        api_data = requests.get('https://customsearch.googleapis.com/customsearch/v1?key=' + GOOGLEKEY + '&cx=a22729bb04f1e4c95&q=' + searchTerm + '&searchType=image&start=' + str(random.randint(0,90)))
        newdogjson['leon'][0] = api_data.json()
        newdogjson['leon'][1] = 0

    # store the image link
    data = newdogjson['leon'][0]['items'][(newdogjson['leon'][1])]['link']
    
    # increment the index
    newdogjson['leon'][1] += 1

    await ctx.send("Powered by Google. Link: " + data)
    
# On command '/newguy15', fetch lizard image from unsplash api and post.
@bot.command(name='newguy15')
async def new_guy_15(ctx):
    
    searchTerm = "guy"

    # first, check if an api call needs to be made, and perform one if necessary. update json file accordingly, and set index to 0.
    if (newdogjson['guy'][0] == {} or newdogjson['guy'][1] >= 10):
        api_data = requests.get('https://customsearch.googleapis.com/customsearch/v1?key=' + GOOGLEKEY + '&cx=a22729bb04f1e4c95&q=' + searchTerm + '&searchType=image&start=' + str(random.randint(0,90)))
        newdogjson['guy'][0] = api_data.json()
        newdogjson['guy'][1] = 0

    # store the image link
    data = newdogjson['guy'][0]['items'][(newdogjson['guy'][1])]['link']
    
    # increment the index
    newdogjson['guy'][1] += 1

    await ctx.send("Powered by Google. Link: " + data)

@bot.command(name='newanimegirl15')
async def new_anime_girl_15(ctx):

    searchTerm = "anime+girl"

    # first, check if an api call needs to be made, and perform one if necessary. update json file accordingly, and set index to 0.
    if (newdogjson['animegirl'][0] == {} or newdogjson['animegirl'][1] >= 10):
        api_data = requests.get('https://customsearch.googleapis.com/customsearch/v1?key=' + GOOGLEKEY + '&cx=a22729bb04f1e4c95&q=' + searchTerm + '&searchType=image&start=' + str(random.randint(0,90)))
        newdogjson['animegirl'][0] = api_data.json()
        newdogjson['animegirl'][1] = 0

    # store the image link
    data = newdogjson['animegirl'][0]['items'][(newdogjson['animegirl'][1])]['link']

    # increment the index
    newdogjson['animegirl'][1] += 1

    await ctx.send("Powered by Google. Link: " + data)

@bot.command(name='newbird15')
async def new_anime_girl_15(ctx):

    searchTerm = "bird"

    # first, check if an api call needs to be made, and perform one if necessary. update json file accordingly, and set index to 0.
    if (newdogjson['bird'][0] == {} or newdogjson['bird'][1] >= 10):
        api_data = requests.get('https://customsearch.googleapis.com/customsearch/v1?key=' + GOOGLEKEY + '&cx=a22729bb04f1e4c95&q=' + searchTerm + '&searchType=image&start=' + str(random.randint(0,90)))
        newdogjson['bird'][0] = api_data.json()
        newdogjson['bird'][1] = 0

    # store the image link
    data = newdogjson['bird'][0]['items'][(newdogjson['bird'][1])]['link']

    # increment the index
    newdogjson['bird'][1] += 1

    await ctx.send("Powered by Google. Link: " + data)

@bot.command(name='newhgtvdreamhomesweepstakes15')
async def new_hgtv_dream_home_sweepstakes_15(ctx):

    searchTerm = "hgtv dream home sweepstakes"

    # first, check if an api call needs to be made, and perform one if necessary. update json file accordingly, and set index to 0.
    if (newdogjson['hgtv'][0] == {} or newdogjson['hgtv'][1] >= 10):
        api_data = requests.get('https://customsearch.googleapis.com/customsearch/v1?key=' + GOOGLEKEY + '&cx=a22729bb04f1e4c95&q=' + searchTerm + '&searchType=image&start=' + str(random.randint(0,90)))
        newdogjson['hgtv'][0] = api_data.json()
        newdogjson['hgtv'][1] = 0

    # store the image link
    data = newdogjson['hgtv'][0]['items'][(newdogjson['hgtv'][1])]['link']

    # increment the index
    newdogjson['hgtv'][1] += 1

    await ctx.send("Powered by Google. Link: " + data)

@bot.command(name='newcryptid15')
async def new_cryptid_15(ctx):

    searchTerm = "cryptid"

    # first, check if an api call needs to be made, and perform one if necessary. update json file accordingly, and set index to 0.
    if (newdogjson['cryptid'][0] == {} or newdogjson['cryptid'][1] >= 10):
        api_data = requests.get('https://customsearch.googleapis.com/customsearch/v1?key=' + GOOGLEKEY + '&cx=a22729bb04f1e4c95&q=' + searchTerm + '&searchType=image&start=' + str(random.randint(0,90)))
        newdogjson['cryptid'][0] = api_data.json()
        newdogjson['cryptid'][1] = 0

    # store the image link
    data = newdogjson['cryptid'][0]['items'][(newdogjson['cryptid'][1])]['link']

    # increment the index
    newdogjson['cryptid'][1] += 1

    await ctx.send("Powered by Google. Link: " + data)

@bot.command(name='newcar15')
async def new_car_15(ctx):

    searchTerm = "car"

    # first, check if an api call needs to be made, and perform one if necessary. update json file accordingly, and set index to 0.
    if (newdogjson['car'][0] == {} or newdogjson['car'][1] >= 10):
        api_data = requests.get('https://customsearch.googleapis.com/customsearch/v1?key=' + GOOGLEKEY + '&cx=a22729bb04f1e4c95&q=' + searchTerm + '&searchType=image&start=' + str(random.randint(0,90)))
        newdogjson['car'][0] = api_data.json()
        newdogjson['car'][1] = 0

    # store the image link
    data = newdogjson['car'][0]['items'][(newdogjson['car'][1])]['link']

    # increment the index
    newdogjson['car'][1] += 1

    await ctx.send("Powered by Google. Link: " + data)

@bot.command(name='newdragon15')
async def new_dragon_15(ctx):

    searchTerm = "dragon"

    # first, check if an api call needs to be made, and perform one if necessary. update json file accordingly, and set index to 0.
    if (newdogjson['dragon'][0] == {} or newdogjson['dragon'][1] >= 10):
        api_data = requests.get('https://customsearch.googleapis.com/customsearch/v1?key=' + GOOGLEKEY + '&cx=a22729bb04f1e4c95&q=' + searchTerm + '&searchType=image&start=' + str(random.randint(0,90)))
        newdogjson['dragon'][0] = api_data.json()
        newdogjson['dragon'][1] = 0

    # store the image link
    data = newdogjson['dragon'][0]['items'][(newdogjson['dragon'][1])]['link']

    # increment the index
    newdogjson['dragon'][1] += 1

    await ctx.send("Powered by Google. Link: " + data)

# ----------------------added 3/15/2025------------------------------------

@bot.command(name='newrat15')
async def new_rat_15(ctx):

    searchTerm = "rat"

    # first, check if an api call needs to be made, and perform one if necessary. update json file accordingly, and set index to 0.
    if (newdogjson['rat'][0] == {} or newdogjson['rat'][1] >= 10):
        api_data = requests.get('https://customsearch.googleapis.com/customsearch/v1?key=' + GOOGLEKEY + '&cx=a22729bb04f1e4c95&q=' + searchTerm + '&searchType=image&start=' + str(random.randint(0,90)))
        newdogjson['rat'][0] = api_data.json()
        newdogjson['rat'][1] = 0

    # store the image link
    data = newdogjson['rat'][0]['items'][(newdogjson['rat'][1])]['link']

    # increment the index
    newdogjson['rat'][1] += 1

    await ctx.send("Powered by Google. Link: " + data)

@bot.command(name='newjam15')
async def new_jam_15(ctx):

    searchTerm = "otter"

    # first, check if an api call needs to be made, and perform one if necessary. update json file accordingly, and set index to 0.
    if (newdogjson['otter'][0] == {} or newdogjson['otter'][1] >= 10):
        api_data = requests.get('https://customsearch.googleapis.com/customsearch/v1?key=' + GOOGLEKEY + '&cx=a22729bb04f1e4c95&q=' + searchTerm + '&searchType=image&start=' + str(random.randint(0,90)))
        newdogjson['otter'][0] = api_data.json()
        newdogjson['otter'][1] = 0

    # store the image link
    data = newdogjson['otter'][0]['items'][(newdogjson['otter'][1])]['link']

    # increment the index
    newdogjson['otter'][1] += 1

    await ctx.send("Powered by Google. Link: " + data)

# -------------------------------------------------RUNNING THE BOT------------------------------------------------------

async def on_ready():
    print("bot online")
    # Start the loop to check if it is DAY 15
    asyncio.run(check_to15())

# Run the bot, with the bot token
bot.run(TOKEN)

import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from datetime import datetime
import discord
import praw
import mimetypes
from discord.ext import commands
from dotenv import load_dotenv
from pyowm.owm import OWM
from random import randint
from pornhub_api import PornhubApi
from configparser import ConfigParser
import tweepy


config = ConfigParser()
config.read('config.cfg')

# prons
api = PornhubApi()


# twitter
consumer_key = config['twitter']['consumer_key']
consumer_secret = config['twitter']['consumer_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']


# news
news_url="https://news.google.com/news/rss"


# weather
owm = OWM(config['weather']['owm'])
weather_mgr = owm.weather_manager()
reg = owm.city_id_registry()


#reddit
reddit = praw.Reddit(client_id=config['reddit']['client_id'],
                     client_secret=config['reddit']['client_secret'],
                     user_agent=config['reddit']['user_agent'])


# bot
load_dotenv()
TOKEN = config['bot']['TOKEN']
GUILD = config['bot']['GUILD']
client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@client.command(help='Pong!')
async def ping(ctx):
    await ctx.send(f'Pong! {round (client.latency * 1000)}ms ')


@client.command(pass_context=True, help="It's probably raining in Scotland")
async def weather(message, location):
    list_of_tuples = reg.ids_for(location)
    for country in list_of_tuples:
        observation = weather_mgr.weather_at_place(f'{location},{country[2]}')
        weather = observation.weather
        weather.status  # short version of status (eg. 'Rain')
        weather.detailed_status
        temps = weather.temperature('celsius')
        await message.send(f"Weather in {location.title()}, {country[2]}\n"
                           f"Temp: {temps['temp']}C\n"
                           f"Max: {temps['temp_max']}C\n"
                           f"Min: {temps['temp_min']}C\n"
                           f"Feels like: {temps['feels_like']}C\n"
                           f"{weather.detailed_status.title()}")


@client.command(pass_context=True, help="What has that twat Trump done now?")
async def news(message):
    Client = urlopen(news_url)
    xml_page = Client.read()
    Client.close()
    soup_page = soup(xml_page, "xml")
    news_list = soup_page.findAll("item")
    # Print news title, url and publish date
    for news in news_list[0:5]:
        await message.send(f"{news.title.text}\n"
                           f"{news.link.text}\n")


@client.command(pass_context=True, help='Yeah baby! (NSFW, durr!)')
async def sexytime(message):
    subs = ('tightdresses', 'goddesses', 'shinyporn', 'trophywives', 'boltedontits')
    sub_num = randint(0, len(subs) - 1)
    start = randint(0, 15)
    posts = reddit.subreddit(subs[sub_num]).hot(limit=20)
    a = 0
    for post in posts:
        if a < start:
            a += 1
            continue
        mimetype, encoding = mimetypes.guess_type(post.url)
        if mimetype and mimetype.startswith('image'):
            await message.send(f"{post.url}")
            break


@client.command(pass_context=True, help="I'm lonely (NSF Your PP)")
async def xxx(message):
    data = api.search.search(
        ordering="mostviewed",
        period="weekly",
    )
    vid_num = randint(0, len(data.videos) - 1)
    vid = data.videos[vid_num]
    print(vid)
    await message.send(f"{vid.url}")


@client.command(pass_context=True, help='What a cunt')
async def trump(message):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    public_tweets = api.user_timeline('realDonaldTrump')

    tweet_num = randint(0, len(public_tweets) - 1)
    await message.send(public_tweets[tweet_num].text)


@client.command(pass_context=True, help='What a legend')
async def elon(message):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    public_tweets = api.user_timeline('elonmusk')

    tweet_num = randint(0, len(public_tweets) - 1)
    await message.send(public_tweets[tweet_num].text)


@client.command(pass_context=True, help="What's the time?")
async def time(message):
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    await message.send(f"Current Time: {current_time}")

@client.command(pass_context=True, help="Your life")
async def joke(message):
    jokes = reddit.subreddit('jokes').hot(limit=20)
    start = randint(1, 20)
    a = 1
    for joke in jokes:
        if a == start:
            await message.send(f"{joke.title}...\n"
                               f"{joke.selftext}")
            break
        else:
            a += 1
            continue

@client.command(pass_context=True, help="where are you?")
async def daddy(message):
    jokes = reddit.subreddit('dadjokes').hot(limit=20)
    start = randint(0, 20)
    a = 1
    for joke in jokes:
        if a == start:
            await message.send(f"{joke.title}...\n"
                               f"{joke.selftext}")
            break
        else:
            a += 1
            continue

client.run(TOKEN)

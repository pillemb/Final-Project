import os
import random
import discord
import asyncpraw
from discord.ext import commands

#code from: https://www.youtube.com/watch?v=nW8c7vT6Hl4&list=PLW3GfRiBCHOhfVoiDZpSz8SM_HybXRPzZ&index=1&ab_channel=Lucas
# for lines 9 to 20

TOKEN = os.environ['TOKEN']                   #Discord bot token
client_id = os.environ['client_id']           #Reddit client ID
client_secret = os.environ['client_secret']   #Reddit client token

client = commands.Bot(command_prefix='$')     #setting up bot prefix

reddit = asyncpraw.Reddit(client_id = client_id, client_secret = client_secret, user_agent = 'meme')     #setting up reddit api


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')   #when bot is ready, it will print into console




@client.command()
async def search(ctx, sub, sort='hot', num=100):  #command for bot to take post from a subreddit $search 'subreddit', 'sorting', 'amount of posts'
  posts = []                           #list of the posts in the subreddit
  sr=await reddit.subreddit(sub)
  
  if sort == 'hot': 
    async for post in sr.hot(limit=int(num)):             #puts posts in a list and randomly chooses a post from the list
      if post.over_18 == True or post.stickied == True:   #filters nsfw content and pinned posts
        pass
      else:
        posts.append(post)
    result_post = random.choice(posts)
    if result_post.is_self == True:
      url = 'https://www.reddit.com' + result_post.permalink
      embed=discord.Embed(title=result_post.title, url=url, description = result_post.selftext)   #If post found has only test, embed it.
      await ctx.send(embed=embed)
    else:
      url = 'https://www.reddit.com' + result_post.permalink    #embeds the link to post so user can click on it
      embed=discord.Embed(title=result_post.title, url=url)     #embeds post title as text 
      await ctx.send(embed=embed)
      await ctx.send( result_post.url)

  elif sort == 'new':                                        #same as above, but sorts through 'new'
    async for post in sr.new(limit=int(num)):              
      if post.over_18 == True or post.stickied == True:    
        pass
      else:
        posts.append(post)
    result_post = random.choice(posts)
    if result_post.is_self == True:
      url = 'https://www.reddit.com' + result_post.permalink
      embed=discord.Embed(title=result_post.title, url=url, description = result_post.selftext)
      await ctx.send(embed=embed)
    else:
      url = 'https://www.reddit.com' + result_post.permalink
      embed=discord.Embed(title=result_post.title, url=url)
      await ctx.send(embed=embed)
      await ctx.send( result_post.url)

  elif sort == 'top':                                       #same as above, but sorts through 'top'
    async for post in sr.top(limit=int(num)):             
      if post.over_18 == True or post.stickied == True:  
        pass
      else:
        posts.append(post)
    result_post = random.choice(posts)
    if result_post.is_self == True:
      url = 'https://www.reddit.com' + result_post.permalink
      embed=discord.Embed(title=result_post.title, url=url, description = result_post.selftext)
      await ctx.send(embed=embed)
    else:
      url = 'https://www.reddit.com' + result_post.permalink
      embed=discord.Embed(title=result_post.title, url=url)
      await ctx.send(embed=embed)
      await ctx.send( result_post.url)





@client.command(aliases=['make'])           #make me hungry command, browses r/food, sends yummy back.
async def make_me_hungry(ctx, me, hungry):
  if me == 'me' and hungry == 'hungry':
    posts = []
    sr = await reddit.subreddit('food')
    async for post in sr.hot(limit=100):
      posts.append(post)
    result_post = random.choice(posts)
    await ctx.send(result_post.url)
  else:
    pass




@client.command()               #Command to delete large amounts of messages.
async def clear(ctx, amount=5):
  await ctx.channel.purge(limit=amount+1)
  

client.run(TOKEN)

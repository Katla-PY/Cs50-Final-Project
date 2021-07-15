
import os, discord, datetime, requests

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

def time():
    date = datetime.datetime.now()
    return f"{date.year}/{date.month}/{date.day}~{date.strftime('%X')}"

@client.event
async def on_ready():
    print('@ {1}\n{0.user}:({0.user.id}) logged in\n'.format(client, time()))

@client.event
async def on_message(message):
    if message.author==client.user:
        return
    
    print("@ {1}\nFrom {0.author}:({0.author.id})\nMessage: {0.content}\n".format(message, time()))

@client.event
async def on_member_join(member):
    print("@ {1}\nUser: {0}:({0.id})\nJoined: {0.guild}:({0.guild.id})\n".format(member, time()))

@client.event
async def on_member_remove(member):
    print("@ {1}\nUser: {0}:({0.id})\nLeft: {0.guild}:({0.guild.id})\n".format(member, time()))

if __name__=="__main__":
    client.run(os.getenv("BOT_TOKEN"))
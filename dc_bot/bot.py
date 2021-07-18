
import os, discord, datetime, re, requests, json
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix="/", intents=intents)

def time():
    # gets current time
    date = datetime.datetime.now()
    return f"{date.year}/{date.month}/{date.day}~{date.strftime('%X')}"

###
# Events
###

@client.event
async def on_ready():
    print('@ {1}\n{0.user}:({0.user.id}) logged in\n'.format(client, time()))

@client.event
async def on_message(message):
    if message.author==client.user:
        return

    await client.process_commands(message)

    print("@ {1}\nFrom {0.author}:({0.author.id})\nMessage: {0.content}\n".format(message, time()))

@client.event
async def on_member_join(member):
    print("@ {1}\nUser: {0}:({0.id})\nJoined: {0.guild}:({0.guild.id})\n".format(member, time()))

@client.event
async def on_member_remove(member):
    print("@ {1}\nUser: {0}:({0.id})\nLeft: {0.guild}:({0.guild.id})\n".format(member, time()))

###
# Bot commands
###

@client.command(name="setup")
@commands.has_permissions(administrator=True)
async def _setup(ctx):
    
    await ctx.send("Setting up {0.name}:({0.id})".format(ctx.guild))

    # gets bool from flask api
    api_req = requests.get("http://127.0.0.1:5000/server_setup?server-id={0.id}&server-name={0.name}".format(ctx.guild))

    # loads api response as dict
    api_req = json.loads(api_req.text)

    if api_req["exists"]:
        await ctx.send("Server already setup")
        return

    for member in ctx.guild.members:
        api_req = requests.get(f"http://127.0.0.1:5000/server_setup_users?server-id={ctx.guild.id}&user-id={member.id}")

    await ctx.send("Server setup complete")

@client.command(name="sheesh")
async def _sheesh(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/680928395399266314/865187562918117396/sheeesh.mp4")

@client.command(name="p")
async def _print(ctx, *, message):
    await ctx.send(message)

if __name__=='__main__':
    client.run(os.getenv("BOT_TOKEN"))

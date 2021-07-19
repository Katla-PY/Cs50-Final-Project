
import os, discord, datetime, re, requests, json
from discord.ext import commands

API_URL = "http://127.0.0.1:5000"

intents = discord.Intents.default()
intents.guilds = True
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


@client.event
async def on_guild_remove(guild):
    requests.get(f"{API_URL}/api/remove_server?server-id={guild.id}")

###
# Bot commands
###

# TODO: create roll muted on setup
@client.command(name="setup")
@commands.has_permissions(administrator=True)
async def _setup(ctx):
    
    await ctx.send("Setting up {0.name}:({0.id})".format(ctx.guild))

    # gets bool from flask api
    api_req = requests.get("{1}/api/add_server?server-id={0.id}&server-name={0.name}".format(ctx.guild, API_URL))

    # loads api response as dict
    api_req = json.loads(api_req.text)

    if api_req["exists"]:
        await ctx.send("Server already setup")
        return

    for member in ctx.guild.members:
        requests.get(f"{API_URL}/api/add_user?user-id={member.id}&user-name={member.name}")
        requests.get(f"{API_URL}/api/add_user_server?user-id={member.id}&server-id={ctx.guild.id}")

    await ctx.send("Server setup complete")

@client.command(name="mute")
async def _mute(ctx, user: discord.Member, *, reason=None):

    requests.get(f"{API_URL}/api/user_violation?user-id={user.id}&server-id={ctx.guild.id}&violation-id=2&reason={reason}")

    role = discord.utils.get(ctx.guild.roles, name="muted")

    if not role:
        role = await ctx.guild.create_role(name="muted")

        for channel in ctx.guild.channels:
            await channel.set_permissions(role, send_messages=False, speak=False, read_message_history=True)

    await user.add_roles(role, reason=reason)

@client.command(name="unmute")
async def _unmute(ctx, user: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="muted")

    if not role:
        return

    await user.remove_roles(role)


@client.command

@client.command(name="sheesh")
async def _sheesh(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/680928395399266314/865187562918117396/sheeesh.mp4")

@client.command("whoasked")
async def _whoasked(ctx, user):
    await ctx.message.delete()
    await ctx.send(f"{user} https://cdn.discordapp.com/attachments/680928395399266314/866657138280890438/video0_3.mp4")


@client.command(name="p")
async def _print(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(message)

if __name__=='__main__':
    client.run(os.getenv("BOT_TOKEN"))

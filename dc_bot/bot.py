import os, discord, datetime, requests, json, asyncio
from discord.ext import commands

API_URL = "http://127.0.0.1:5000"

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

client = commands.Bot(command_prefix="/", intents=intents)


def _time():
    # gets current time
    date = datetime.datetime.now()
    return f"{date.year}/{date.month}/{date.day}~{date.strftime('%X')}"

###
# Events
###

@client.event
async def on_ready():
    print('@ {1}\n{0.user}:({0.user.id}) logged in\n'.format(client, _time()))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await client.process_commands(message)

    print("@ {1}\nFrom {0.author}:({0.author.id})\nMessage: {0.content}\n".format(message, _time()))


@client.event
async def on_member_join(member):
    print("@ {1}\nUser: {0}:({0.id})\nJoined: {0.guild}:({0.guild.id})\n".format(member, _time()))


@client.event
async def on_member_remove(member):
    print("@ {1}\nUser: {0}:({0.id})\nLeft: {0.guild}:({0.guild.id})\n".format(member, _time()))


@client.event
async def on_guild_remove(guild):
    requests.request(
        "POST", f"{API_URL}/api/remove_server",
        data={"server-id": guild.id}
    )

###
# Bot commands
###

@client.command(name="setup")
@commands.has_permissions(administrator=True)
async def _setup(ctx):

    await ctx.send("Setting up {0.name}:({0.id})".format(ctx.guild))

    # gets bool from flask api
    api_res = requests.request(
        "POST", f"{API_URL}/api/add_server",
        data={"server-id": ctx.guild.id, "server-name": ctx.guild.name}
    )

    # loads api response as dict
    api_res = json.loads(api_res.text)

    # checks if server already exists
    if api_res["exists"]:
        await ctx.send("Server already setup")
        return

    members = []

    for member in ctx.guild.members:
        members.append([member.id, member.name])

    requests.request(
        "POST", f"{API_URL}/api/add_server_users",
        json={"users": members}
    )

    requests.request(
        "POST", f"{API_URL}/api/add_user_server",
        json={"server-id": ctx.guild.id, "users": members}
    )

    await ctx.send("Server setup complete")


@client.command(name="mute")
async def _mute(ctx, user: discord.Member, time_: int=5, unit="m", *, reason="No reason provided"):
    try:
        await ctx.message.delete()
    except discord.errors.NotFound:
        pass
    
    requests.request(
        "POST", f"{API_URL}/api/user_violation",
        data={"user-id": user.id, "server-id": ctx.guild.id, "violation-id": 2, "reason": reason}
    )

    role = discord.utils.get(ctx.guild.roles, name="muted")

    if not role:
        role = await ctx.guild.create_role(name="muted")

        for channel in ctx.guild.channels:
            await channel.set_permissions(role, send_messages=False, speak=False, read_message_history=True)

    await user.add_roles(role, reason=reason)

    log_channel = discord.utils.get(ctx.guild.channels, name="logs").id
    log_channel = client.get_channel(log_channel)
    await log_channel.send(f"{ctx.message.author} **muted** {user}")

    embed = discord.Embed(title="User::Mute", color=0xff0000)
    embed.add_field(name="User:", value=f"{user.name}", inline=False)
    embed.add_field(name="Unit:", value=f"{time_} {unit}", inline=False)
    embed.add_field(name="Reason:", value=f"{reason}", inline=False)
    await ctx.send(embed=embed)

    if unit not in ["s", "m", "h"]:
        unit = "m"

    if unit=="s":
        seconds = time_
    elif unit=="m":
        seconds = time_*60
    elif unit=="h":
        seconds = time_*3600

    await asyncio.sleep(seconds)
    await user.remove_roles(role)


@client.command(name="kick")
async def _kick(ctx, user: discord.Member, *, reason="No reason provided"):
    try:
        await ctx.message.delete()
    except discord.errors.NotFound:
        pass
    
    requests.request(
        "POST", f"{API_URL}/api/user_violation",
        data={"user-id": user.id, "server-id": ctx.guild.id, "violation-id": 3, "reason": reason}
    )

    await user.kick(reason=reason)

    log_channel = discord.utils.get(ctx.guild.channels, name="logs").id
    log_channel = client.get_channel(log_channel)
    await log_channel.send(f"{ctx.message.author} **kicked** {user}")

    embed = discord.Embed(title="User::Kick", color=0xff0000)
    embed.add_field(name="User:", value=f"{user.name}", inline=False)
    embed.add_field(name="Reason:", value=f"{reason}", inline=False)
    await ctx.send(embed=embed)


@client.command(name="ban")
async def _ban(ctx, user: discord.Member, *, reason="No reason provided"):
    try:
        await ctx.message.delete()
    except discord.errors.NotFound:
        pass
    
    requests.request(
        "POST", f"{API_URL}/api/user_violation",
        data={"user-id": user.id, "server-id": ctx.guild.id, "violation-id": 4, "reason": reason}
    )

    await user.ban(reason=reason)

    log_channel = discord.utils.get(ctx.guild.channels, name="logs").id
    log_channel = client.get_channel(log_channel)
    await log_channel.send(f"{ctx.message.author} **banned** {user}")

    embed = discord.Embed(title="User::Ban", color=0xff0000)
    embed.add_field(name="User:", value=f"{user.name}", inline=False)
    embed.add_field(name="Reason:", value=f"{reason}", inline=False)
    await ctx.send(embed=embed)


@client.command(name="warn")
async def _warn(ctx, user: discord.Member, *, reason="No reason provided"):
    await ctx.message.delete()
    
    api_res = requests.request(
        "POST", f"{API_URL}/api/user_violation",
        data={"user-id": user.id, "server-id": ctx.guild.id, "violation-id": 1, "reason": reason}
    )

    # loads api response as dict
    api_res = json.loads(api_res.text)

    if api_res["warns"] > 0:
        if api_res["warns"] in (3, 6, 8):
            await _mute(ctx, user, reason=f"{api_res['warns']} warns")
            return
        elif api_res["warns"] in (5, 7, 9):
            await _kick(ctx, user, reason=f"{api_res['warns']} warns")
            return
        elif api_res["warns"] == 10:
            await _ban(ctx, user, reason=f"10 warns")
            return
    
    log_channel = discord.utils.get(ctx.guild.channels, name="logs").id
    log_channel = client.get_channel(log_channel)
    await log_channel.send(f"{ctx.message.author} **warned** {user}")

    embed = discord.Embed(title="User::Warn", color=0xff0000)
    embed.add_field(name="User:", value=f"{user.name}", inline=False)
    embed.add_field(name="Reason:", value=f"{reason}", inline=False)
    await ctx.send(embed=embed)


@client.command(name="p")
async def _print(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(message)


if __name__=="__main__":
    client.run(os.getenv("BOT_TOKEN"))

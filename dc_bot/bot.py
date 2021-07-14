
import discord

bot = {
    "token": "ODY0ODIzMDI2MDE3MTA4MDA1.YO7DNQ.PwRuW7sCk2BOIQzR6UyVJEmg6Cc"
}

# intents = discord.Intents.default()
# intents.members = True
# client = discord.Client(intents=intents)

# @client.event
# async def on_ready():
#     print('{0.user}:({0.user.id}) logged in'.format(client))

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
    
#     print("From {0.author}:({0.author.id})\nMessage: {0.content}".format(message))

# @client.event
# async def on_member_join(member):

#     print(f"{member}:({member.id}) has joined")

# if __name__=="__main__":
#     client.run(bot["token"])

class Client(discord.Client):
    async def on_ready(self):
        print('{0.user}:({0.user.id}) logged in\n'.format(self))
    
    async def on_message(self, message):
        if message.author == self.user:
            return
        
        print("From {0.author}:({0.author.id})\nMessage: {0.content}\n".format(message))

    async def on_member_join(self, member):

        print(f"{member}:({member.id}) has joined\n")

if __name__=="__main__":
    intents = discord.Intents.default()
    intents.members = True

    client = Client(intents=intents)
    client.run(bot["token"])

import discord
import os
import openpyxl
import atexit
import random
import time
import asyncio
from discord.ext import commands

# Load your token securely (replace 'your_token_here' with your actual token)
TOKEN = os.getenv("DISCORD_TOKEN")

# Setting up intents
intents = discord.Intents.default()
intents.messages = True  # Required to read messages
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)

# Hardcoded save path
SAVE_PATH = os.path.expanduser('~/all/data.xlsx')  # Change this to your desired location

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# Raw Data Lists
userIDList = []
messageIDList = []
xpFromMessage = []
commandUseTimestamp = []

def clearRawData(securitycode: str):
    if securitycode == "DELETE":
        userIDList.clear()
        messageIDList.clear()
        xpFromMessage.clear()
        commandUseTimestamp.clear()

def save_data():
    try:
        print(f"Saving data to: {SAVE_PATH}")  # Debugging output
        
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "User Data"
        
        # Write headers
        sheet.append(["User ID", "Message ID", "XP", "Timestamp"])
        
        # Write data
        for i in range(len(userIDList)):
            sheet.append([userIDList[i], messageIDList[i], xpFromMessage[i], commandUseTimestamp[i]])
        
        workbook.save(SAVE_PATH)
        print("Data saved successfully.")
    except Exception as e:
        print(f"Error saving data: {e}")

def updateList(userid, messageid, xptoadd, timestamp):
    userIDList.append(int(userid))
    messageIDList.append(messageid.id if isinstance(messageid, discord.Message) else messageid)
    xpFromMessage.append(int(xptoadd))
    commandUseTimestamp.append(str(timestamp))

def save_on_exit():
    save_data()

atexit.register(save_on_exit)  # Save data when the bot exits

async def periodic_save():
    while True:
        save_data()
        await asyncio.sleep(300)  # Save every 5 minutes

class MyBot(commands.Bot):
    async def setup_hook(self):
        # This will schedule the periodic_save task when the bot is ready.
        self.loop.create_task(periodic_save())

# Instantiate your bot using the custom class
bot = MyBot(command_prefix=".", intents=intents)

@bot.command()
async def mansave(ctx,):
    save_data()


@bot.command()
async def xpno(ctx,):

    #vars
    emoji = "0️⃣"
    xp = 0

    # Check if the user is replying to a message
    if ctx.message.reference:
        # Get the message that is being replied to
        original_message = await ctx.fetch_message(ctx.message.reference.message_id)
        
        # get userid of the original message sender
        original_user_id = original_message.author.id

        # delete the bot command reply
        await ctx.message.delete()

        # Add the reaction (emoji) to the original message
        await original_message.add_reaction(emoji)

        updateList(original_user_id, original_message, xp, (time.ctime()))

    else:
        await ctx.send("You need to reply to a message first!")



@bot.command()
async def xpskl(ctx,):

    #vars
    emoji = "1️⃣"
    xp = 1

    # Check if the user is replying to a message
    if ctx.message.reference:
        # Get the message that is being replied to
        original_message = await ctx.fetch_message(ctx.message.reference.message_id)
        
        # get userid of the original message sender
        original_user_id = original_message.author.id

        # delete the bot command reply
        await ctx.message.delete()

        # Add the reaction (emoji) to the original message
        await original_message.add_reaction(emoji)

        updateList(original_user_id, original_message, xp, (time.ctime()))

    else:
        await ctx.send("You need to reply to a message first!")


@bot.command()
async def xpsty(ctx,):

    #vars
    emoji = "2️⃣"
    xp = 2

    # Check if the user is replying to a message
    if ctx.message.reference:
        # Get the message that is being replied to
        original_message = await ctx.fetch_message(ctx.message.reference.message_id)
        
        # get userid of the original message sender
        original_user_id = original_message.author.id

        # delete the bot command reply
        await ctx.message.delete()




        # Add the reaction (emoji) to the original message
        await original_message.add_reaction(emoji)

        updateList(original_user_id, original_message, xp, (time.ctime()))

    else:
        await ctx.send("You need to reply to a message first!")


@bot.command()
async def xpfnd(ctx,):

    #vars
    emoji = "3️⃣"
    xp = 3

    # Check if the user is replying to a message
    if ctx.message.reference:
        # Get the message that is being replied to
        original_message = await ctx.fetch_message(ctx.message.reference.message_id)
        
        # get userid of the original message sender
        original_user_id = original_message.author.id

        # delete the bot command reply
        await ctx.message.delete()




        # Add the reaction (emoji) to the original message
        await original_message.add_reaction(emoji)

        updateList(original_user_id, original_message, xp, (time.ctime()))

    else:
        await ctx.send("You need to reply to a message first!")


#exports all raw data from the 4 main lists
@bot.command()
async def exportraw(ctx,):
    await ctx.send(f"User id: {userIDList} OG message id {messageIDList} xp: {xpFromMessage} timestamp: {commandUseTimestamp}")

#clears raw data from the 4 main lists 


@bot.command()
async def clearraw(ctx,):
    # Send confirmation message asking the user to reply with "DELETE"
    confirmation_message = await ctx.send(
        f"{ctx.author.mention}\n\nAre you SURE that you want to clear all of the raw data stored? This CANNOT be recovered.\n\nIf you want to proceed with deleting ALL saved data, reply to this message with 'DELETE'. If you do not want to clear all saved data, type anything else in a reply to this message, or wait 30 seconds, and this request will expire"
    )

    #deletes bot command issued by user
    await ctx.message.delete() 

    # Wait for a reply to the confirmation message
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel and message.reference and message.reference.message_id == confirmation_message.id

    try:
        # Wait for the user to reply within 60 seconds
        reply = await bot.wait_for('message', timeout=30.0, check=check)

        # Check if the reply is "DELETE"
        if reply.content.strip().upper() == "DELETE":
            # Clear the saved data (implement your actual data clearing logic here)
            clearRawData("DELETE") # You can replace this with your data clearing function

            await ctx.send("All raw data has been successfully cleared!")
        else:
            await ctx.send("Deletion canceled. The data was not cleared.")
        
        # Optionally, delete the confirmation and user reply messages to keep the channel clean
        await confirmation_message.delete()
        await reply.delete()

    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond. Deletion canceled.")
        await confirmation_message.delete()



@bot.command()
async def exportuser(ctx, userid: int):
    # This is a list that temporarily stores the other list's index numbers for the specific data requested for export
    indexListToExport = [i for i, x in enumerate(userIDList) if x == userid]
    
    exportdata = []  # Initialize the list outside the loop to store the results
    
    # Iterate over the indexes in indexListToExport
    for i in indexListToExport:
        # Append the data from both userIDList and xpFromMessage using the index
        exportdata.append({
            'xp': xpFromMessage[i], 
            'timestamp': commandUseTimestamp[i]
            
        })
    total_xp = sum(data['xp'] for data in exportdata)
    # If there is any data to export, format it for display
    if exportdata:
        formatted_data = "\n".join([f" Timestamp: {data['timestamp']}, XP: {data['xp']}" for data in exportdata])
        await ctx.send(f"Here is the data for {userid}:\n\n{formatted_data}\n\nTotal XP Gained: {total_xp} ")
    else:
        await ctx.send(f"No data found for {userid}.")



@bot.command()
async def exportalluser(ctx):
    # Group the data by user ID
    data_by_user = {}
    for i in range(len(userIDList)):
        user_id = userIDList[i]
        xp = xpFromMessage[i]
        timestamp = commandUseTimestamp[i]
        if user_id not in data_by_user:
            data_by_user[user_id] = []
        data_by_user[user_id].append((timestamp, xp))
    
    # Build the output message
    output_lines = []
    for user_id, entries in data_by_user.items():
        output_lines.append(str(user_id))
        output_lines.append("")  # Blank line for formatting
        
        total_xp = 0
        for timestamp, xp in entries:
            output_lines.append(f"{timestamp}, XP: {xp}")
            total_xp += xp
        
        output_lines.append("")
        output_lines.append(f"Total XP Gained: {total_xp}")
        output_lines.append("")  # Blank line to separate users
    
    final_output = "\n".join(output_lines)
    
    # Send the final output (if the message is too long consider sending it as a file)
    await ctx.send(final_output)

    

# Run the bot
bot.run(TOKEN)

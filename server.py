import discord
import requests

bot = discord.Client()

sleep_logo = """
                  ██████  ██▓    ▓█████ ▓█████  ██▓███  
                ▒██    ▒ ▓██▒    ▓█   ▀ ▓█   ▀ ▓██░  ██▒
                ░ ▓██▄   ▒██░    ▒███   ▒███   ▓██░ ██▓▒
                  ▒   ██▒▒██░    ▒▓█  ▄ ▒▓█  ▄ ▒██▄█▓▒ ▒
                ▒██████▒▒░██████▒░▒████▒░▒████▒▒██▒ ░  ░
                ▒ ▒▓▒ ▒ ░░ ▒░▓  ░░░ ▒░ ░░░ ▒░ ░▒▓▒░ ░  ░
                ░ ░▒  ░ ░░ ░ ▒  ░ ░ ░  ░ ░ ░  ░░▒ ░     
                ░  ░  ░    ░ ░      ░      ░   ░░       
                      ░      ░  ░   ░  ░   ░  ░
"""

expecting_captcha = False

@bot.event
async def on_message(message):
  global expecting_captcha
  
  if message.author.id == 960296984365903952 and message.content != "Success." and message.content != "Failure.":
    print(" [ SLEEP ] Expecting response.")
    expecting_captcha = True

  if message.channel.id == 960289900224192522 and (message.content == "1" or message.content == "2" or message.content == "3" or message.content == "4" or message.content == "refresh"):
    signal = requests.get("your_url/simplemmo/captcha.php?task=captcha&state=send&captcha_response={}".format(message.content))
    print(" [ SLEEP ] Sent captcha response",signal)
    expecting_captcha = False

  if message.channel.id == 960715687385518110 and (message.content == "start" or message.content == "stop"):
    signal = None
    if message.content == "start":
       signal = requests.get("your_url/simplemmo/captcha.php?task=remote&state=send&value=true")
    else:
      signal = requests.get("your_url/simplemmo/captcha.php?task=remote&state=send&value=false")
    print(" [ SLEEP ] Sent remote activation",signal)

print(sleep_logo, "[ SLEEP ] Server started.\n")

bot.run("your_discord_bot_token")

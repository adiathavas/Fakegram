import instabot 

bot = instabot.Bot(filter_users=False)
bot.login()
bot.like_followers("toronto")


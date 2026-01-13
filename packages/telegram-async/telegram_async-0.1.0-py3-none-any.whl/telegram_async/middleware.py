from telegram_async import Bot
from telegram_async.throttling import Throttle

bot = Bot(token="TOKEN")
throttle = Throttle()

@bot.middleware()
async def rate_limit(ctx, next):
    allowed = await throttle.check(ctx.user_id, rate=5, per=10)
    if not allowed:
        await ctx.reply("⛔ Too many attempts. Please wait a moment.")
        return
    await next()

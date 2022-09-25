from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Open navigation"),
            types.BotCommand("help", "Show help"),
            types.BotCommand("admins", "Open admins panel (ONLY FOR ADMINS!!!!!)"),
        ]
    )

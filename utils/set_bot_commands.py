from aiogram import types

#set some commands that bot can show to user anytime
async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Start the bot"),
            types.BotCommand("help", "Show useful commands"),
            types.BotCommand("random", "Get random recipe"),
            types.BotCommand("filters", "Get recipe based on filters")
        ]
    )

import os
import discord
from discord.ext import commands
from datetime import datetime, timedelta
import platform

# import logging
# logging.basicConfig(level=logging.INFO)
#    status=discord.Status.
# status=discord.Status.idle

bot = commands.Bot(
    command_prefix='m:'
)

bot.remove_command('help')
bot.BORDER_COLOR = 0x00aaaa

# 掲載サーバー用カテの区切りになるカテ
bot.info_start_cate_id = 653327583206703168
bot.info_end_cate_id = 650704906365435923


@bot.event
async def on_ready():
    jst = datetime.utcnow() + timedelta(hours=9)
    print('--------------------------------')
    print(jst.strftime('%Y/%m/%d %H:%M:%S'))
    print(f'{bot.user.name} ({bot.user.id})')
    print(f'discord.py {discord.__version__} python {platform.python_version()}')
    print('--------------------------------')

    bot.load_extension('cogs.admintoolsCog')


bot.run(os.environ['DISCORD_BOT_MIHON_TOKEN'])

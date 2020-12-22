import os
import discord
from discord.ext import commands
from datetime import datetime, timedelta
import json
import platform

intents = discord.Intents.all()
intents.typing = False  # typingを受け取らないように
bot = commands.Bot(command_prefix='m:', intents=intents)

# 設定ファイル読み込み（本番用も開発用も同じものだけ）
with open("mihon_config.json", "r", encoding="utf-8_sig") as f:
    bot.config = json.load(f)

# 本番環境と開発環境で異なる定数
# 開発環境
'''
TOKEN = 'DISCORD_BOT_MIHON_TOKEN_T'
GUILD_ID = 762847789259423754
bot.info_start_cate_id = 762847790354530331 # 区切りカテ（上）
bot.info_end_cate_id = 762995177006170112 # 区切りカテ（下）
bot.report_summary_ch_id = 764078688199245826
bot.bump_channel_id = 762847792213262345
'''
# 本番環境
TOKEN = 'DISCORD_BOT_MIHON_TOKEN'
GUILD_ID = 641916844990529537
bot.info_start_cate_id = 653327583206703168 # 区切りカテ（上）
bot.info_end_cate_id = 763583069163749406 # 区切りカテ（下）
bot.report_summary_ch_id = 764498318620885062
bot.bump_channel_id = 659638377494216717

# cogのロード
bot.load_extension('cogs._extentions')


@bot.event
async def on_ready():
    bot.GUILD = bot.get_guild(GUILD_ID) # サーバー専属ボットなので指定ギルドのみ動作
    jst = datetime.utcnow() + timedelta(hours=9)
    print('--------------------------------')
    print(f"{jst.strftime('%Y/%m/%d %H:%M:%S')} JST")
    print(f'{bot.user.name} ({bot.user.id})')
    print(f'discord.py {discord.__version__} python {platform.python_version()}')
    print('--------------------------------')


bot.run(os.environ[TOKEN])

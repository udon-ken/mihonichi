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

# 本番環境も開発環境も同じ定数
bot.BORDER_COLOR = 0x00aaaa
bot.man_role_name = '男性'
bot.woman_role_name = '女性'
bot.not_prof_role_name = 'プロフ【未】'
bot.man_exist_prof_role_name = 'プロフ【男】'
bot.woman_exist_prof_role_name = 'プロフ【女】'
bot.beginner_role_name = '🌱'

bot.man_prof_ch_name = '男性プロフィール'
bot.woman_prof_ch_name = '女性プロフィール'

# 本番環境と開発環境で異なる定数
# 開発環境
TOKEN = 'DISCORD_BOT_MIHON_TOKEN_T'
GUILD_ID = 762847789259423754
# 掲載サーバー用カテの区切りになるカテ
bot.info_start_cate_id = 762847790354530331
bot.info_end_cate_id = 762995177006170112
bot.bump_channel_id = 762847792213262345

# 本番環境
TOKEN = 'DISCORD_BOT_MIHON_TOKEN'
GUILD_ID = 641916844990529537
# 掲載サーバー用カテの区切りになるカテ
bot.info_start_cate_id = 653327583206703168
bot.info_end_cate_id = 763583069163749406
bot.bump_channel_id = 659638377494216717


@bot.event
async def on_ready():
    jst = datetime.utcnow() + timedelta(hours=9)
    print('--------------------------------')
    print(jst.strftime('%Y/%m/%d %H:%M:%S'))
    print(f'{bot.user.name} ({bot.user.id})')
    print(f'discord.py {discord.__version__} python {platform.python_version()}')
    print('--------------------------------')

    bot.GUILD = bot.get_guild(GUILD_ID) # 完全専属サーバーなのでギルドと言えばコレ！

    bot.load_extension('cogs.admin_toolsCog')
    bot.load_extension('cogs.move_categoryCog')
    bot.load_extension('cogs.auto_rolesCog')


bot.run(os.environ[TOKEN])

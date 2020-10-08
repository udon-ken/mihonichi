# import discord
from discord.ext import commands
import re

import utils.lib


class admin_toolsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['sl'])
    # @commands.has_permissions(administrator=True)
    async def server_list(self, ctx):
        """掲載サーバーのカテゴリ一覧を出力（【】は削除）"""
        if ctx.author.bot:
            return
        cate_list = []
        is_start = False

        for cate in ctx.author.guild.categories:
            if cate.id == self.bot.info_start_cate_id: # 鯖情報カテ開始
                is_start = True
                continue
            if cate.id == self.bot.info_end_cate_id: # 鯖情報カテ終了
                break

            if is_start:
                cate_list.append(re.sub('(【|】)', '', cate.name))

        title = f'● 掲載サーバー数 {len(cate_list)}サーバー'
        result = '\n'.join(cate_list)
        await ctx.send(f'{title}```{result}```')

    @commands.command(aliases=['cl'])
    # @commands.has_permissions(administrator=True)
    async def cate_list(self, ctx):
        """全カテゴリ一覧を出力（【】は削除）"""
        if ctx.author.bot:
            return
        cate_list = []

        for cate in ctx.author.guild.categories:
            cate_list.append(re.sub('(【|】)', '', cate.name))

        title = f'● カテゴリ総数 {len(cate_list)}カテゴリ'
        result = '\n'.join(cate_list)
        await ctx.send(f'{title}```{result}```')

    # opt(bool)に3つの状態を持たせるのはトリッキーかも？
    @commands.command()
    # @commands.has_permissions(manage_roles=True)
    async def roles(self, ctx, opt: bool = None):
        """ロールと人数表示（以前のDynoの仕様に近い形式） """
        if ctx.author.bot:
            return

        if opt is None:
            roles = sorted(ctx.guild.roles, reverse=True)
        else:
            roles = sorted(ctx.guild.roles, key=lambda r: len(r.members), reverse=opt)
        result = ''
        results = []
        for role in roles:
            mentionable = ' *' if role.mentionable else ''
            result += f'{role.name}：{len(role.members)}{mentionable}\n'
            # メッセージ内文字数で区切る
            if len(result) > 1900:
                results.append(result)
                result = ''
        # 余ったテキストを追加
        results.append(result)

        all_count = len(ctx.guild.members)
        bot_count = sum(1 for member in ctx.guild.members if member.bot)
        human_count = all_count - bot_count

        header = 'メンバー数右の*はそのロールに対してのメンション許可\n'
        header += f'オプションは0か1 0=少ない順 1=多い順  例：{self.bot.command_prefix}roles 1\n\n'
        header += f'全ロール数：{len(roles)}　全メンバー：{all_count}　人間：{human_count}　bot：{bot_count}\n'

        await ctx.send(f'```{header}```') # タイトル部
        for result in results: # 結果部分ループして出力
            await ctx.send(f'```{result}```')

    @roles.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await utils.lib.send_error(ctx, f'ロール管理の権限が必要です\n\n{error}')
        if isinstance(error, commands.BadArgument):
            await utils.lib.send_error(ctx, f'オプション引数は0か1を指定して下さい（無しでも可）\n\n{error}')


def setup(bot):
    bot.add_cog(admin_toolsCog(bot))

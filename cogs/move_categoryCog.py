import discord
from discord.ext import commands


class move_categoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.min_length = 20
        self.del_after = 60

    # 日報を書いたら日報のあるカテゴリをサーバ―情報カテ範囲内の最上位に移動する
    # 日報の定義
    # ・チャンネル名が'日報'で終わるチャンネルに書かれたメッセージ
    # ・min_length文字以上のメッセージ

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if not message.channel.name.endswith('日報'):
            return

        # サーバー情報カテの一番上と一番下のpositionを求める（つまり、仕切りカテの直下と直上）
        if not (upper_cate := message.channel.guild.get_channel(self.bot.info_start_cate_id)):
            return
        top_position = upper_cate.position + 1
        if not (lower_cate := message.channel.guild.get_channel(self.bot.info_end_cate_id)):
            return
        bottom_position = lower_cate.position - 1
        # 現在のpostionが範囲外なら無視
        current_position = message.channel.category.position
        if current_position < top_position or current_position > bottom_position:
            return

        if len(message.content) < self.min_length:
            result = f'{self.min_length}文字以下ですのでカテゴリは移動しませんでした'
            await message.channel.send(result, delete_after=self.del_after)
            return

        # これ以下、日報の体裁として問題ない投稿があったとして処理
        if message.channel.category.position == top_position:
            result = '※ 最上位でしたのでカテゴリ移動はできませんでした'
        else:
            try:
                await message.channel.category.edit(position=top_position)
            except Exception:
                result = '恐らく権限問題でカテゴリの移動ができませんでした\n管理者にお問い合わせください'
            else:
                result = '※ カテゴリを最上位に移動しました'

        title = f'{message.author.mention}さん\n**{result}**\n'
        embed = discord.Embed(
            description='日報のご投稿ありがとうございました。',
            color=self.bot.BORDER_COLOR
        )
        embed.add_field(
            name='お願い',
            inline=False,
            value=f'''
日報ご投稿時には必ず<#{self.bot.bump_channel_id}>からbumpをお願いします。
（前回bumpから2時間以上経過していない場合エラーになりますがその場合でも確認の為bumpしてエラーを出しておいて下さい）
'''
        )
        embed.set_footer(
            text=f'※ このメッセージは{self.del_after}秒後に自動削除されます'
        )
        await message.channel.send(title, embed=embed, delete_after=self.del_after)


def setup(bot):
    bot.add_cog(move_categoryCog(bot))

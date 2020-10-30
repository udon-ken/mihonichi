import discord
from discord.ext import commands
from datetime import datetime, timedelta
import re

REPORT_MIN_LENGTH = 60 # 日報最低文字数
MESSAGE_LIFETIME = 60 # 受け付け完了メッセージ削除秒数

'''
・適正な日報を書いた場合の動作
　- 日報のあるカテゴリをサーバ―情報カテ範囲内の最上位に移動する
　- 日報の先頭から規定文字数をサマリーとしてサマリー用チャンネルに転記する
・適正な日報の定義
　- 適正なサーバー日報チャンネルに書かれている事
    - 文字数が REPORT_MIN_LENGTH 以上である事
'''


class ReportingSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """メッセージが投稿されたら自動処理"""
        if message.author.bot:
            return
        if isinstance(message.channel, discord.DMChannel): # DM拾うとchannel.nameが無いのでエラーになる
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
        # 現在のpostionが範囲外（つまりチャンネル名が日報だがサーバー日報とは違う）なら無視
        if not(top_position <= message.channel.category.position <= bottom_position):
            return
        if len(message.content) < REPORT_MIN_LENGTH:
            title = f'{message.author.mention}さん\n**投稿が{REPORT_MIN_LENGTH}文字以下ですのでカテゴリは移動しませんでした**'
            msg_body = '''
書き直す場合は、今回の投稿を削除して新規に再投稿して下さい（編集した場合、システムに認識されずこのカテゴリが一番上に移動しません）。
'''
            await self._put_result(message.channel, title, msg_body)
            return

        # これ以下、日報の体裁としては問題ない投稿があったとして処理
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
        msg_body = '日報のご投稿ありがとうございました。'

        await self._put_result(message.channel, title, msg_body)
        await self._put_report_summary(message)

    async def _put_result(self, ch, title, msg_body):
        """処理結果の表示"""
        embed = discord.Embed(
            description=msg_body,
            color=self.bot.config['border_color']
        )
        embed.add_field(
            name='【　お　願　い　】',
            inline=False,
            value=f'''
日報ご投稿時には必ず<#{self.bot.bump_channel_id}>からbumpをお願いします。
（前回bumpから2時間以上経過していない場合エラーになりますが、その場合でも確認の為bumpしてエラーを出しておいて下さい）
'''
        )
        embed.set_footer(
            text=f'※ このメッセージは{MESSAGE_LIFETIME}秒後に自動削除されます'
        )
        await ch.send(title, embed=embed, delete_after=MESSAGE_LIFETIME)

    async def _put_report_summary(self, message):
        """日報サマリー（最新日報）への投稿 日報最低文字数分を出力"""
        if not(summary_ch := self.bot.get_channel(self.bot.report_summary_ch_id)):
            return

        jst = datetime.utcnow() + timedelta(hours=9)
        ch_name = message.channel.name

        summary = message.content[:REPORT_MIN_LENGTH]
        summary = re.sub('\n{2,}', '\n', summary)

        body = f'```{summary} ……```[...続きはこちらから]({message.jump_url})'
        embed = discord.Embed(
            title=ch_name,
            url=message.jump_url,
            description=body,
            color=self.bot.config['border_color']
        )
        embed.set_footer(
            icon_url=message.author.avatar_url_as(static_format='png'),
            text=f"Posted by {message.author.name}　{jst.strftime('%Y/%m/%d %H:%M')}"
        )
        await summary_ch.send(embed=embed)

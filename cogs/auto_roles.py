import discord
from discord.ext import commands, tasks
import asyncio
from datetime import datetime, timedelta

BEGINNER_LIMIT = 60 # 初心者とみなす日数


class AutoRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.auto_roles.start()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """join時に初心者ロールを付ける"""
        if member.bot:
            return
        if datetime.utcnow() - member.created_at > timedelta(days=BEGINNER_LIMIT):
            return
        if not(role := discord.utils.get(member.guild, name=self.bot.config['beginner_role_name'])):
            return
        await asyncio.sleep(3) # 他ボットとの競合回避
        await member.add_roles(role)

    @tasks.loop(seconds=3600)
    async def auto_roles(self):
        """定期的にロールチェックしてプロフ・初心者ロールの整合性を取る
        チェックする性別ロール名、チェックするチャンネル、付与するロールを渡すだけ
        性別ついてないとチェックしない事になるが、それは逆に好都合"""
        await self.bot.wait_until_ready()
        await asyncio.sleep(1) # on_radyイベント中に取得する情報がある為、少し待つ

        # 男性処理
        await self._role_operation(
            target_sex=self.bot.config['man_role_name'],
            target_ch=self.bot.config['man_prof_ch_name'],
            target_role=self.bot.config['man_exist_prof_role_name']
        )
        # 女性処理
        await self._role_operation(
            target_sex=self.bot.config['woman_role_name'],
            target_ch=self.bot.config['woman_prof_ch_name'],
            target_role=self.bot.config['woman_exist_prof_role_name']
        )

    async def _role_operation(self, target_sex, target_ch, target_role):
        """プロフロール・初心者ロール操作
        引数 チェックする性別ロール名、チェックするチャンネル、付与するロール"""
        try:
            GUILD = self.bot.GUILD # このボットが扱うたった一つのギルド（何回も出るので定義）
            no_prof_role = discord.utils.get(GUILD.roles, name=self.bot.config['no_prof_role_name']) # プロフ無しロール
            beginner_role = discord.utils.get(GUILD.roles, name=self.bot.config['beginner_role_name']) # 初心者ロール
            # 以下、引数で渡されたもの
            sex_role = discord.utils.get(GUILD.roles, name=target_sex) # 対象性別ロール
            prof_ch = discord.utils.get(GUILD.channels, name=target_ch) # プロフch
            exist_prof_role = discord.utils.get(GUILD.roles, name=target_role) # プロフ有ロール

            count_add = 0
            count_remove = 0
            profs = {}
            async for message in prof_ch.history(limit=2000):
                if '【エロイプ' in message.content:
                    profs[message.author.id] = message.id

            for member in sex_role.members:
                if member.bot:
                    continue
                # プロフロール操作
                if profs.get(member.id): # プロフ有り
                    if exist_prof_role not in member.roles: # プロフ有りロール無し
                        await member.add_roles(exist_prof_role) # 付与
                        count_add += 1
                        print(f'＋ {member} さんに{exist_prof_role}ロールを付与しました')
                    if no_prof_role in member.roles: # プロフ無しロールが付いてれば
                        await member.remove_roles(no_prof_role) # 削除
                else: # プロフ無し
                    if exist_prof_role in member.roles: # ロール有り（プロフ削除したという事）
                        await member.remove_roles(exist_prof_role) # 剥奪
                        count_remove += 1
                        print(f'－ {member} さんから{exist_prof_role}を削除しました')
                    if no_prof_role not in member.roles: # プロフ無しロールが無ければ
                        await member.add_roles(no_prof_role) # 付与
                # 初心者ロール操作
                if datetime.utcnow() - member.created_at > timedelta(days=BEGINNER_LIMIT): #初心者期間じゃない
                    if beginner_role in member.roles: # 初心者ロールがある
                        await member.remove_roles(beginner_role) # 削除
                        print(f'－ {member} さんから{beginner_role}を削除しました')
                else:
                    if beginner_role not in member.roles: # 初心者ロールが無い
                        await member.add_roles(beginner_role) # 追加
                        print(f'＋ {member} さんに{beginner_role}を付与しました')

            print(f'{prof_ch.name}チェック完了 追加：{count_add}名　削除：{count_remove}名　total：{len(exist_prof_role.members)}名')
        except Exception as e:
            print(f'error on role_operation\n{e}')

import discord
from discord.ext import commands, tasks
import asyncio
from datetime import datetime, timedelta


class auto_rolesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.beginner_role_limit = 600 # 初心者とみなす日数
        self.auto_roles.start()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return
        if datetime.utcnow() - member.created_at < timedelta(days=self.beginner_role_limit):
            await asyncio.sleep(3)
            if role := discord.utils.get(member.guild, name=self.bot.beginner_role_name):
                await member.add_roles(role)

    # 定期的にロール操作
    @tasks.loop(seconds=180)
    # @commands.command(aliases=['ro'])
    async def auto_roles(self):
        # チェックする性別、チェックするチャンネル、付与するロール
        # 男性処理
        await self.role_operation(
            target_sex=self.bot.man_role_name,
            target_ch=self.bot.man_prof_ch_name,
            target_role=self.bot.man_exist_prof_role_name
        )
        # 女性処理
        await self.role_operation(
            target_sex=self.bot.woman_role_name,
            target_ch=self.bot.woman_prof_ch_name,
            target_role=self.bot.woman_exist_prof_role_name
        )

    # プロフロール・初心者ロール操作
    async def role_operation(self, target_sex, target_ch, target_role):
        try:
            GUILD = self.bot.GUILD # このボットが扱うたった一つのギルド（何回も出るので定義）
            no_prof_role = discord.utils.get(GUILD.roles, name=self.bot.not_prof_role_name) # プロフ無しロール
            beginner_role = discord.utils.get(GUILD.roles, name=self.bot.beginner_role_name) # 初心者ロール
            # 以下、引数で渡されたもの
            sex_role = discord.utils.get(GUILD.roles, name=target_sex) # 対象性別
            prof_ch = discord.utils.get(GUILD.channels, name=target_ch) # プロフch
            exist_prof_role = discord.utils.get(GUILD.roles, name=target_role) # プロフ有ロール

            count_add = 0
            count_remove = 0
            profs = {}
            async for message in prof_ch.history(limit=2000):
                profs[message.author.id] = message.id

            for member in sex_role.members:
                if member.bot:
                    continue
                # プロフロール操作
                if profs.get(member.id): # プロフ有り
                    if exist_prof_role not in member.roles: # プロフ有りロール無し
                        await member.add_roles(exist_prof_role) # 付与
                        count_add += 1
                        print(f'＋ {member} さんに{exist_prof_role}ロールを新規付与しました')
                    if no_prof_role in member.roles: # プロフ無しロールが付いてれば
                        await member.remove_roles(no_prof_role) # 削除
                        count_add += 1
                else: # プロフ無し
                    if exist_prof_role in member.roles: # ロール有り
                        await member.remove_roles(exist_prof_role) # 剥奪
                        count_remove += 1
                        print(f'－ {member} さんから{exist_prof_role}を削除しました')
                    if no_prof_role not in member.roles: # プロフ無しロールが無ければ
                        await member.add_roles(no_prof_role) # 付与
                # 初心者ロール操作
                if datetime.utcnow() - member.created_at > timedelta(days=self.beginner_role_limit): #初心者期間じゃない
                    if beginner_role in member.roles: # 初心者ロールがある
                        await member.remove_roles(beginner_role) # 削除
                        print(f'－ {member} さんから{beginner_role}を削除しました')
                else:
                    if beginner_role not in member.roles: # 初心者ロールが無い
                        await member.add_roles(beginner_role) # 追加
                        print(f'＋ {member} さんに{beginner_role}を付与しました')

            print(f'{prof_ch.name}チェック完了 追加：{count_add}名　削除：{count_remove}名　total：{len(profs)}名')
        except Exception as e:
            print(f'error on role_operation\n{e}')


def setup(bot):
    bot.add_cog(auto_rolesCog(bot))

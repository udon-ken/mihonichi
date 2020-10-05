import discord


# エラーメッセージ
async def send_error(ctx, description: str = '本文無し'):
    embed = discord.Embed(
        title='⚠ ERROR!!',
        description=description,
        color=0xff0000
    )
    await ctx.send(embed=embed)
    return

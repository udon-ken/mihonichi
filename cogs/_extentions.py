from cogs.admin_tools import AdminTools
from cogs.auto_roles import AutoRoles
from cogs.reporting_system import ReportingSystem


def setup(bot):
    bot.add_cog(AdminTools(bot))
    bot.add_cog(AutoRoles(bot))
    bot.add_cog(ReportingSystem(bot))

# このファイルのファイル名先頭のアンダースコアは位置を調整したいだけの理由

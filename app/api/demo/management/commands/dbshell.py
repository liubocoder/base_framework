import django.conf
import readline
import wcwidth
from tabulate import tabulate

from django.db import ConnectionHandler, ConnectionProxy
from django.core.management import BaseCommand

"""

基于 postgresql的一个db 命令行查询工具


"""

exit_cmds = ["exit", "q", "quit"]
table_theme = "psql"

def printAsTable(tabs, datas):
    table = tabulate(datas, headers=tabs, tablefmt=table_theme)
    print(table)

class BaseSqlExecutor:

    def isTagCmd(self, cmd: str):
        return False

    def exec(self, connection, cursor, cmd):
        sql = self.buildSql(cmd)
        print(sql)
        cursor.execute(sql)
        connection.commit()
        self.doResult(cursor)

    def doResult(self, cursor):
        tabs = []
        for col in cursor.description:
            tabs.append(col[0])
        datas = []
        for row in cursor.fetchall():
            datas.append(list(row))
        printAsTable(tabs, datas)

    def buildSql(self, cmd):
        return cmd

class HelpExecutor(BaseSqlExecutor):
    def isTagCmd(self, cmd: str):
        return cmd.startswith("help")
    def exec(self, connection, cursor, cmd):
        tab = ["指令", "描述", "快捷指令"]
        datas = [
            ["show databases;", "展示所有数据库", "show dbs;"],
            ["show database;", "当前激活连接的数据库", "show db;"],
            ["use <database name>;", "连接新的数据库", ""],
            ["show tables;", "展示当前数据库的所有表", "show tabs; show tb; show tabs;"],
            ["desc <table name>;", "展示表的基础定义", ""],
            ["select ...;", "数据库查询语句...默认limit 20", ""],
            ["ctrl+c", "清空之前的输入，上述指令未用;结束时，可换行继续输入", ""],
            ["exit", "退出", "quit 或 q 或组合按键 ctrl+d"],
            ["help", "帮助", ""]
        ]
        printAsTable(tab, datas)
class SelectExecutor(BaseSqlExecutor):

    def isTagCmd(self, cmd: str):
        return cmd.startswith("select") or cmd.startswith("SELECT")

    def buildSql(self, cmd):
        if "limit" not in cmd or "LIMIT" not in cmd:
            cmd = cmd.strip(";")
            return f"{cmd} limit 20;"
        return cmd

class DescExecutor(BaseSqlExecutor):

    def isTagCmd(self, cmd: str):
        return cmd.startswith("desc") or cmd.startswith("DESC")

    def buildSql(self, cmd):
        tab = cmd.strip(";").strip("desc").strip("DESC").strip()
        return 'SELECT column_name, data_type, character_maximum_length,is_nullable, ordinal_position ' \
               f'FROM "information_schema"."columns" WHERE "table_name" = \'{tab}\''
    def doResult(self, cursor):
        tabs = []
        for col in cursor.description:
            tabs.append(col[0])
        datas = []
        for row in cursor.fetchall():
            datas.append(list(row))
        datas.sort(key=lambda it: it[-1])
        table = tabulate(datas, headers=tabs, tablefmt=table_theme)
        print(table)

class ShowTabsExecutor(BaseSqlExecutor):
    def isTagCmd(self, cmd: str):
        return "show tbs" in cmd or "show tb" in cmd or "show tables" in cmd  or "show tabs" in cmd

    def buildSql(self, cmd):
        return "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';"

    def doResult(self, cursor):
        printAsTable(["table"], [[row[0]]for row in cursor.fetchall()])

helper = HelpExecutor()
SQLExecutors = [SelectExecutor(), ShowTabsExecutor(), DescExecutor()]

class Command(BaseCommand):
    cursor:CursorBase|None = None
    connection = None
    curDbName = "default"
    help = (
        "数据库sql语句执行shell"
    )

    def initCursor(self, dbName="default"):
        self.print(f"数据库已切换，当前数据库: {dbName}")
        if self.cursor and dbName == self.curDbName:
            return
        if self.cursor is not None:
            self.cursor.close()
            self.connection.close()
        connection = ConnectionProxy(ConnectionHandler(), dbName)
        self.connection = connection
        self.cursor = connection.cursor()
        self.curDbName = dbName

    def add_arguments(self, parser):
        super().add_arguments(parser)

    def handle(self, **options):
        tempCmd = []
        self.initCursor()
        while True:
            try:
                cmd = input(">>>")
            except Exception as e:
                self.print("退出")
                break
            except KeyboardInterrupt as ke:
                tempCmd.clear()
                self.print("已清空缓存指令，退出请用ctrl+d")
                continue
            if cmd in exit_cmds:
                self.print(cmd)
                break
            if helper.isTagCmd(cmd):
                helper.exec(connection=self.connection, cursor=self.cursor, cmd=cmd)
                continue
            if cmd.endswith(";"):
                tempCmd.append(cmd)
                execCmd = " ".join(tempCmd)
                try:
                    execCmd = execCmd.strip()
                    self.print(f"输入：{execCmd}")
                    self.exec(execCmd)
                except Exception as e:
                    self.stderr.write(f"出现异常：{e}")
                    self.connection.commit()
                tempCmd.clear()
            else:
                tempCmd.append(cmd)
        self.cursor.close()
        self.connection.close()


    def print(self, obj):
        self.stdout.write(obj)

    def exec(self, ecmd:str):
        if "show dbs" in ecmd or "show databases" in ecmd:
            printAsTable(["database"], [[it] for it in django.conf.settings.DATABASES.keys()])
            return
        if "show db" in ecmd or "show database" in ecmd:
            self.print(f"当前数据库：{self.curDbName}")
            return
        if ecmd.startswith("use "):
            dbname = ecmd.replace("use ", "").replace(";", "")
            self.initCursor(dbname)
            return

        for exe in SQLExecutors:
            if exe.isTagCmd(ecmd):
                exe.exec(self.connection, self.cursor, ecmd)
                return

        self.print("不支持的命令")
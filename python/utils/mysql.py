# -*- coding: utf-8 -*-
import pymysql

from utils.read_config import ReadConfig


class Mysql(object):

    def __init__(self):
        cfg = ReadConfig()
        if not cfg.mysql():
            self.conn = pymysql.connect(
                host='localhost',
                user='slurm',
                password='123456',
                database='slurm_acct_db',
                charset='utf8',
                port=3306
            )
        else:
            mysql_cfg = cfg.mysql()
            self.conn = pymysql.connect(
                host=mysql_cfg.get('host'),
                user=mysql_cfg.get('user'),
                password=mysql_cfg.get('pwd'),
                database=mysql_cfg.get('db'),
                charset=mysql_cfg.get('charset'),
                port=int(mysql_cfg.get('port'))
            )
        self.cursor = self.conn.cursor()

    def query(self, sql):
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            return res
        except Exception as e:
            return None

    def close(self):
        self.cursor.close()
        self.conn.close()

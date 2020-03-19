# coding:utf-8

import pymysql


class DB(object):
    """
    用于连接数据库
    """
    def __init__(self, database):
        """
        :param database:需要连接的数据库名称
        """
        self.connect = self.establish_connect(database)
        self.cursor = self.connect.cursor()

    def establish_connect(self, database):
        """

        :param database: 需要连接的数据库名称
        :return: 返回连接
        """
        self.connect = pymysql.Connect(host="127.0.0.1",
                                       user="root",
                                       password="password",
                                       database=database,
                                       port=3306,
                                       charset="utf8")
        return self.connect

    def execute_sql(self, sql):
        """
        :param self
        :param sql: 执行的sql语句
        :return: 返回affect_rows
        """
        try:
            affected_rows = self.cursor.execute(sql)
        except Exception as e:
            self.connect.rollback()
            print(e)

        else:
            self.connect.commit()
            return affected_rows

    def get_one(self):
        """
        获取sql语句的结果集数据,一个结果
        :return:
        """
        return self.cursor.fetchone()[0]

    def get_all(self):
        """
        获取sql语句的结果集数据,所有结果
        :return:
        """
        return self.cursor.fetchall()


if __name__ == "__main__":
    pass
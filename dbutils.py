import time

import pymongo
import pymysql


class Mongo(object):
    def __init__(self):
        self.db_name = "sensor"
        self.db_col = "temp_hum"
        self.client = pymongo.MongoClient('mongodb://????:????@????', 27017,
                                          serverSelectionTimeoutMS=5000, socketTimeoutMS=5000)
        print('Mongo数据库连接成功……')
        self.db = self.client[self.db_name]
        self.col = self.db[self.db_col]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('关闭MongoDB连接')
        self.client.close()

    def save_data(self, data):
        x = self.col.insert_one(data)
        print(x, data)

    def read_all(self):
        rows = self.col.find().sort('_id', -1).limit(20)
        dataList = []
        # print(rows[1]['_id'])
        for row in rows:
            dataList.append(list(row.values()))
        return dataList

    def read_ones(self):
        rows = self.col.find().sort('_id', -1).limit(1)  # 倒序以后，只返回1条数据
        dataList = []
        # print(rows[1]['_id'])
        for row in rows:
            print(row)
            dataList.append(list(row.values()))
        return dataList[0]

    def load_temp_list(self):
        rows = self.col.find().sort('_id', -1).limit(20)
        dataList = []
        for row in rows:
            dataList.append(row['temp'])
        print(dataList)
        return dataList


class MySQL(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='root',
            db='sensor',
            charset='utf8',
        )
        print("MySQL数据库连接成功……")
        self.cursor = self.conn.cursor()  # 创建游标

    def __enter__(self):
        print("__enter__")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__')
        print("关闭MySQL对象连接")
        self.conn.close()

    def read_all(self):
        rows = self.cursor.execute('select * from temp_hum order by _id desc limit 20;')
        print(str(rows) + "条查询")
        res = self.cursor.fetchall()
        rs = []
        for i in range(len(res)):
            rs1 = []
            for j in range(len(res[i])):
                rs1.append(res[i][j])
            rs.append(rs1)
        return rs

    def read_ones(self):
        rows = self.cursor.execute('select * from temp_hum order by _id desc limit 1;')
        print(str(rows) + "条查询")
        res = self.cursor.fetchall()
        for i in range(len(res)):
            rs1 = []
            for j in range(len(res[i])):
                rs1.append(res[i][j])
        return rs1

    def write_ones(self, data):
        rows = self.cursor.execute(
            "insert into temp_hum(_id, temp, hum) values('%d','%d','%d')" % (data[0], data[1], data[2]))
        print("更新" + str(rows) + "条查询")
        self.conn.commit()
        return


if __name__ == '__main__':
    mysql = MySQL()
    data = [int(time.time()), 11, 11]
    mysql.write_ones(data)
    print(mysql.read_ones())

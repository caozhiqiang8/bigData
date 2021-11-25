from sqlalchemy import create_engine
import pymysql
import pandas as pd
import sqlite3

# sqlite数据----dataFram
class SqliteDB1(object):
    def __init__(self, sql, ):
        self.sql = sql

    def connectdb(self):
        engine = create_engine('sqlite:///F:\\PythonObject\\SchoolObject\\db.sqlite3')
        result = pd.read_sql(sql=self.sql, con=engine)
        result = result.fillna(0)
        return result

#数据专程字典
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# sqlite数据查询
class SqliteDB(object):
    def __init__(self, sql,):
        self.sql = sql

    def connectdb(self):
        conn = sqlite3.connect('F:\\PythonObject\\SchoolObject\\db.sqlite3')
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute(self.sql)
        res = cur.fetchall()
        cur.close()
        conn.close()
        return res
    def updatedb(self):
        conn = sqlite3.connect('F:\\PythonObject\\SchoolObject\\db.sqlite3')
        cur = conn.cursor()
        cur.execute(self.sql)
        conn.commit()
        return conn.total_changes


# 数据库链接
# (self,sql,host='gw4.bj.etiantian.net', port=12262, user='schu', passwd='test', db='school', charset='utf8'):
# (self,sql,host='localhost', port=3306, user='root', passwd='qiang520', db='school', charset='utf8'):

class MysqlDB(object):
    def __init__(self, sql,
                 host='123.103.75.152',
                 port=3306,
                 user='schu',
                 passwd='slavep',
                 db='school',
                 charset='utf8',
                 cursorclass=pymysql.cursors.DictCursor):
        self.sql = sql
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        self.charset = charset
        self.cursorclass = cursorclass

    def connectdb(self):
        conn = pymysql.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               passwd=self.passwd,
                               db=self.db,
                               charset=self.charset,
                               cursorclass=self.cursorclass)
        cur = conn.cursor()
        cur.execute(self.sql)
        res = cur.fetchall()
        cur.close
        conn.close
        return res


#链接mysql -----dataFrame
def mysqlDB(sql):
    engine = create_engine(
        'mysql+pymysql://schu:slavep@123.103.75.152:3306/school')
    result = pd.read_sql_query(sql = sql, con = engine)
    return result

#链接sqlite
def sqliteDB(sql):
    engine = create_engine('sqlite:///F:\\PythonObject\\SchoolObject\\db.sqlite3')
    result = pd.read_sql(sql = sql, con = engine)
    return result



con = sqlite3.connect('F:\\PythonObject\\SchoolObject\\db.sqlite3')


#mysql 同步 sqlite数据
def mysqlSqlite(sql, db_name):
    mysqlDB(sql=sql).to_sql(name=db_name, con=con, if_exists='replace', index=False)

    return '同步成功'




if __name__ == '__main__':

    # sql = '''
    #     UPDATE updata_table SET c_time = '2021-02-19 16:51:19' WHERE table_name in ( 'every_day_course','every_day_task')
    # '''
    # print(SqliteDB(sql).updatedb())

    # sql = '''
    # SELECT * FROM "resource_info"
    # '''
    # json_list = sqliteDB(sql=sql)
    # print(json_list)
    # print(json_list.to_json(orient='index'))

    sql = '''
        SELECT s.province as 'name',count(DISTINCT fr.SCHOOL_ID) as 'value'  from franchised_school_info fr,school_info s where fr.school_type in (3,4)   
        and fr.school_id  >50000 and fr.enable = 0  and s.school_id = fr.school_id 
        GROUP BY s.province
                '''
    json_list = mysqlDB(sql=sql)
    print(json_list)
    print(json_list.to_json(orient='index'))
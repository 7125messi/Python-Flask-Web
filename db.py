import pymysql

"""
常用模块：读写mysql
MySQL是当今最流行的关系型数据库，很多重要的事务性数据比如用户信息、订单数据都存在MySQL
一个通用的模块读写MySQL，然后演示了查询数据、新增和更新数据。
"""

def get_conn():
    """
    获取MySQL的链接
    :return: mysql connection
    """
    return pymysql.connect(
        host = '127.0.0.1',
        user = 'root',
        password = 'ydzhao',
        database = 'python_mysql',
        charset = 'utf8'
    )

def query_data(sql):
    """
    根据SQL查询数据并且返回
    :param sql:SQL语句
    :return:list[dict]
    """
    conn = get_conn()
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        conn.close()

def insert_or_update_data(sql):
    """
    执行新增insert或者update的SQL
    :param sql: insert or update sql
    :return: None
    """
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    finally:
        conn.close()

if __name__ == '__main__':
    insert_sql = """
    insert user (name,sex,age,email) values ('xiaodong','man',26,'xiaodong@qq.com');
    """
    insert_or_update_data(insert_sql)

    query_sql = """
    select * from user;
    """
    datas = query_data(query_sql)
    import pprint
    pprint.pprint(datas)

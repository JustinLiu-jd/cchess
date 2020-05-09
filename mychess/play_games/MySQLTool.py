import pymysql


def set_conn():
    return pymysql.connect(host='localhost',
                           user='Justin',
                           password='miracle',
                           database='chinaChess',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)


def close_conn(conn: pymysql.connect):
    conn.close()


def get_all_records(conn: pymysql.connect):
    sql = "select * from record " \
          "order by time desc;"
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def get_len(conn: pymysql.connect):
    sql = "select * from record;"
    cursor = conn.cursor()
    len = cursor.execute(sql)
    return len


def get_page(conn: pymysql.connect, page=0, page_num=15):
    sql = f"select * from record " \
          f"order by time desc, uniID asc " \
          f"limit {page * page_num}, {page_num};"
    print(sql)
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def insert_a_record(conn: pymysql.connect, winner, path):
    sql = f"insert into record (time, whoWin, filePath) " \
          f"values " \
          f"(now(), '{winner}', '{path}');"
    print(sql)
    cursor = conn.cursor()
    success = cursor.execute(sql)
    if success:
        conn.commit()
    return success


def delete_a_record(conn: pymysql.connect, uniID):
    sql = f"delete from record " \
          f"where uniID = {uniID};"
    print(sql)
    cursor = conn.cursor()
    success = cursor.execute(sql)
    if success:
        conn.commit()
    return success


def get_record_path(conn: pymysql.connect, uniID):
    sql = f"select filePath " \
          f"from record " \
          f"where uniID = {uniID};"
    print(sql)
    cursor = conn.cursor()
    num = cursor.execute(sql)
    if num == 1:
        return cursor.fetchone()['filePath']
    else:
        return False

# res = get_page(set_conn())
# for i in res:
#     print(i)

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
    sql = "select * from record"
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def get_page(conn: pymysql.connect, page=0, page_num=15):
    sql = f"select * from record limit {page * page_num}, {page_num};"
    cursor = conn.cursor()
    cursor.execute(sql)
    print(sql)
    return cursor.fetchall()


def insert_a_record(conn: pymysql.connect, winner, path):
    sql = f"insert into record (time, whoWin, filePath) " \
          f"values " \
          f"(now(), '{winner}', '{path}');"
    cursor = conn.cursor()
    success = cursor.execute(sql)
    if success:
        conn.commit()
    print(sql)
    return success


def delete_a_record(conn: pymysql.connect, uniID):
    sql = f"delete from record " \
          f"where uniID = {uniID};"
    cursor = conn.cursor()
    success = cursor.execute(sql)
    if success:
        conn.commit()
    print(sql)
    return success

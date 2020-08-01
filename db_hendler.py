import sqlite3
from sqlite3 import Error



def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn

data_base = r"db/product.db"
conn = create_connection(data_base)

def select_string_in_tb(conn, price):
    cur = conn.cursor()
    cur.execute("SELECT * FROM imgfolga WHERE price=?", (price,))
    rows = cur.fetchall()
    for row in rows:
        print(row)


def max_id(conn, name_table):
    sql = "SELECT MAX(id) FROM " + str(name_table)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    ret = int(rows[0][0])
    return ret

def get_string_fo_id(conn, name_table, id):
    sql = "SELECT * FROM " + str(name_table) +" WHERE id=?"
    cur = conn.cursor()
    cur.execute(sql, (id,))
    rows = cur.fetchall()
    ret = rows[0]
    return ret

def get_callback_fo_user_id(conn, user_id):
    sql = "SELECT * FROM user_data WHERE user_id=?"
    cur = conn.cursor()
    cur.execute(sql, (user_id,))
    rows = cur.fetchall()
    ret = rows[0][2]
    print(rows)
    return rows[0]

def get_string_table_for_elem(conn, table, name_stolb, elem):
    sql = "SELECT * FROM " + str(table) + " WHERE " + str(name_stolb) + "=?"
    print(sql)
    cur = conn.cursor()
    cur.execute(sql, (elem,))
    rows = cur.fetchall()
    print(rows)
    return rows


def search_elem(conn, name_table, search_text):
    sql = "SELECT * FROM " + name_table + " WHERE file_id MATCH '" + search_text + "';"
    cur = conn.cursor()
    rows = cur.fetchall()
    return rows

def add_user(conn, user_id):
    sql = """SELECT * FROM user_data WHERE user_id=?"""
    sql_add = """INSERT INTO user_data(user_id) VALUES(?)"""
    add_data = (str(user_id))
    cur = conn.cursor()
    cur.execute(sql, (user_id,))
    rows = cur.fetchall()
    if len(rows) == 0:
        with conn:
            cur = conn.cursor()
            cur.execute(sql_add, (add_data,))
            return cur.lastrowid


def add_cb_user(conn, user_id, callback_in, message_id):
    sql_update_out = "UPDATE user_data SET callback_in=?, message_id=? WHERE user_id=?"
    cur = conn.cursor()
    cur.execute(sql_update_out, (callback_in, str(message_id), int(user_id)))
    conn.commit()


def update_table(conn, table, name_id_string, column, up_data, id_string):
    sql_update = "UPDATE " + table + " SET " + column + "=? WHERE " + name_id_string + "=?"
    cur = conn.cursor()
    cur.execute(sql_update, (up_data, id_string))
    conn.commit()





id = 'AA'
imggelii = 'imgfolga'
#print(search_elem(conn, imggelii, id))





import sqlite3
from sqlite3 import Error


class ConDB:
    sql_methods = ('SELECT ', 'UPDATE ', ' FROM ', ' WHERE ', '=?', ' SET ', 'MAX', ' MATCH ', 'INSERT INTO ', ' VALUES ')
    data_base = r"db/product.db"


    @classmethod
    def create_con(self):
        try:
            self.conn = sqlite3.connect(self.data_base)
            self.cur = self.conn.cursor()
            print(sqlite3.version)
        except Error as e:
            print(e)
        return self.cur


class DB_select(ConDB):
    def string_with_value(self, select_row, table, row, value):
        sql = self.sql_methods[0] + str(select_row) + self.sql_methods[2] + str(table) + self.sql_methods[3] + str(row) + self.sql_methods[4]
        print(sql)
        self.cur = self.create_con()
        self.cur.execute(sql, (value,))
        rows = self.cur.fetchall()
        return rows


    def max_value(self, name_row, table):
        val_id = '(' + name_row + ')'
        sql = self.sql_methods[0] + self.sql_methods[6] + val_id + self.sql_methods[2] + table + ';'
        print(sql)
        self.cur = self.create_con()
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        return rows[0][0]

    # Метод не реализован до конца (сейчас не работает)
    def search_string(self, select_row, table, where_row, search_test):
        sql = self.sql_methods[0] + str(select_row) + self.sql_methods[2] + str(table) + self.sql_methods[3] + str(
            where_row) + self.sql_methods[7] + "'" + str(search_test) + "';"
        print(sql)
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        return rows


class DB_update(ConDB):
    def string_with_value(self, table, select_row, row, value, set_value):
        sql = self.sql_methods[1] + str(table) + self.sql_methods[5] + str(select_row) + self.sql_methods[4] + self.sql_methods[3] + str(
            row) + self.sql_methods[4]
        print(sql)
        self.cur = self.create_con()
        self.cur.execute(sql, (set_value, int(value)))
        self.conn.commit()


class DB_insert(ConDB):
    def full_string(self, table, rows_in_table, value):
        sql_rows = ', '.join(rows_in_table)
        sql_value = "'"
        for elem in value:
            if elem == None:
                elem = 'None'
            sql_value += elem + "', '"
        sql = self.sql_methods[8] + table + ' (' + sql_rows + ')' + self.sql_methods[9] + '(' + sql_value[:len(sql_value) - 3] + ');'
        print(sql)
        self.cur = self.create_con()
        self.cur.execute(sql)
        self.conn.commit()
        return 'ok'

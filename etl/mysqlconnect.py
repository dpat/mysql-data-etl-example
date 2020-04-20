import mysql.connector


class Mysqlconnect:

    db = mysql.connector.connect(
          host="host",
          user="user",
          passwd="password",
          database="ca_business"
        )
    cursor=db.cursor()

    @classmethod
    def sql_insert(self, sql_call, data):
        self.cursor.execute(sql_call, data)
        self.db.commit()


    @classmethod
    def sql_get_id(self, table, key, value):
        sql_select = "SELECT * FROM `{}` WHERE `{}`='{}' LIMIT 1".format(table,key,value)
        self.cursor.execute(sql_select)
        data = self.cursor.fetchone()
        if data is None:
            return None
        else:
            return data[0]

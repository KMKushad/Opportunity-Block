import sqlite3

con = sqlite3.connect("oblock.db")

cur = con.cursor()

'''
SQL table to store users
account_type is between 0 and 2 for student, organisation, moderator respectively
'''
#cur.execute("CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY AUTOINCREMENT, username varchar(255), password varchar(255), account_type INTEGER)")
cur.execute("INSERT INTO Users (username, password, account_type) VALUES ('kmkushad', 1234, 0)")

con.commit()

cur.close()
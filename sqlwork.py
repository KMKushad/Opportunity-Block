import sqlite3

con = sqlite3.connect(r"C:\Users\kmkus_4e9n0iq\Desktop\Coding\Opportunity-Block\oblock.db")

cur = con.cursor()

'''
SQL table to store users
account_type is between 0 and 2 for student, organisation, moderator respectively
'''
cur.execute("DROP TABLE users")
cur.execute("DROP TABLE user_info")
cur.execute("DROP TABLE posts")

cur.execute("CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY AUTOINCREMENT, username varchar(255), password varchar(255), account_type INTEGER)")
cur.execute("CREATE TABLE IF NOT EXISTS user_info (id INTEGER PRIMARY_KEY, interests varchar(255), aboutme varchar(255))")
cur.execute("CREATE TABLE IF NOT EXISTS posts (message_id INTEGER PRIMARY KEY AUTOINCREMENT, poster_id INTEGER, title varchar(255), content varchar(255), timestamp varchar(255), weights varchar(255))")
print(list(cur.execute("SELECT * FROM Users")))

con.commit()

cur.close()
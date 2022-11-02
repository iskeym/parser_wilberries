import sqlite3

conn = sqlite3.connect('DBwildberries.db')

sql = "CREATE TABLE wildberries (title TEXT, brand TEXT, price TEXT, article TEXT, photo TEXT, link TEXT)"
cursor = conn.cursor()
conn.execute(sql)

conn.close()
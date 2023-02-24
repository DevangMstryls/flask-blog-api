import sqlite3

connection = sqlite3.connect('database/blog.db')


with open('database/schema.sql') as f:
    connection.executescript(f.read())

connection.close()

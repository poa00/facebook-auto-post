import sqlite3

con = sqlite3.connect('articles.db')
cursorObj = con.cursor()
cursorObj.execute("CREATE TABLE post(id integer PRIMARY KEY, title text, price integer, category text, state text, type text, option text, description text, path text, groups text)")
con.commit()
con.close()
import sqlite3

con = sqlite3.connect('articles.db')
cursorObj = con.cursor()
cursorObj.execute("CREATE TABLE post(id integer PRIMARY KEY, title text, price integer, category text, state text, type text, option text, description text, path text, groups text, label text)")
cursorObj.execute("CREATE TABLE settings(user_email_login TEXT,user_password_login TEXT,'language' TEXT,images_path TEXT,binary_location TEXT,driver_location TEXT,time_to_sleep TEXT)")
con.commit()
con.close()
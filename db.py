import sqlite3

con = sqlite3.connect('storage.db')


def add_new_tunnel():
    cur = con.cursor()
    cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")


def init_db():
    cur = con.cursor()
    # Create table
    cur.execute('''CREATE TABLE IF NOT EXISTS tunnel 
                   (tunnel_id text, api_key text, last_request integer)''')

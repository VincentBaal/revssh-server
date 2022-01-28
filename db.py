import sqlite3

con = sqlite3.connect('storage.db')

# Add a new tunnel entry to the local db
def add_tunnel(tunnel_id, api_key, port, last_request):
    cur = con.cursor()
    query = f"INSERT INTO tunnel VALUES ('{tunnel_id}','{api_key}', {port},{last_request})"
    cur.execute(query)
    con.commit()
    cur.close()


# Check db for a row using this port
def is_port_in_use(port):
    cur = con.cursor()
    cur.execute(f"SELECT * FROM tunnel WHERE port = ?", (port,))
    result = cur.fetchone()
    cur.close()
    return result is not None


# Check db for a row containing the tunnel_id
def is_id_in_use(tunnel_id):
    cur = con.cursor()
    cur.execute(f"SELECT * FROM tunnel WHERE tunnel_id = ?", (tunnel_id,))
    result = cur.fetchone()
    cur.close()
    return result is not None


# Get the highest port in use by the clients
def get_last_used_port():
    cur = con.cursor()
    cur.execute("SELECT port FROM tunnel ORDER BY port DESC;")
    port = cur.fetchone()
    cur.close()
    print(str(port))
    if port is None:
        return 9000
    return port[0]


def init_db():
    cur = con.cursor()
    # Create table
    cur.execute('''CREATE TABLE IF NOT EXISTS tunnel 
                   (tunnel_id text, api_key text, port integer, last_request integer)''')
    con.commit()
    cur.close()


# Delete all data from the local DB
def truncate():
    cur = con.cursor()
    cur.execute('''DELETE FROM tunnel''')
    con.commit()
    cur.close()

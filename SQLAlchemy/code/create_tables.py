import sqlite3

# connection to our DB
connection = sqlite3.connect('data.db')

# select/start things
# responsible for executing queries and storing results
cursor = connection.cursor()

# create table with 3 columns if no user exists
# id starts off by being 1
# INTEGER PRIMARY KEY --> auto-create columns
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"

# run the query with one user
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_table)

# save all of our changes into data.db file
connection.commit()

# close DB so it doesn't receive/wait for any more data
connection.close()

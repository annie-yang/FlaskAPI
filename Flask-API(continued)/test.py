import sqlite3

# connection to our DB
connection = sqlite3.connect('data.db')

# select/start things
# responsible for executing queries and storing results
cursor = connection.cursor()

# create table with 3 columns
create_table = "CREATE TABLE users (id int, username text, password text)"

# run the query with one user
cursor.execute(create_table)

# id, username, password
user = (1, 'jose', 'asdf')

# insert user into DB
# each '?' is id, username, and password
insert_query = "INSERT INTO users VALUES (?,?,?)"

# insert the user into table
cursor.execute(insert_query, user)

# many users
users = [
    (2, 'rolf', 'asdf'),
    (3, 'anne', 'xyz')
]

# run the query with many users
cursor.executemany(insert_query, users)

# select * --> go to users table and find every row and select ALL data from each row
select_query = "SELECT * FROM users"

# running select statement and storing results and iterate row
for row in cursor.execute(select_query):
    print(row)

# save all of our changes into data.db file
connection.commit()

# close DB so it doesn't receive/wait for any more data
connection.close()

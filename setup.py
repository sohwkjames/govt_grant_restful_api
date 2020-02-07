# Create the sqlite3 databases.
import sqlite3
conn = sqlite3.connect('households.db')
c = conn.cursor()

c.execute('''CREATE TABLE household
             (id integer PRIMARY KEY,
              household_type varchar NOT NULL,
              CHECK (household_type = "Landed" OR household_type = "Condominium" OR household_type = "HDB"))''')

conn.commit()


c.execute('''CREATE TABLE member
             (id integer PRIMARY KEY,
              household_id integer,
              name varchar NOT NULL,
              FOREIGN KEY(household_id) REFERENCES household(id)
              )''')

conn.commit()

c.close()

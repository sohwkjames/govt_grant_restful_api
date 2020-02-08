# Create the sqlite3 databases.
import sqlite3
conn = sqlite3.connect('households.db')
c = conn.cursor()

c.execute('''CREATE TABLE household
             (id integer PRIMARY KEY,
              HouseholdType varchar NOT NULL,
              CHECK (HouseholdType = "Landed" OR HouseholdType = "Condominium" OR HouseholdType = "HDB"))''')

conn.commit()

c.execute('''CREATE TABLE member
             (id integer PRIMARY KEY,
              household_id integer,
              Name varchar NOT NULL,
              Gender varchar NOT NULL,
              MaritalStatus varchar NOT NULL,
              spouse_id integer REFERENCES member(id),
              OccupationType varchar NOT NULL,
              AnnualIncome integer NOT NULL,
              DOB date NOT NULL,
              FOREIGN KEY(household_id) REFERENCES household(id),
              CHECK (Gender = "M" OR Gender = "F"),
              CHECK (MaritalStatus = "Married" OR Gender = "Single"),
              CHECK (OccupationType = "Unemployed" OR OccupationType = "Student" OR OccupationType = "Employed"),
              CHECK (AnnualIncome >= 0))
              ''')
# Add some fake data.
household_data = [(1, 'HDB'), (2, 'Landed'), (3, 'Condominium')]
c.executemany('INSERT INTO household VALUES (?, ?)', household_data)


#c.execute('''INSERT INTO household(HouseholdType) VALUES ('HDB'),('Landed')''')

conn.commit()



c.close()

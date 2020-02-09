# Create the sqlite3 databases.
import sqlite3
conn = sqlite3.connect('households.db')
c = conn.cursor()

c.execute('''CREATE TABLE household
             (HouseholdID integer PRIMARY KEY,
              HouseholdType varchar NOT NULL,
              CHECK (HouseholdType = "Landed" OR HouseholdType = "Condominium" OR HouseholdType = "HDB"))''')

conn.commit()

c.execute('''CREATE TABLE member
             (MemberID integer PRIMARY KEY,
              HouseholdID integer,
              Name varchar,
              YOB integer,
              MaritalStatus varchar,
              Spouse integer,
              OccupationType varchar,
              AnnualIncome integer,
              Gender varchar,
              FOREIGN KEY(HouseholdID) REFERENCES household(id),
              CHECK (Gender = "M" OR Gender = "F"),
              CHECK (MaritalStatus = "Married" OR MaritalStatus = "Single"),
              CHECK (OccupationType = "Unemployed" OR OccupationType = "Student" OR OccupationType = "Employed")
              )''')
# Add some fake data.
#c.execute('''INSERT INTO household(HouseholdType) VALUES ('HDB'),('Landed')''')

conn.commit()



c.close()

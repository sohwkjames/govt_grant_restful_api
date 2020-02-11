Python version: 3.6.6

Flask version: 1.0.2

### Steps to setup this app locally

1. Install flask.

`$ pip install flask`

2. Check that sqlite3 is installed by entering `sqlite3` into Terminal. If not, install sqlite3. https://mislav.net/rails/install-sqlite3/

3. Run setup.py in the terminal.

`$ python setup.py`

4. Run app.py

`$ python app.py`

5. (Optional) Simulate inserting some data.

`$ python simulate.py`

6. The API can be called using the path http://localhost:5000/.


### Endpoints

| Endpoint            | Verb | Details                                                                                                                                            |
|---------------------|------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| /household/         | POST | Expects a json. Example of expected key value pair: {"HouseholdType":"HDB"}                                                                                                                                     |
| /household/         | GET  |                                                                                                                                                    |
| /household/int    | GET  | Takes the Household ID you wish to look up as integer in the endpoint.                                                                                                                                                   |
| /member/            | POST | Expects a json. Example of expected key value pairs: {"HouseholdID":1, "Name":"James", "YOB":1991, "MaritalStatus":"Married",
        "Spouse":2, "OccupationType":"Employed", "AnnualIncome":30000, "Gender":"M"}                                                                                                                                  |
| /grants/int/int | GET  | Expects 2 integers as search parameters: Maximum household size, and maximum household income.   Use /grants/0/0 to not use any search parameters. |
| /deletehouse/int | GET  | Expects an integer as HouseholdID to delete. Deletes all members in member table that has the HouseholdID. |
| /removemember/int | GET  | Expects an integer as MemberID. Removes the MemberID from it's household by setting the HouseholdID of the member to 0. |


### Assumptions

For endpoint 5, accepting search parameters: The search parameters act as additional restrictions on households that will be returned in the endpoint. For example, if a household qualifies for Elder Bonus and earns $100,000 annual income, that household will not be returned if we call `/grants/0/99999`.


import urllib.request
import json




# Test sending a POST request to add household.
body_list = [{"HouseholdType":"HDB"},
            {"HouseholdType":"Condominium"},
             {"HouseholdType":"Landed"}]
myurl = "http://127.0.0.1:5000/household"
for body in body_list:
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    print (jsondataasbytes)
    response = urllib.request.urlopen(req, jsondataasbytes)

# Test sending a POST request to add members to household
body_list = [{"HouseholdID":1, "Name":"James", "YOB":1991, "MaritalStatus":"Married",
        "Spouse":2, "OccupationType":"Employed", "AnnualIncome":30000, "Gender":"M"},
        {"HouseholdID":1, "Name":"Jane", "YOB":1995, "MaritalStatus":"Married",
        "Spouse":1, "OccupationType":"Employed", "AnnualIncome":40000, "Gender":"F"},
        {"HouseholdID":1, "Name":"Baby Ming", "YOB":2018, "MaritalStatus":"Single",
        "Spouse":0, "OccupationType":"Student", "AnnualIncome":0, "Gender":"F"},
        {"HouseholdID":1, "Name":"Grandpa Tan", "YOB":1950, "MaritalStatus":"Single",
        "Spouse":0, "OccupationType":"Unemployed", "AnnualIncome":0, "Gender":"M"},

        {"HouseholdID":2, "Name":"Single Parent Michelle", "YOB":1981, "MaritalStatus":"Single",
        "Spouse":0, "OccupationType":"Unemployed", "AnnualIncome":3000, "Gender":"F"},
        {"HouseholdID":2, "Name":"Young Student Dave", "YOB":2009, "MaritalStatus":"Single",
        "Spouse":0, "OccupationType":"Unemployed", "AnnualIncome":0, "Gender":"M"}]

myurl = "http://127.0.0.1:5000/member"

for body in body_list:
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    print (jsondataasbytes)
    response = urllib.request.urlopen(req, jsondataasbytes)

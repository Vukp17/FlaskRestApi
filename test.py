import requests
import json

BASE = 'http://127.0.0.1:5000/'

data = [{"votes": 1,"context": "Kocka je bacena","nameOfBook":"Priova pobeda"},
         {"votes": 101,"context": "Bolje biti pijan nego star","nameOfBook":"Koliba" },
        {"votes": 1023, "context": "Kocka je bacena","nameOfBook":"Lakoleba"}]

for i in range(len(data)):
     response = requests.put(BASE + "cite/" + str(i), data[i])
     print(response.json())

response = requests.patch(BASE + "cite/2", { "context": "Mali princ"})
print(response.json())
input()
response = requests.get(BASE + "cite/2",)
print(response.json())
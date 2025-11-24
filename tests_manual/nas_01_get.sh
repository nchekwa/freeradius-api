curl -X 'GET' http://localhost:8000/nas | jq .
#> 200 OK
[
    {"nasname": "3.3.3.3", "shortname": "my-super-nas", "secret": "my-super-secret"},
    {"nasname": "4.4.4.4", "shortname": "my-other-nas", "secret": "my-other-secret"},
    {"nasname": "4.4.4.5", "shortname": "another-nas", "secret": "another-secret"},
]
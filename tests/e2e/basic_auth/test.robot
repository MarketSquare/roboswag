*** Settings ***
Library  ..${/}results${/}basic_auth${/}RoboswagTestAPI${/}endpoints${/}Users.py    http://127.0.0.1:8000


*** Test Cases ***
Missing auth
    Users Me    exp_status=401    validate_schema=False

User and password from kwargs
    Users Me    user=testuser    password=1234pass

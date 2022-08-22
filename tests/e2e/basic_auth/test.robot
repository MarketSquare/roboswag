*** Settings ***
Library  ..${/}results${/}basic_auth${/}RoboswagTestAPI${/}endpoints${/}Users.py    http://127.0.0.1:8000


*** Test Cases ***
Get user
    Users Me

*** Settings ***
Library  ..${/}results${/}custom_id${/}RoboswagTestAPI${/}endpoints${/}Items.py    http://127.0.0.1:8000


*** Test Cases ***
Simple test
    Read Item    1

Invalid input
    Read Item    string    exp_status=422

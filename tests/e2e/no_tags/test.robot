*** Settings ***
Library  ..${/}results${/}no_tags${/}RoboswagTestAPI${/}endpoints${/}Items.py    http://127.0.0.1:8000


*** Test Cases ***
Simple test
    Read Item Items Item Id Get    1

Invalid input
    Read Item Items Item Id Get    string    exp_status=422

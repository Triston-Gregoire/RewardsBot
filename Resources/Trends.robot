*** Settings ***
Resource    ../resources/common.robot
Library    ../src/Trends.py
Resource    common.robot


*** Keywords ***
Setup Search Terms
    load search terms

Search Trends
    [Arguments]    ${mode}    ${count}
    FOR    ${i}    IN RANGE    ${count}
        ${query} =    Get Next Term    ${mode}
        Submit Query    ${query}
        ${time}    generate random string    2    123456789
        sleep    ${time}s
    END




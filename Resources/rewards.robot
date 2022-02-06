*** Settings ***
Resource    common.robot
Resource    Trends.robot

*** Keywords ***

Run Searches
    [Arguments]    ${username}    ${password}    ${browser}    ${mode}    ${count}
    Init Webdriver    ${browser}    ${mode}
    Sign Into Microsoft Account    ${username}    ${password}
    Visit Bing
    Search Trends    ${mode}    ${count}
    sleep    5s
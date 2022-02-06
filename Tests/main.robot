*** Settings ***
Resource    ../Resources/rewards.robot
Resource    ../Resources/common.robot
Resource    ../Resources/Trends.robot

Suite Setup    Trends.Setup Search Terms
Test Teardown    Common.Finish


*** Test Cases ***

Desktop
    Run Searches    ${username}    ${password}    ${browser}    desktop    ${desktop_count}

Mobile
    Run Searches    ${username}    ${password}    ${browser}    mobile    ${mobile_count}

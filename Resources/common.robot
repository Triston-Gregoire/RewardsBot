*** Settings ***
Library    ../src/DriverSync.py
Library    ../src/ManageQuery.py
Library    SeleniumLibrary
Library    Collections
Library    OperatingSystem
Library    String

*** Variables ***
${QUERY_FILE}    queries.txt
${MOBILE_HAMBURGER_ID}=     id:mHamburger
${SIGN_IN_ICON} =    id:mectrl_main_trigger
${SIGN_OUT_BUTTON} =    id:mectrl_body_signOut
${EMAIL_TEXT_BOX} =    id:i0116
${SUBMIT_BUTTON} =    id:idSIButton9
${PASSWORD_TEXT_FIELD} =    id:i0118
${NO_BUTTON} =    id:idBtn_Back


*** Keywords ***

Get Driver
    [Arguments]    ${preffered_browser}
    ${driver_path} =    get webdriver    ${preffered_browser}
    log    ${driver_path}
    [Return]    ${driver_path}

Init Driver Log
    [Arguments]    ${driver_path}
    ${driver_log_path} =    DriverSync.get driver log path    ${driver_path}
    log    ${driver_log_path}
    [Return]    ${driver_log_path}

Init Webdriver
    [Arguments]    ${browser}    ${mode}
    ${driver_path} =    Get Driver    ${browser}
    ${options} =    get browser options    ${browser}    ${mode}
#    ${capabilities} =    call method    ${options}    to_capabilities
    create webdriver    ${browser}    executable_path=${driver_path}    options=${options}
    maximize browser window

Visit Bing
    Go To    https://www.bing.com

Sign Out Of Microsoft Account
    click element    ${SIGN_OUT_BUTTON}

Sign Into Microsoft Account
    [Arguments]    ${username}    ${password}
    go to    https://www.microsoft.com
    wait until element is visible    ${SIGN_IN_ICON}
    click element    ${SIGN_IN_ICON}
    wait until element is visible    ${EMAIL_TEXT_BOX}
    input text    ${EMAIL_TEXT_BOX}    ${username}    True
    click button    ${SUBMIT_BUTTON}
    wait until element is visible    ${PASSWORD_TEXT_FIELD}
    input text    ${PASSWORD_TEXT_FIELD}    ${password}    True
    wait until element is visible    ${SUBMIT_BUTTON}
    click button    ${SUBMIT_BUTTON}
    wait until element is visible    ${NO_BUTTON}    timeout=60
    click button    ${NO_BUTTON}
    sleep    5s

Submit Query
    [Arguments]    ${query}
    wait until element is visible    id:sb_form_q
    input text    id:sb_form_q    ${query}
    submit form


Finish
    CLOSE BROWSER

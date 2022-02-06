import logging

from robot.api.deco import keyword
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# os.environ['WDM_LOCAL'] = '1'
browser_map = {
    "edge"  : EdgeChromiumDriverManager(log_level=logging.WARNING),
    "chrome": ChromeDriverManager()
}
supported_browsers = ['chrome', 'edge']
valid_modes = ['desktop', 'mobile']


@keyword
def get_webdriver(preferred_browser='chrome'):
    browser = preferred_browser.casefold()
    driver = browser_map[browser]
    driver_path = driver.install()
    return driver_path


def get_edge_driver():
    print('wtf')
    driver_path = EdgeChromiumDriverManager(log_level=logging.ERROR).install()
    print(driver_path)
    return driver_path


def get_chrome_driver():
    driver_path = ChromeDriverManager().install()
    print("WTF: " + driver_path)
    return driver_path


@keyword
def get_driver_log_path(path):
    rightmost_slash_index = path.rindex("\\")
    dir_path = path[0:rightmost_slash_index + 1]
    new_path = dir_path + "chromedriver_log.txt"
    return new_path


@keyword
def get_browser_options(preferred_browser, mode):
    browser = preferred_browser.casefold()
    if browser in supported_browsers:
        if browser == supported_browsers[0]:
            return get_chrome_options(mode)
        else:
            return get_edge_options(mode)
    raise Exception(
        f"Expected browser to be one of the following: {supported_browsers}. Received {preferred_browser} instead!"
    )


def get_chrome_options(mode):
    param = mode.casefold()
    if param in (option.casefold() for option in valid_modes):
        if param == valid_modes[0]:
            return get_chrome_desktop_options()
        else:
            return get_chrome_mobile_options()
    raise Exception(
        f"Expected browser mode to be one of the following: {valid_modes}. Received {mode} instead!"
    )


def get_edge_options(mode):
    folded_mode = mode.casefold()
    if folded_mode in valid_modes:
        if folded_mode == valid_modes[0]:
            return get_edge_desktop_options()
        else:
            return get_edge_mobile_options()
    raise Exception(
        f"Expected browser mode to be one of the following: {valid_modes}. Received {mode} instead!"
    )


def get_chrome_desktop_options():
    options = webdriver.ChromeOptions()
    return options


def get_chrome_mobile_options():
    options = webdriver.ChromeOptions()
    mobile_emulation = {
        "deviceName": "Pixel 2 XL",
    }
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    return options


def get_edge_desktop_options():
    options = webdriver.EdgeOptions()
    # options.add_argument('-inprivate')
    return options


def get_edge_mobile_options():
    options = webdriver.EdgeOptions()
    mobile_emulation = {
        "deviceName": "Pixel 2 XL"
    }
    # options.add_argument('-inprivate')
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    return options


def get_mobile_capabilities():
    options = get_chrome_mobile_options()
    capabilities = options.to_capabilities()
    return capabilities

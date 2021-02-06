import time
from selenium import webdriver
# Import your username and password of tradingview.com
import credentials
#credentials = credentials.get_credentials()
#username = credentials['hnmwtr999']
#password = credentials['hnm4264wtr@']

username = 'hnmwtr999'
password = 'hnm4264wtr@'



# You should download chromedriver and place it in a high hierarchy folder
chromedriver_path = "C://driver/chromedriver.exe"
# This is the generic url that I mentioned before
url = "https://jp.tradingview.com/chart/yLiKQdYg/#signin"
file_name = r"C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\tradingview"

def open_browser(chromedriver_path):
    chrome_options = webdriver.ChromeOptions()

    preferences = {"download.prompt_for_download": False,
                   "download.default_directory": file_name,
                   "download.directory_upgrade": True,
                   "profile.default_content_settings.popups": 0,
                   "profile.default_content_setting_values.notifications": 2,
                   "profile.default_content_setting_values.automatic_downloads": 1
                   }



    chrome_options.add_experimental_option("prefs", preferences)

    driver = webdriver.Chrome(executable_path=chromedriver_path,
                          chrome_options=chrome_options)
    return driver

def site_login(username,password,url,driver):
    driver.get(url)
    driver.find_element_by_css_selector("#overlap-manager-root > div > div.tv-dialog__modal-wrap.tv-dialog__modal-wrap--"
                                        "contain-size > div > div > div > div > div > div > div:nth-child(1) > "
                                        "div.i-clearfix > div > span").click()
    driver.find_element_by_name('username').send_keys(username)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_class_name('tv-button__loader').click()
    time.sleep(5) # ensure the page loads (bottleneck)
    return driver

def get_csv(driver):
    # driver.find_element_by_xpath('//div[@title="Export screener data to a CSV file"]').click()
    # click taskbar
    driver.find_element_by_css_selector('body > div.js-rootresizer__contents > div.layout__area--topleft > div > div > '
                                        'div > div > svg').click()
    # click csv export on toolbar
    driver.find_element_by_css_selector('#overlap-manager-root > div > span > div.popupMenu-2ot2Uu9Z.menuWrap-1gEtmoET '
                                        '> div > div > div.apply-common-tooltip.common-tooltip-vertical.item-2xPVYue0.item-1dXqixrD '
                                        '> div > div').click()
    time.sleep(4)
    # click datetime format
    driver.find_element_by_css_selector('#overlap-manager-root > div > div > div.dialog-34XTwGTT.dialog-2QwUBM-N.dialog'
                                        '-2APwxL3O.rounded-tXI9mwGE.shadowed-2M13-xZa > div > div.scrollable-2ZZHicYg > '
                                        'div > div:nth-child(3) > div.container-AqxbM340.dropdown-143jb8d-.intent-default'
                                        '-saHBD6pK.border-thin-2A_CUSMk.size-medium-2saizg8j > span > span').click()

    # click ISO date
    driver.find_element_by_css_selector('#overlap-manager-root > div > div > div:nth-child(2) > div > span > '
                                        'div.dropdownMenu-3eseaOZb.menuWrap-1gEtmoET > div > div > div:nth-child(1) >'
                                        ' div > div').click()

    # click csv export
    driver.find_element_by_css_selector('#overlap-manager-root > div > div > div.dialog-34XTwGTT.dialog-2QwUBM-N.dialog-2APwxL3O.rounded-tXI9mwGE.shadowed-2M13-xZa > div > div.footer-1mvnCDqp '
                                        '> div > span > button').click()

if __name__ == '__main__':
    driver_1 = open_browser(chromedriver_path)
    driver_2 = site_login(username,password,url,driver_1)
    time.sleep(7)

    get_csv(driver_2)
    print('csvファイルダウンロード完了')

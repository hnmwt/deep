import time
import predict
from selenium import webdriver

get_csv_dir = r"C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\tradingview"

def open_browser(chromedriver_path):
    chrome_options = webdriver.ChromeOptions()

    preferences = {"download.prompt_for_download": False,
                   "download.default_directory": get_csv_dir,
                   "download.directory_upgrade": True,
                   "profile.default_content_settings.popups": 0,
                   "profile.default_content_setting_values.notifications": 2,
                   "profile.default_content_setting_values.automatic_downloads": 1
                   }
    chrome_options.add_experimental_option("prefs", preferences)
#    chrome_options.add_argument('--headless')
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
    time.sleep(3) # ensure the page loads (bottleneck)
    return driver

def get_csv(driver):
    # driver.find_element_by_xpath('//div[@title="Export screener data to a CSV file"]').click()
    # click taskbar
    driver.find_element_by_css_selector('body > div.js-rootresizer__contents > div.layout__area--topleft > div > div > '
                                        'div > div > svg').click()
    time.sleep(1)
    # click csv export on toolbar
    driver.find_element_by_css_selector('#overlap-manager-root > div > span > div.popupMenu-2ot2Uu9Z.menuWrap-1gEtmoET '
                                        '> div > div > div.apply-common-tooltip.common-tooltip-vertical.item-2xPVYue0.item-1dXqixrD '
                                        '> div > div').click()
    time.sleep(3)
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
    username = 'hnmwtr999'
    password = 'hnm4264wtr@'

    driver_1 = open_browser(chromedriver_path)
    driver_2 = site_login(username,password,url,driver_1)
    time.sleep(7)
    get_csv(driver_2)
    print('csvファイルダウンロード完了')

    df = predict.create_train_data(get_csv_name)  # 取ってきたcsvからdfを作成
    predict.pred(df)  # 予測

    #df = predict.create_train_data(get_csv_name)  # df作成

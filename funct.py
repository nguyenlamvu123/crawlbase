from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from tkinter import messagebox
import time, threading
import tkinter as tk

import time, os, random, requests
from addr import (
    ad, em, pa, em_test, pa_test, lo, get_tok, to, fanpage,
    uidfile, contentfile, spam_done, get_in4, likl_ist,
    comment, like,
)


def readfile(file="uid.txt", mod="r", cont: str or None = None) -> list or None:
    if not mod == 'w':
        assert os.path.isfile(file)
    if mod == "r":
        with open(file, mod, encoding="utf-8") as file:
            lines: list = file.readlines()
        return lines
    else:
        with open(file, mod, encoding="utf-8") as file:
            file.write(cont)


def findelem(driver, xpath, scroll: bool = True):
    element = []
    lan = 0
    # if scroll:
    #     # https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
    #     driver.execute_script("window.scrollTo(0, 30)")
    #     # html = driver.find_element(By.TAG_NAME, 'html')
    #     # html.send_keys(Keys.END)
    while len(element) == 0:
        element = driver.find_elements(By.XPATH, xpath)
        lan += 1
        if lan > 3:
            raise NoSuchElementException
        time.sleep(1)
    return element[0]


def clickkk(driver, xpath):
    element = findelem(driver, xpath)
    try:
        element.click()  # TODO: check elem clicked or not
    except ElementClickInterceptedException:  # https://stackoverflow.com/questions/57741875/selenium-common-exceptions-elementclickinterceptedexception-message-element-cl:
        print_on_gui("ElementClickInterceptedException", text_widget=text_widget)
    # time.sleep(3)
    try:
        driver.execute_script("arguments[0].click();", element)
    except:
        pass


def sendkkkeys(driver, xpath, cont, enter=True):
    element = findelem(driver, xpath)
    element.send_keys(cont)
    if not enter:
        return
    time.sleep(3)  # Thời gian chờ trước khi gửi nội dung
    element.send_keys(Keys.RETURN)
    time.sleep(3)  # Thời gian chờ trước khi gửi nội dung


def chrooome(PROXY: str or None = None):
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager
    from fake_useragent import UserAgent

    options = webdriver.ChromeOptions()
    if PROXY is not None:
        # https://stackoverflow.com/questions/11450158/how-do-i-set-proxy-for-chrome-in-python-webdriver
        options.add_argument('--proxy-server=%s' % PROXY)
##    options.add_experimental_option('excludeSwitches', ['enable-logging'])
##    options.add_argument("--start-maximized")
        
    ua = UserAgent()
    user_agent = ua.random;print(user_agent)
##    https://stackoverflow.com/questions/68566449/how-to-fix-this-browser-or-app-may-not-be-secure-error-when-using-selenium-java
##    https://stackoverflow.com/questions/49565042/way-to-change-google-chrome-user-agent-in-selenium
    options.add_argument(f'--user-agent={user_agent}')
    
##    options.add_argument("--window-size=1000,1080")
##    options.add_argument("--window-position=1000,0")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
##    disable the banner "Chrome is being controlled by automated test software"
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    return webdriver.Chrome(
##        ChromeDriverManager(version='114.0.5735.16').install(),
        service=ChromeService(ChromeDriverManager().install()),
##        chrome_options=options,
        options=options,
        )


def phant():
##    https://stackoverflow.com/questions/71360239/how-to-use-python-selenium-to-automate-login-to-google/71360264#71360264
    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0'
    PHANTOMJS_ARG = {'phantomjs.page.settings.userAgent': UA}
    return webdriver.PhantomJS(desired_capabilities=PHANTOMJS_ARG)


def firefox():
##    https://stackoverflow.com/questions/66209119/automation-google-login-with-python-and-selenium-shows-this-browser-or-app-may
    import geckodriver_autoinstaller
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.service import Service

    service = Service()
    geckodriver_autoinstaller.install()

    options = Options()
    options.add_argument("--headless")
    options.binary_location = '/usr/bin/firefox'
    options.add_argument("download.default_directory=C:\\Music")
    profile = webdriver.FirefoxProfile(
        '/home/nguyenlamvu/snap/firefox/common/.mozilla/firefox/f1yu319w.default-release'
        )
    profile.set_preference("dom.webdriver.enabled", False)
    profile.set_preference('useAutomationExtension', False)
##    profile.set_preference('browser.download.folderList', 2)
##    profile.set_preference('browser.download.manager.showWhenStarting', False)
##    profile.set_preference('browser.download.dir', os.getcwd())
##    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', ('application/vnd.ms-excel'))
##    profile.set_preference('general.warnOnAboutConfig', False)
    profile.update_preferences()
    desired = DesiredCapabilities.FIREFOX
##    https://stackoverflow.com/questions/76802588/python-selenium-unexpected-keyword-argument-executable-path
    return webdriver.Firefox(
        service=service,
        options=options
        )
##    return webdriver.Firefox(
##        options=options,
##        executable_path='/snap/bin/geckodriver'
##        )


def getin4():
    listin4: list = readfile(file=get_in4)
    liklist: list = readfile(file=likl_ist)
    for enu, em__pa in enumerate(listin4):
        em_pa: list = em__pa.split('|')
        em_pa.append(liklist[enu])  # TODO need an other way
        yield em_pa


def stopandkillthread():  # TODO
    pass


def dangnhap(text_widget, email=em_test, passw=pa_test, falivetok=get_tok):
    def gettok():
        req = requests.get('https://2fa.live/tok/' + falivetok)
        return req.json()

    driver = chrooome()
    driver.get(ad)
    sendkkkeys(driver, xpath=em, cont=email, enter=False)
    time.sleep(3)
    sendkkkeys(driver, xpath=pa, cont=passw, enter=False)

    clickkk(driver, xpath=lo)
    token = gettok()
    time.sleep(3)
    element = findelem(driver, to)
    element.send_keys(token["token"])
    time.sleep(2)
    try:
        clickkk(driver, xpath='//button[@value="continue"]')
        print_on_gui('Enter the 6-digit code from the authentication app that you set up._ done', text_widget=text_widget);time.sleep(2)
        clickkk(driver, xpath='//button[@value="Continue"]')
        print_on_gui('If you save this browser, you wont have to enter a code when you log in from this browser again._done', text_widget=text_widget);time.sleep(2)
        clickkk(driver, xpath='//button[@value="Continue"]')
        print_on_gui('//button[@value="Continue"]', text_widget=text_widget);time.sleep(2)
        clickkk(driver, xpath='//button[@value="This was me"]')
        print_on_gui('//button[@value="This was me"]', text_widget=text_widget);time.sleep(2)
        clickkk(driver, xpath='//button[@value="Continue"]')
        print_on_gui('//button[@value="Continue"]', text_widget=text_widget);time.sleep(2)
    except Exception as e:
        print(e)
    print_on_gui(
        str(email) + '_done',
        text_widget=text_widget
    )
    return driver


def thich(
    driver,
    fanpage: str = fanpage,
    li: str = like
):
    if not fanpage.startswith('/'):
        fanpage = '/' + fanpage
    print_on_gui(
        fanpage[1:],
        text_widget=text_widget
    )
    driver.get(ad + fanpage)
    try:
        time.sleep(4)
        clickkk(driver, xpath=li)
        time.sleep(1)
    except NoSuchElementException:
        print_on_gui(
            "Đã thích trang này!",
            text_widget=text_widget
        )
    else:
        print_on_gui(
            '_ liked',
            text_widget=text_widget
        )

    driver.get(ad)
    time.sleep(6)
    return driver


def spam(driver):
    # Đọc danh sách UID từ tệp văn bản và lưu vào danh sách lines
    lines: list = readfile(file=uidfile)
    # Đọc nội dung từ tệp văn bản
    content_lines: list = readfile(file=contentfile)

    # Khởi tạo danh sách để lưu lại những UID đã tương tác
    uids_to_remove = list()  # ["spam_done.txt"]

    # Lặp qua từng giá trị trong danh sách UID
    while lines:
        # Lấy và loại bỏ giá trị đầu tiên từ danh sách
        uid = lines.pop(0).strip()

        # Kiểm tra xem uid có giá trị không rỗng
        if uid:
            if not uid.startswith('/'):
                uid = '/' + uid
            try:
                # Sử dụng giá trị uid
                driver.get(ad + uid)
                time.sleep(10)

                # Chọn ngẫu nhiên một phần từ danh sách nội dung
                random_content = random.choice(content_lines)
                sendkkkeys(
                    driver,
                    xpath=comment,
                    cont=random_content
                )
                print_on_gui(
                    random_content + '_done in ' + str(ad) + str(uid),
                    text_widget=text_widget
                )

                # Sau khi tương tác xong, thêm UID vào danh sách để loại bỏ
                uids_to_remove.append(uid)
            except NoSuchElementException:
                print_on_gui(
                    'stt này', str(ad) + str(uid), 'đã bị tắt comment!',
                    text_widget=text_widget
                )
                continue

    # Đóng trình duyệt sau khi hoàn thành
    driver.quit()

    # Số lượng Comment
    cont = "\n".join(uids_to_remove)
    cont = cont.replace('/', '')
    readfile(file=spam_done, mod="a", cont=cont)
    # Ghi lại danh sách UID còn lại vào tệp uid.txt
    readfile(
        file=uidfile,
        mod="w",
        cont=str([s for s in lines if s not in uids_to_remove])
    )


def print_on_gui(*args, text_widget, sep=" ", end="\n"):
    text = sep.join(args) + end
    # Set the Text widget's state to normal so that we can edit its text
    text_widget.config(state="normal")
    # Insert the text at the end
    text_widget.insert("end", text)
    # Set the Text widget's state to disabled to disallow the user changing the text
    text_widget.config(state="disabled")

def helloCallBack():  # mở cửa sổ popup
    messagebox.showinfo( "Hello Python", "Hello World")
    print_on_gui("Hello Python!", text_widget=text_widget)
    print_on_gui("Hello", "world!", text_widget=text_widget)


### Create a new tkinter window
##root = tk.Tk()
### Create a new `Text` widget
##text_widget = tk.Text(root, state="disabled")
### Show the widget on the screen
##text_widget.pack(fill="both", expand=True)
##B = tk.Button(root, text="Hello", command=helloCallBack)
##B.pack(fill="both", expand=True)

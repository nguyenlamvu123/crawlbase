from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from tkinter import messagebox
import time, threading, pyautogui
import tkinter as tk

import time, os, random, requests
from addr import (
    # em, pa, em_test, pa_test, lo, get_tok, to, fanpage, comment, like,
    uidfile, contentfile, spam_done, get_in4, likl_ist, ad, danhmuc_s, page,
    loca_l, prename, classsanpham, classthongtin, classten, classdanhgiadaban, datasqe_danhgia, classdaban,
)


def readfile(file="uid.txt", mod="r", cont: str or None = None) -> list or str or None:
    if not mod == 'w':
        assert os.path.isfile(file)
    if mod == "r":
        with open(file, mod, encoding="utf-8") as file:
            lines: list = file.readlines()
        return lines
    elif mod == "_r":
        with open(file, mod[1], encoding="utf-8") as file:
            contents = file.read()
        return contents
    else:
        with open(file, mod, encoding="utf-8") as file:
            file.write(cont)


def gethtmlslist_bycategories():
    # https://shopee.vn/Đồ-Chơi-cat.11036932
    for danhmuc in danhmuc_s:
        url_: str = ad + danhmuc
        for trang in range(9):
            url: str = url_ + page + str(trang) if trang > 0 else url_
            brow__ser(url=url)
            time.sleep(15)


def crawlfromhtml():
    from bs4 import BeautifulSoup
    for html in [s for s in os.listdir(loca_l) if s.startswith(prename)]:
        print(html)
        contents = readfile(
            file=os.path.join(loca_l, html),
            mod="_r"
        )
        htMl = BeautifulSoup(contents, 'html.parser')
        sanpham_s = htMl.find_all('li', {"class": lambda x: x and classsanpham in x})
        for sanpham in sanpham_s:
            link = sanpham.find('a', {"href": True});
            print(link.get("href"))
            img_s = link.find_all('img', {'src': True});
            print("len(img_s):", len(img_s))
            # for img in img_s:
            #     print(img.get('src'))
            thongtin_s = link.find_all('div', {"class": classthongtin});
            print("len(thongtin_s):", len(thongtin_s))
            for thongtin in thongtin_s:
                ten = thongtin.find('div', {"class": classten});
                print('ten:', ten.text)
                danhgia_daban = thongtin.find('div', {"class": classdanhgiadaban})
                danhgia = danhgia_daban.find('div', {"data-sqe": datasqe_danhgia})
                daban = danhgia_daban.find('div', {"class": lambda x: x and classdaban in x});
                print("đã bán:", daban.text)


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


def perform_actions(driver, keys):
    actions = ActionChains(driver)
    actions.send_keys(keys)
    time.sleep(2)
    print('Performing Actions!')
    actions.perform()


def delete_cache(driver):
    driver.execute_script("window.open('')")  # Create a separate tab than the main one
    driver.switch_to.window(driver.window_handles[-1])  # Switch window to the second tab
    driver.get('chrome://settings/clearBrowserData')  # Open your chrome settings.
    perform_actions(driver, Keys.TAB * 2 + Keys.DOWN * 4 + Keys.TAB * 5 + Keys.ENTER)  # Tab to the time select and key down to say "All Time" then go to the Confirm button and press Enter
    driver.close()  # Close that window
    driver.switch_to.window(driver.window_handles[0])  # Switch Selenium controls to the original tab to continue normal functionality.


def chrooome(PROXY: str or None = None, incog: bool = False):
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager
    from fake_useragent import UserAgent

#     options = webdriver.ChromeOptions()
#     if PROXY is not None:
#         # https://stackoverflow.com/questions/11450158/how-do-i-set-proxy-for-chrome-in-python-webdriver
#         options.add_argument('--proxy-server=%s' % PROXY)
# ##    options.add_experimental_option('excludeSwitches', ['enable-logging'])
# ##    options.add_argument("--start-maximized")
#
#     ua = UserAgent()
#     user_agent = ua.random;print(user_agent)
# ##    https://stackoverflow.com/questions/68566449/how-to-fix-this-browser-or-app-may-not-be-secure-error-when-using-selenium-java
# ##    https://stackoverflow.com/questions/49565042/way-to-change-google-chrome-user-agent-in-selenium
#     options.add_argument(f'--user-agent={user_agent}')
#
# ##    options.add_argument("--window-size=1000,1080")
# ##    options.add_argument("--window-position=1000,0")
#     options.add_argument("--disable-notifications")
#     options.add_argument("--disable-infobars")
#     # options.add_argument('--headless')
# ##    disable the banner "Chrome is being controlled by automated test software"
#     options.add_argument("--disable-extensions")
#     options.add_argument("--disable-popup-blocking")
#     if incog:
#         options.add_argument("--incognito")
    return webdriver.Chrome(
##        ChromeDriverManager(version='114.0.5735.16').install(),
        service=ChromeService(ChromeDriverManager().install()),
##        chrome_options=options,
        # options=options,
        )


def brow__ser(
    url="https://shopee.vn/search?facet=11036946&keyword=do%20choi&noCorrection=true&page=0",
    browser_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
):
    import webbrowser
    webbrowser.register('custom_browser', None, webbrowser.BackgroundBrowser(browser_path))
    webbrowser.get('custom_browser').open(url)
    # pyautogui.click(x=100, y=200)
    # pyautogui.hotkey('ctrl', 'end')


def phant():
##    https://stackoverflow.com/questions/71360239/how-to-use-python-selenium-to-automate-login-to-google/71360264#71360264
    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0'
    PHANTOMJS_ARG = {'phantomjs.page.settings.userAgent': UA}
    return webdriver.PhantomJS(desired_capabilities=PHANTOMJS_ARG)


##    return webdriver.Firefox(
def firefox(incog: bool = False):
##    https://stackoverflow.com/questions/66209119/automation-google-login-with-python-and-selenium-shows-this-browser-or-app-may
    # import geckodriver_autoinstaller
    # geckodriver_autoinstaller.install()
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.service import Service


    # service = Service(executable_path=r'C:\Users\HLC\Downloads\geckodriver-v0.33.0-win64\geckodriver.exe')
    service = Service()

    # options = webdriver.FirefoxOptions()
    options = Options()
    if incog:
        options.set_preference("browser.privatebrowsing.autostart", True)
    # options.add_argument("--headless")
    # options.binary_location = '/usr/bin/firefox'
    # options.add_argument("download.default_directory=C:\\Music")
    # profile = webdriver.FirefoxProfile(
    #     '/home/nguyenlamvu/snap/firefox/common/.mozilla/firefox/f1yu319w.default-release'
    #     )
    # # profile.set_preference("dom.webdriver.enabled", False)
    # # profile.set_preference('useAutomationExtension', False)
    # profile.set_preference('browser.download.folderList', 2)
    # profile.set_preference('browser.download.manager.showWhenStarting', False)
    # profile.set_preference('browser.download.dir', os.getcwd())
    # profile.set_preference('browser.helperApps.neverAsk.saveToDisk', ('application/vnd.ms-excel'))
    # profile.set_preference('general.warnOnAboutConfig', False)
    # profile.update_preferences()
    # desired = DesiredCapabilities.FIREFOX
##    https://stackoverflow.com/questions/76802588/python-selenium-unexpected-keyword-argument-executable-path
    return webdriver.Firefox(
        service=service,
        options=options,
        )


def getin4():
    listin4: list = readfile(file=get_in4)
    liklist: list = readfile(file=likl_ist)
    for enu, em__pa in enumerate(listin4):
        em_pa: list = em__pa.split('|')
        em_pa.append(liklist[enu])  # TODO need an other way
        yield em_pa


def stopandkillthread():  # TODO
    pass


# def dangnhap(text_widget, email=em_test, passw=pa_test, falivetok=get_tok):
#     def gettok():
#         req = requests.get('https://2fa.live/tok/' + falivetok)
#         return req.json()
#
#     driver = chrooome()
#     driver.get(ad)
#     sendkkkeys(driver, xpath=em, cont=email, enter=False)
#     time.sleep(3)
#     sendkkkeys(driver, xpath=pa, cont=passw, enter=False)
#
#     clickkk(driver, xpath=lo)
#     token = gettok()
#     time.sleep(3)
#     element = findelem(driver, to)
#     element.send_keys(token["token"])
#     time.sleep(2)
#     try:
#         clickkk(driver, xpath='//button[@value="continue"]')
#         print_on_gui('Enter the 6-digit code from the authentication app that you set up._ done', text_widget=text_widget);time.sleep(2)
#         clickkk(driver, xpath='//button[@value="Continue"]')
#         print_on_gui('If you save this browser, you wont have to enter a code when you log in from this browser again._done', text_widget=text_widget);time.sleep(2)
#         clickkk(driver, xpath='//button[@value="Continue"]')
#         print_on_gui('//button[@value="Continue"]', text_widget=text_widget);time.sleep(2)
#         clickkk(driver, xpath='//button[@value="This was me"]')
#         print_on_gui('//button[@value="This was me"]', text_widget=text_widget);time.sleep(2)
#         clickkk(driver, xpath='//button[@value="Continue"]')
#         print_on_gui('//button[@value="Continue"]', text_widget=text_widget);time.sleep(2)
#     except Exception as e:
#         print(e)
#     print_on_gui(
#         str(email) + '_done',
#         text_widget=text_widget
#     )
#     return driver


# def thich(
#     driver,
#     fanpage: str = fanpage,
#     li: str = like
# ):
#     if not fanpage.startswith('/'):
#         fanpage = '/' + fanpage
#     print_on_gui(
#         fanpage[1:],
#         text_widget=text_widget
#     )
#     driver.get(ad + fanpage)
#     try:
#         time.sleep(4)
#         clickkk(driver, xpath=li)
#         time.sleep(1)
#     except NoSuchElementException:
#         print_on_gui(
#             "Đã thích trang này!",
#             text_widget=text_widget
#         )
#     else:
#         print_on_gui(
#             '_ liked',
#             text_widget=text_widget
#         )
#
#     driver.get(ad)
#     time.sleep(6)
#     return driver


# def spam(driver):
#     # Đọc danh sách UID từ tệp văn bản và lưu vào danh sách lines
#     lines: list = readfile(file=uidfile)
#     # Đọc nội dung từ tệp văn bản
#     content_lines: list = readfile(file=contentfile)
#
#     # Khởi tạo danh sách để lưu lại những UID đã tương tác
#     uids_to_remove = list()  # ["spam_done.txt"]
#
#     # Lặp qua từng giá trị trong danh sách UID
#     while lines:
#         # Lấy và loại bỏ giá trị đầu tiên từ danh sách
#         uid = lines.pop(0).strip()
#
#         # Kiểm tra xem uid có giá trị không rỗng
#         if uid:
#             if not uid.startswith('/'):
#                 uid = '/' + uid
#             try:
#                 # Sử dụng giá trị uid
#                 driver.get(ad + uid)
#                 time.sleep(10)
#
#                 # Chọn ngẫu nhiên một phần từ danh sách nội dung
#                 random_content = random.choice(content_lines)
#                 sendkkkeys(
#                     driver,
#                     xpath=comment,
#                     cont=random_content
#                 )
#                 print_on_gui(
#                     random_content + '_done in ' + str(ad) + str(uid),
#                     text_widget=text_widget
#                 )
#
#                 # Sau khi tương tác xong, thêm UID vào danh sách để loại bỏ
#                 uids_to_remove.append(uid)
#             except NoSuchElementException:
#                 print_on_gui(
#                     'stt này', str(ad) + str(uid), 'đã bị tắt comment!',
#                     text_widget=text_widget
#                 )
#                 continue
#
#     # Đóng trình duyệt sau khi hoàn thành
#     driver.quit()
#
#     # Số lượng Comment
#     cont = "\n".join(uids_to_remove)
#     cont = cont.replace('/', '')
#     readfile(file=spam_done, mod="a", cont=cont)
#     # Ghi lại danh sách UID còn lại vào tệp uid.txt
#     readfile(
#         file=uidfile,
#         mod="w",
#         cont=str([s for s in lines if s not in uids_to_remove])
#     )


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

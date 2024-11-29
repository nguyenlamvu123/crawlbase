from coordinate import *

data = pd.read_csv('export-as-csv-20241106062517.csv')
data_ = data.drop_duplicates(subset=['Tên bài hát'])

chrome_service = Service(executable_path='/home/zaibachkhoa/Documents/TikTok/chromedriver-linux64/chromedriver')
driver = webdriver.Chrome(service=chrome_service)
dangnhap = False
so = 0
ttal = data.shape[0]  # number of rows


def loop(row, ttal, rang: tuple or None = None):
    global dangnhap, so
    so += 1
    pr_ing = readfile(file="processing", mod='_r')
    fn = row["Tên bài hát"]
    for sc in ('\\', '/', ')', '(', ):
        fn = fn.replace(sc, '')
    if fn == pr_ing:
        return

    if rang is not None:
        assert len(rang) == 2
        if any([
            so < rang[0],
            so > rang[1],
        ]):
            return

    for tenfile in (
            f'{row["Tên bài hát"]}.csv',
            f'_{row["Tên bài hát"]}.csv',
            f'{fn}.csv',
            f'_{fn}.csv',
    ):
        if tenfile in os.listdir():
            if os.path.getsize(tenfile) > 30000:  # file size is above 50KB -> accept
                return

    readfile(file="processing", mod="w", cont=fn)
    driver.get('https://www.tiktok.com/foryou')
    if not dangnhap:
        input('đăng nhập')  # time.sleep(2)
        dangnhap = True
    else:
        time.sleep(2)

    click_sele(driver, row['Tên bài hát'] + ' ' + row['Tác giả'])
    for _ in range(20):
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    samgiongzon = driver.find_elements(By.XPATH, '//div[@data-e2e="search_top-item"]//a')
    print('################', len(samgiongzon))
    linklist = list()
    for elem in samgiongzon:
        linklist.append(elem.get_attribute('href'))
        # print(linklist[-1])

    df = pd.DataFrame(
        {
            'Tên video': [], 'Link sound': [], 'Tên sound': [], 'Link video': [], 'Tên bài hát': []
        }
    )
    for ind, link in enumerate(linklist):
        newrow = {'Tên bài hát': row['Tên bài hát']}
        print(f"{so}/{ttal}: {row['Tên bài hát']}_{datetime.datetime.now()}")
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        again = True

        while again:
            driver.get(link)
            time.sleep(3)

            try:
                newtab = driver.find_element(By.XPATH, '//h1[@data-e2e="browse-video-desc"]')
                newrow['Tên video'] = newtab.text
                # print('Tên video:', newtab.text)
            except Exception as e:
                newrow['Tên video'] = 'trục trặc'
            try:
                newtab = driver.find_element(By.XPATH, '//h4[@data-e2e="browse-music"]')
                newrow['Tên sound'] = newtab.text
                # print('Tên sound:', newtab.text)
            except Exception as e:
                newrow['Tên sound'] = 'trục trặc'
            try:
                newtab = driver.find_element(By.XPATH, '//h4[@data-e2e="browse-music"]//a')
                newrow['Link sound'] = newtab.get_attribute('href')
                # print('Link sound:', newtab.get_attribute('href'))
            except Exception as e:
                newrow['Link sound'] = 'trục trặc'

            if not all([
                newrow['Tên video'].strip() == '',
                newrow['Tên sound'].strip() == '',
            ]):
                again = False
            else:
                input('vượt captcha')
        newrow['Link video'] = link
        df = df._append(newrow, ignore_index = True)

        time.sleep(2)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        if ind % 50 == 3:
            df.to_csv(f'{fn}.csv', encoding='utf-8', index=False)
    df.to_csv(f'{fn}.csv', encoding='utf-8', index=False)


# loop(data.iloc[49, :], df)
data.apply(loop, ttal=ttal, rang=(3125, 4015), axis=1)

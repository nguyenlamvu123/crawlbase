import json, requests, os, pyautogui, time, webbrowser, threading
# from tkinter import messagebox

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from addr import (
    loca_l, html_local, prename, amongname, sear__ch, masanphamshopee, page, idfromlink, ma__hang, hinh_anh_alib,
    soluongdaban_1688, motvan_1688, mot_1688, findid_class, noiban_class, xpathsanpham_1688,
    debug, allproduct, allproduct_, cra_html, db,
    browser_path, danhmucnhom, danhmucloai, scro, motsolanmomoi, sear_ch, headers, postapi, form_json, getid,
)


def readfile(file="uid.txt", mod="r", cont=None, jso: bool = False):
    if not mod == 'w':
        assert os.path.isfile(file)
    if mod == "r":
        with open(file, mod, encoding="utf-8") as file:
            lines: list = file.readlines()
        return lines
    elif mod == "_r":
        with open(file, mod[1], encoding="utf-8") as file:
            contents = file.read() if not jso else json.load(file)
        return contents
    elif mod == "w":
        with open(file, mod, encoding="utf-8") as fil_e:
            if not jso:
                fil_e.write(cont)
            else:
                json.dump(cont, fil_e, indent=2, ensure_ascii=False)


def initjson():
    readfile(
        file="danhmucnhom.json",
        mod="w",
        cont=[
            {
                'Ma_nhom': str(enu),
                "Ten_nhom": nhom,
            } for enu, nhom in enumerate(danhmucnhom)
        ],
        jso=True
    )
    readfile(
        file="danhmucloai.json",
        mod="w",
        cont=[
            {
                'Ma_loai': str(enu),
                "Ten_loai": loai,
            } for enu, loai in enumerate(danhmucloai)
        ],
        jso=True
    )


def oversimplify_string(s: str) -> str:
    return s.strip().lower()\
        .replace(' ', '')


def adapt2iters(htMl, classinprod_motadai: list or tuple, selenium: bool = False) -> str:
    assert len(classinprod_motadai) == 2
    if not selenium:
        itemname_ite_ = findelem(htMl, xpath=classinprod_motadai[0], scroll=True, getall=True)
        itemvalu_ite_ = findelem(htMl, xpath=classinprod_motadai[1], getall=True)
    else:
        itemname_ite_ = htMl.find_all('span', {"class": classinprod_motadai[0]})
        itemvalu_ite_ = htMl.find_all('span', {"class": classinprod_motadai[1]})
    itemname_ite = iter(itemname_ite_)
    itemvalu_ite = iter(itemvalu_ite_)
    if debug:
        print('yêu cầu hai số lượng (phần mô tả) sau bằng nhau', len(itemname_ite_), len(itemvalu_ite_))
    motadai: str = ''
    while True:  # iname will be "end" if iteration is complete
        iname = next(itemname_ite, "end")
        if iname == "end":
            break
        ivalu = next(itemvalu_ite)
        s: str = iname.text + ': ' + ivalu.text + '\n'
        motadai += s
    return motadai


def parsesoluongdaban(soluongdaban) -> int:
    """
    万件 = x10.000
    件: x1
    """
    assert soluongdaban_1688 in soluongdaban
    soluong: str = soluongdaban[
                   soluongdaban.find(soluongdaban_1688) + len(soluongdaban_1688):
                   ]
    if motvan_1688 in soluong:
        return parse_giaban(soluong) * 10000
    elif mot_1688 in soluong:
        return parse_giaban(soluong) * 1
    else:
        print()


def parse_soluong(soluongdaban: str) -> int:  # just only shopee
    """
    'Đã bán 789'
    'Đã bán 4,3k'
    'Đã bán 1,7tr'
    """
    # assert soluongdaban.startswith('Đã bán ')
    if not soluongdaban.startswith('Đã bán '):
        ret: int = -1
    elif soluongdaban.endswith('k'):
        ret: int = int(float(
            soluongdaban.replace('Đã bán ', '').replace('k', '').replace(',', '.')
        ) * 1000)
    elif soluongdaban.endswith('tr'):
        ret: int = int(float(
            soluongdaban.replace('Đã bán ', '').replace('tr', '').replace(',', '.')
        ) * 1000000)
    else:
        ret: int = int(soluongdaban.replace('Đã bán ', ''))
    return ret


def parse_giaban(giaban: str) -> float:
    # '310.000 ₫'
    # '911 Đã bán'
    # ¥0.58
    return float(''.join([s for s in giaban if s.isdigit() or s in ('.', )]))


def parse_mahang(mahang: str) -> str:
    # 'https://rights.1688.com/trade/workReport.htm?itemId=678314123816'
    iI: str = 'itemId='
    assert iI in mahang
    return mahang.split(iI)[-1]


def post2api(jso):
    try:
        payload = json.dumps(jso)
        response = requests.request("POST", postapi, headers=headers, data=payload)
        if not response.status_code == 200:
            print('><><><><>< !!!!!!!!!', response.status_code, response.text, payload)
        else:
            print(response.text)
    except requests.exceptions.ConnectionError:
        print('><><><><>< !!!!!!!!! requests.exceptions.ConnectionError')


def html2bs4(product: bool = False, tmdt: str = '1688'):
    if tmdt == '1688':
        html_s = [s for s in os.listdir(loca_l) if s.endswith('.html')]
    else:
        html_s = [s for s in os.listdir(loca_l) if all([  # danh sách html các trang chi tiết sản phẩm
            s.endswith('.html'),
            amongname in s,  # tên file chứa chuỗi 'Shopee Việt Nam'
            not s.startswith(prename),  # tên file không bắt đầu bằng chuỗi 'Mua sắm online sản phẩm'
        ])] if product else [s for s in os.listdir(loca_l) if all([  # danh sách html các trang tổng
            s.endswith('.html'),
            amongname in s,  # tên file chứa chuỗi 'Shopee Việt Nam'
            s.startswith(prename),  # tên file bắt đầu bằng chuỗi 'Mua sắm online sản phẩm'
        ])]
    for html in html_s:
        if debug:
            print(html)
        filename = os.path.join(loca_l, html)
        contents = readfile(
            file=filename,
            mod="_r"
        )
        htMl = BeautifulSoup(contents, 'html.parser')
        if cra_html:
            os.rename(
                filename,
                os.path.join(html_local, html),
            )
        yield htMl


def elem2bs4_(contents, dataitemid, classthongtin, classdanhgiadaban, classdaban_, classdaban, datasqe_danhgia, classten, classnoiban, classgiaban):  # 1688
    """
    <a class=classdanhgiadaban>                                            duongdan
        <div class="is-video-container"></div>
        <div class=datasqe_danhgia><img></img></div>                       danhsachhinhanh_
        <div class=classthongtin>                                          thongtin_
            <div class="title-container"></div>
                <div class="icons"></div>
                <div class=classten></div>                                 tencuasanpham
            <div class="offer-properties"></div>
            <div class="offer-labels"></div>
            <div class=classdaban_>                                        soluongdaban_
                <p class=classgiaban></p>                                  giaban
                <p class="offer-attr"></p>
            </div>
        </div>
        <div class=classdaban_>                                            soluongdaban_
            <div class="...classdaban..."></div>                           soluongdaban
            <div class="...classnoiban..."></div>                          noiban
        </div>
    </a>
    """
    htMl = BeautifulSoup(contents, 'html.parser')
    duongdan = htMl.find('a', {"class": classdanhgiadaban})
    duongdancuasanpham = duongdan.get('href')
    thongtin_ = duongdan.find('div', {"class": classthongtin})
    danhsachhinhanh_ = duongdan.find('div', {"class": datasqe_danhgia})
    divclassclearfix = duongdan.find_all('div', {"class": classdaban_})

    tencuasanpham = thongtin_.find('div', {'class': classten}).text
    danhsachhinhanh = danhsachhinhanh_.find('img', {'src': True})

    giaban, soluongdaban, noiban = None, None, None
    for soluongdaban_ in divclassclearfix:
        if giaban is None:
            giaban = soluongdaban_.find('p', {"class": classgiaban})
            if giaban is not None:
                giaban = giaban.text
        if soluongdaban is None:
            soluongdaban = soluongdaban_.find('div', {"class": lambda x: x and classdaban in x})
        if noiban is None:
            noiban = soluongdaban_.find('div', {"class": lambda x: x and classnoiban in x})
            if noiban is not None:
                noiban = noiban.text

    if danhsachhinhanh is None:
        if debug: print(tencuasanpham, "-", duongdancuasanpham, "không tìm thấy hình ảnh")
    else:
        danhsachhinhanh: list = [danhsachhinhanh.get('src'), ]

    scri_jso: dict = form_json(
        Ma_Hang=dataitemid,
        Ten_Hang=tencuasanpham,
        Mo_Ta="<string>",
        Sl_Ban=parsesoluongdaban(soluongdaban.text),
        Danh_Gia=-1,
        Gia_Bl=parse_giaban(giaban),
        Link_Anh=danhsachhinhanh[-1],
        Link_Sp=duongdancuasanpham,
        Dia_Chi_Ban=noiban,
        ID_Nhom=None,  # TODO
        ID_Loai=None,  # TODO
    )
    lis_jso_1688.append(scri_jso)
    if debug:
        lis__jso = lis_jso_1688.copy()


def elem2bs4_tao(contents, dataitemid, classthongtin, classdanhgiadaban, classdaban_, classdaban, datasqe_danhgia, classten, classnoiban):  # taobao
    htMl = BeautifulSoup(contents, 'html.parser')
    thongtin_ = htMl.find('div', classthongtin)
    thongtin = htMl.find('div', classten)
    soluongdaban_ = htMl.find('div', classdaban_)
    danhsachhinhanh_ = htMl.find('div', datasqe_danhgia)
    if danhsachhinhanh_ is None:
        danhsachhinhanh_ = htMl.find('img', hinh_anh_alib)

    tencuasanpham: str = thongtin.text
    if idfromlink in dataitemid:  # 'https://detail.tmall.com/item.htm?id=733825978598&ns=1&abbucket=16'
        Ma_Hang: str = dataitemid[
                       dataitemid.find(idfromlink) + len(idfromlink): dataitemid.find(sear_ch[0])
                       ]
    else:
        Ma_Hang: str = '-1'

    giaban_ = soluongdaban_.find_all('span', classdanhgiadaban)
    giaban = ''.join([g.text for g in giaban_])

    noiban = thongtin_.find('a', classnoiban)
    if noiban is None:
        if debug: print(tencuasanpham, "-", dataitemid, "không tìm thấy nơi bán")
    else:
        noiban = noiban.text

    danhgia_ = soluongdaban_.find('span', classdaban)
    if danhgia_ is None:
        if debug: print(tencuasanpham, "-", dataitemid, "không tìm thấy số lượng đã bán")
        soluotdanhgia = -1
    else:
        soluotdanhgia_ = danhgia_.text
        soluotdanhgia = parse_giaban(soluotdanhgia_)
        if debug:
            if soluotdanhgia == 5:
                print()

    if danhsachhinhanh_ is None:
        danhsachhinhanh: list = ['-1', ]
    else:
        danhsachhinhanh = danhsachhinhanh_.find('img', {'src': True})
        if danhsachhinhanh is None:
            if debug: print(tencuasanpham, "-", dataitemid, "không tìm thấy hình ảnh")
        else:
            danhsachhinhanh: list = [danhsachhinhanh.get('src'), ]

    scri_jso: dict = form_json(
        Ma_Hang=Ma_Hang,
        Ten_Hang=tencuasanpham,
        Mo_Ta="<string>",
        Sl_Ban=soluotdanhgia,
        Danh_Gia=-1,
        Gia_Bl=parse_giaban(giaban),
        Link_Anh=danhsachhinhanh[-1],
        Link_Sp=dataitemid,
        Dia_Chi_Ban=noiban,
        ID_Nhom=None,  # TODO
        ID_Loai=None,  # TODO
    )
    lis_jso_tao.append(scri_jso)


def elem2bs4_alib(contents, dataitemid, classthongtin, classdanhgiadaban, classdaban_, classdaban, datasqe_danhgia, classten, classnoiban):  # alibaba
    assert all([
        isinstance(classthongtin, list),
        all([isinstance(s, dict) for s in (
            classthongtin,
            classten,
            classdanhgiadaban,
            datasqe_danhgia,
            classnoiban,
        )]),
    ])
    htMl = BeautifulSoup(contents, 'html.parser')
    thongtin_ = htMl.find('div', classthongtin)
    # soluongdaban_ = htMl.find('div', {"class": classdaban_})
    danhsachhinhanh_ = htMl.find('a', datasqe_danhgia)
    #
    thongtin = thongtin_.find('a', classten)
    tencuasanpham: str = thongtin.text
    duongdancuasanpham = thongtin.get('href')
    #
    giaban_ = thongtin_.find('div', classdanhgiadaban)
    giaban = giaban_.text.split('-')[0]
    #
    noiban = thongtin_.find('a', classnoiban)
    if noiban is None:
        if debug: print(tencuasanpham, "-", duongdancuasanpham, "không tìm thấy nơi bán")
    else:
        noiban = noiban.text
    #
    danhgia_ = thongtin_.find('span', {"data-spm-anchor-id": True})
    if danhgia_ is None:
        if debug: print(tencuasanpham, "-", duongdancuasanpham, "không tìm thấy đánh giá")
        soluotdanhgia = danhgia = -1
    else:
        danhgia: float = float(
            danhgia_.find('strong').text
        )
        soluotdanhgia_ = danhgia_.text
        soluotdanhgia = int(soluotdanhgia_[soluotdanhgia_.find('(') + 1 : soluotdanhgia_.find(')')])
    #
    danhsachhinhanh = danhsachhinhanh_.find('img', {'src': True})
    if danhsachhinhanh is None:
        if debug: print(tencuasanpham, "-", duongdancuasanpham, "không tìm thấy hình ảnh")
    else:
        danhsachhinhanh: list = [danhsachhinhanh.get('src'), ]

    scri_jso: dict = form_json(
        Ma_Hang=dataitemid,
        Ten_Hang=tencuasanpham,
        Mo_Ta="<string>",
        Sl_Ban=soluotdanhgia,
        Danh_Gia=danhgia,
        Gia_Bl=parse_giaban(giaban),
        Link_Anh=danhsachhinhanh[-1],
        Link_Sp=duongdancuasanpham,
        Dia_Chi_Ban=noiban,
        ID_Nhom=None,  # TODO
        ID_Loai=None,  # TODO
    )
    lis_jso_alib.append(scri_jso)


def elem2bs4(contents, dataitemid, classthongtin, classdanhgiadaban, classdaban_, classdaban, datasqe_danhgia, classten, classnoiban):  # lazada
    htMl = BeautifulSoup(contents, 'html.parser')
    thongtin_ = htMl.find('div', {"class": classthongtin})
    giaban_ = htMl.find('div', {"class": classdanhgiadaban})
    soluongdaban_ = htMl.find('div', {"class": classdaban_})
    danhsachhinhanh_ = htMl.find('div', {"class": datasqe_danhgia})

    thongtin = thongtin_.find('a')
    try:
        tencuasanpham = thongtin.get(classten)
        assert tencuasanpham == thongtin.text
    except:
        tencuasanpham: str = thongtin.text
    duongdancuasanpham = thongtin.get('href')

    giaban = giaban_.find_all('span')
    if not len(giaban) == 1:
        if debug: print(tencuasanpham, "-", duongdancuasanpham, "chứa thông tin khác bên cạnh giá bán")
    else:
        giaban = giaban[0].text

    noiban = soluongdaban_.find('span', {"class": classnoiban})
    if noiban is None:
        if debug: print(tencuasanpham, "-", duongdancuasanpham, "không tìm thấy nơi bán")
    else:
        noiban = noiban.text

    soluongdaban = soluongdaban_.find('span', {"class": classdaban})
    if soluongdaban is None:
        if debug: print(tencuasanpham, "-", duongdancuasanpham, "không tìm thấy số lượng đã bán")
        soluongdaban: int = 0
    else:
        soluongdaban: int = parse_giaban(soluongdaban.text)

    danhsachhinhanh = danhsachhinhanh_.find('img', {'src': True})
    if danhsachhinhanh is None:
        if debug: print(tencuasanpham, "-", duongdancuasanpham, "không tìm thấy hình ảnh")
    else:
        danhsachhinhanh: list = [danhsachhinhanh.get('src'), ]

    scri_jso: dict = form_json(
        Ma_Hang=dataitemid,
        Ten_Hang=tencuasanpham,
        Mo_Ta="<string>",
        Sl_Ban=soluongdaban,
        Danh_Gia=-1,
        Gia_Bl=parse_giaban(giaban),
        Link_Anh=danhsachhinhanh[-1],
        Link_Sp=duongdancuasanpham,
        Dia_Chi_Ban=noiban,
        ID_Nhom=None,  # TODO
        ID_Loai=None,  # TODO
    )
    lis_jso_laz.append(scri_jso)


def gethtmlslist_byjson(looplv1, tmdt, classinprod_motadai, classinprod_danhgia, driver, jso: dict or None = None, i=0, classinprod_ten: str or None = None):
    if jso is None:
        jso: dict = readfile(
            file=looplv1,
            mod="_r",
            jso=True,
        )
    dongmotloattabsaumotsolanmomoi: int = 1
    for jsodict in jso:
        ion: int or None = allproduct_(i)
        if ion is None:
            i += 1
            continue
        else:
            if ion < 0:
                break
            else:
                i += 1
        url = jsodict['Link_Sp']
        if tmdt in ('la', 'alib', 'ta', ):
            assert driver is not None
            if url.startswith('//'):
                url = url[2:]
            if not url.startswith('http'): url = 'https://' + url
            pressescbuttonafterloadpage(driver, url)  # driver.get(url=url)
            if tmdt in ('la', 'ta', ):
                sanpham_s: list = findelem(driver, xpath=classinprod_motadai, scroll=True, getall=True)
                motatuple: tuple = tuple(
                    s.text for s in sanpham_s
                ) if tmdt == 'la' else tuple(
                    get_in4from_elem(elem=s, fie='title') for s in sanpham_s
                )
                jsodict['Mo_Ta'] = '\n'.join(motatuple)
                if tmdt in ('la', ):
                    danhgia = findelem(driver, xpath=classinprod_danhgia)
                    jsodict['Danh_Gia'] = danhgia.text
                # giaban = findelem(driver, xpath=classgiaban)
                # jsodict['Gia_Bl'] = giaban.text  # giá bán lẻ trang tổng và trang chi tiết không khớp nhau -> bug_in_laz
                if tmdt in ('ta', ):
                    if jsodict['Link_Anh'] == '-1':
                        hinhanh = findelem(driver, xpath=classinprod_danhgia, scroll=False, getall=False)
                        jsodict['Link_Anh'] = get_in4from_elem(elem=hinhanh, fie="src")
                    if jsodict['Ma_Hang'] == '-1':
                        Ma_hang_ = findelem(driver, xpath=ma__hang, scroll=False, getall=False)
                        # assert Ma_hang_ is not None
                        jsodict['Ma_Hang'] = get_in4from_elem(elem=Ma_hang_, fie="data-item")
                    danhgia_ = findelem(driver, xpath=classinprod_ten, scroll=False, getall=False)
                    soluotdanhgia_ = danhgia_.text
                    soluotdanhgia = parse_giaban(soluotdanhgia_)
                    if not jsodict['Sl_Ban'] == soluotdanhgia:
                        jsodict['Sl_Ban'] = soluotdanhgia
            else:
                jsodict['Mo_Ta'] = adapt2iters(driver, classinprod_motadai)
            post2api(jsodict)
        elif tmdt in ('sh', '1688', ):  # elif tmdt == 'sh':
            if cra_html:
                brow__ser(url=url, scroll=True, dongtab=dongmotloattabsaumotsolanmomoi)
                dongmotloattabsaumotsolanmomoi += 1


def buttonaftersomeseconds(sec: int = 10, butt: str = 'esc'):
    time.sleep(sec)
    pyautogui.press(butt)


def pressescbuttonafterloadpage(driver, url):
    t1 = threading.Thread(target=buttonaftersomeseconds)
    t1.start()
    driver.get(url)
    t1.join()


def gethtmlslist_bycategories(
        driver, fol, danhmuc_s, ad, tmdt, classsanpham,
        classthongtin=None, classdanhgiadaban=None, classdaban_=None, classdaban=None, datasqe_danhgia=None, classten=None, classnoiban=None, classgiaban=None,
):
    # https://shopee.vn/Đồ-Chơi-cat.11036932
    # https://www.lazada.vn/tag/do-choi-tre-em/?page=0
    if fol is not None:
        if not os.path.isdir(fol):
            os.mkdir(fol)
    looplv1: str = os.path.join(fol, "looplv1.json") if fol is not None else "looplv1.json"
    looplv2: str = os.path.join(fol, "looplv2.json") if fol is not None else "looplv2.json"

    sotrang: int = 9 if allproduct else 2

    if tmdt == 'ta':
        if any([
            len(danhmuc_s) == 0,
            all([
                '_' in danhmuc_s,
                len(danhmuc_s) == 1,
            ]),
        ]):
            driver.get(ad)
            a_cate = findelem(driver, '//div[@data-spm="lead_cate1"]//a', getall=True)
            danhmuc_s: dict = {get_in4from_elem(elem, 'data-spm'): get_in4from_elem(elem, 'href') for elem in a_cate}
    for danhmuc in danhmuc_s:
        if isinstance(danhmuc_s, dict):
            url_: str = danhmuc_s[danhmuc]
        else:
            url_: str = ad + danhmuc

        if tmdt in ('1688', ):
            if not cra_html:
                continue
            driver.get(url_)
            a_cate = findelem(
                driver,
                xpath=classsanpham,
                # scroll=True,
                getall=True,
            )
            link_s: tuple = tuple(get_in4from_elem(elem, 'href') for elem in a_cate)
            for i, link in enumerate(link_s):

                ion: int or None = allproduct_(i, sotrang)
                if ion is None:
                    continue
                else:
                    if ion < 0:
                        break

                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[-1])
                driver.get(link)
                a_cate_ = findelem(
                    driver,
                    xpath=xpathsanpham_1688,
                    scroll=True,
                    getall=True,
                )
                for elem in a_cate_:
                    elem2bs4_(
                        get_in4from_elem(elem), get_in4from_elem(elem, 'id'), classthongtin, classdanhgiadaban, classdaban_, classdaban, datasqe_danhgia, classten, classnoiban, classgiaban
                    )
                driver.close()
                driver.switch_to.window(driver.window_handles[-1])
            print()
            continue

        dangnhap: bool = False
        for trang in range(sotrang):
            if tmdt in ('alib', ):
                url: str = url_ + sear_ch + str(trang) if trang > 0 else url_
            else:
                url: str = url_ + page + str(trang) if trang > 0 else url_
            if tmdt in ('la', 'alib', 'ta', ):
                assert driver is not None
                driver.get(url)
                if not dangnhap:
                    if tmdt == 'ta':
                        print('Yêu cầu mở app quét qr đăng nhập bằng điện thoại rồi nhấn Enter!')
                        dangnhap: bool = True
                        input()
                pressescbuttonafterloadpage(driver, url)
                sanpham_s: list = findelem(driver, xpath=classsanpham, scroll=True, getall=True)
                for sanpham in sanpham_s:
                    fie: str = getid(tmdt)
                    dataitemid = get_in4from_elem(
                            elem=sanpham,
                            fie=fie,
                        )
                    contents = get_in4from_elem(
                        elem=sanpham,
                    )
                    if contents is None:
                        contents = get_in4from_elem(
                            elem=sanpham,
                            fie='innerhtml',
                        )
                    if tmdt in ('alib', ):
                        elem2bs4_alib(
                            contents, dataitemid, classthongtin, classdanhgiadaban, classdaban_, classdaban, datasqe_danhgia, classten, classnoiban,
                        )
                    elif tmdt in ('ta', ):
                        elem2bs4_tao(
                            contents, dataitemid, classthongtin, classdanhgiadaban, classdaban_, classdaban, datasqe_danhgia, classten, classnoiban,
                        )
                    else:
                        elem2bs4(
                            contents, dataitemid, classthongtin, classdanhgiadaban, classdaban_, classdaban, datasqe_danhgia, classten, classnoiban,
                        )
            elif tmdt == 'sh':
                assert classthongtin is None
                brow__ser(url=url, scroll=True)
    if tmdt == 'la':
        if debug:
            lis__jso = lis_jso_laz.copy()
        # readfile(file=looplv1, mod="w", cont=lis_jso_laz, jso=True)
    return looplv2, looplv1


def gethtmlslist_bysearch(ad, keyword: str = "%C4%91%E1%BB%93%20ch%C6%A1i"):
    # https://shopee.vn/search?keyword=%C4%91%E1%BB%93%20ch%C6%A1i&page=2
    # https://shopee.vn/search?facet=11036954&keyword=%C4%91%E1%BB%93%20ch%C6%A1i&noCorrection=true&page=0
    url_: str = ad + sear__ch + keyword
    for trang in range(9):
        url: str = url_ + sear_ch + str(trang)
        brow__ser(url=url)
        for _ in range(5):
            pyautogui.scroll(-100)  # Scroll down 100 pixels
            time.sleep(3)


def product_in_detail_(looplv2, looplv1, tmdt, classinprod_ten, classinprod_danhgia, classinprod_motadai, driver):
    lis__jso = None
    if tmdt == 'la':
        lis__jso = lis_jso_laz.copy()
    elif tmdt == 'sh':
        lis__jso = lis_jso.copy()
    elif tmdt == '1688':
        lis__jso = lis_jso_1688.copy()
    elif tmdt == 'alib':
        lis__jso = lis_jso_alib.copy()
    elif tmdt == 'ta':
        lis__jso = lis_jso_tao.copy()
    gethtmlslist_byjson(looplv1, tmdt, classinprod_motadai, classinprod_danhgia, driver, jso=lis__jso, classinprod_ten=classinprod_ten)
    if tmdt in ('la', 'ta', ):
        return

    if debug:
        for thutu, jso in enumerate(lis_jso):
            if any([
                not jso['Sl_Ban'] > 0,
                jso['Dia_Chi_Ban'] == '_',
            ]):
                jso_erroe.append(jso)

    if debug:
        tenhangtuple: tuple = tuple(jso["Ten_Hang"] for jso in lis__jso)
    posted: int = 0
    for htMl in html2bs4(product=True, tmdt=tmdt):
        tencuasanpham = None
        for classinprod__ten in classinprod_ten:
            ten_ = htMl.find('div', {"class": classinprod__ten})
            if ten_ is not None:
                tencuasanpham = ten_.find('span') if tmdt == 'sh' else ten_
                break
        if tencuasanpham is None:
            if debug:
                print()
            continue

        motadai = None
        listmt: list = list()
        if tmdt == '1688':
            motadai: str = adapt2iters(htMl, classinprod_motadai)
        else:
            for classinprod__motadai in classinprod_motadai:
                motadai = htMl.find('div', {"class": classinprod__motadai})
                if motadai is not None:
                    break
            if motadai is None:
                if debug:
                    print('không lấy được mô tả!', tencuasanpham.text, )
                # continue

        mahang = None
        noib_an = None
        if tmdt == '1688':
            timmahang = htMl.find('a', {"class": findid_class})
            if timmahang is None:
                if debug:
                    print('không lấy được mã hàng!', tencuasanpham.text, )
            else:
                mahang = parse_mahang(timmahang.get('href'))

            timnoib_an = htMl.find('span', {"class": noiban_class})
            if timnoib_an is None:
                if debug:
                    print('không tìm được nơi bán trong trang chi tiết!', tencuasanpham.text, )
            else:
                noib_an = timnoib_an.text

        upd: bool = False
        if debug:
            listten: list = [jso["Ten_Hang"] for jso in lis__jso]
        for thutu, jso in enumerate(lis__jso):
            if tmdt == '1688':
                if jso["Ma_Hang"] == mahang:
                    upd = True
                    if noib_an is not None and not noib_an.strip() == '':
                        lis__jso[thutu]['Dia_Chi_Ban'] = noib_an
            else:
                if oversimplify_string(jso["Ten_Hang"]) == oversimplify_string(tencuasanpham.text):  # '____' + tencuasanpham.text:
                    upd = True
            if upd:
                lis__jso[thutu]["Mo_Ta"] = motadai.text if not isinstance(motadai, str) else motadai
                posted += 1
                if db:
                    try:
                        post2api(jso)  # TODO có chấp nhận không lấy được mô tả vẫn post lên hay không
                    except requests.exceptions.ConnectionError:
                        pass
                break
        if not upd:
            if debug:
                print()
    else:
        if debug:
            print()
    # readfile(file=looplv2, mod="w", cont=jso, jso=True)


def product_in_detail(looplv2, looplv1, tmdt, classinprod_ten, classinprod_danhgia, classinprod_motadai, driver):
    lis__jso = None
    if tmdt == 'la':
        lis__jso = lis_jso_laz.copy()
    elif tmdt == 'sh':
        lis__jso = lis_jso.copy()
    gethtmlslist_byjson(looplv1, tmdt, classinprod_motadai, classinprod_danhgia, driver, jso=lis__jso)
    for htMl in html2bs4(product=True):
        tencuasanpham = None
        for classinprod__ten in classinprod_ten:
            ten_ = htMl.find('div', {"class": classinprod__ten})
            if ten_ is not None:
                tencuasanpham = ten_.find('span')
                break
        if tencuasanpham is None:
            continue
        # assert tencuasanpham is not None

        danhgia = None
        for classinprod__danhgia in classinprod_danhgia:
            danhgia = htMl.find('div', {"class": classinprod__danhgia})
            if danhgia is not None:
                break
        if danhgia is None:
            if debug:
                print('không lấy được đánh giá!', tencuasanpham.text, )
            continue
        # assert danhgia is not None

        tencuasanpham = None
        for classinprod__ten in classinprod_ten:
            ten_ = htMl.find('div', {"class": classinprod__ten})
            if ten_ is not None:
                tencuasanpham = ten_.find('span')
                break
        if tencuasanpham is None:
            continue
        # assert tencuasanpham is not None

        danhgia = None
        for classinprod__danhgia in classinprod_danhgia:
            danhgia = htMl.find('div', {"class": classinprod__danhgia})
            if danhgia is not None:
                break
        if danhgia is None:
            if debug:
                print('không lấy được đánh giá!', tencuasanpham.text, )
            continue
        # assert danhgia is not None

        if debug:
            print('tên:', tencuasanpham.text)
            print(danhgia.text)

        motadai = None
        for classinprod__motadai in classinprod_motadai:
            motadai = htMl.find('div', {"class": classinprod__motadai})
            if motadai is not None:
                break
        if motadai is None:
            if debug:
                print('không lấy được mô tả!', tencuasanpham.text, )
            continue
        # assert motadai is not None

        upd: bool = False
        for thutu, jso in enumerate(lis__jso):
            if oversimplify_string(jso["Ten_Hang"]) == oversimplify_string(tencuasanpham.text):
                upd = True
                lis__jso[thutu]["Mo_Ta"] = motadai.text
                lis__jso[thutu]["Danh_Gia"] = danhgia.text
                break
        if not upd:
            if debug:
                print()
    post2api(lis__jso)
    # readfile(file=looplv2, mod="w", cont=jso, jso=True)


def crawlfromhtml_(
        looplv1, classsanpham, classthongtin, classten, classdanhgiadaban, datasqe_danhgia, classdaban,
        classnoiban=None, classgiaban=None
):
    for htMl in html2bs4():
        scri_s = htMl.find_all('script', {"type": "application/ld+json"})  # //script[@type="application/ld+json"]
        for scri in scri_s:
            for cont in scri.contents:
                if debug:
                    print(cont)
                jso: dict = json.loads(cont)
                if not jso['@type'] == 'Product':
                    continue
                if debug:
                    if jso['name'] == '[HCM] Bộ tranh đính đá hoạt hình tự làm, Comco KÈM KHUNG VÀ DỤNG CỤ - Bộ tranh gắn đá DIY nhiều mẫu':
                        print()
                Gia_Bl = float(jso['offers']['lowPrice'] if 'lowPrice' in jso['offers'] else jso['offers']['price'])
                scri_jso: dict = form_json(
                    Ma_Hang=jso['productID'],  # '____' + jso['productID'],  #
                    Ten_Hang=jso['name'],  # '____' + jso['name'],  #
                    Mo_Ta="<string>",
                    Sl_Ban=0,  # soluongdaban,  # "<double>",
                    Danh_Gia=float(jso['aggregateRating']['ratingValue']),
                    Gia_Bl=Gia_Bl,
                    Link_Anh=jso['image'],
                    Link_Sp=jso['url'],
                    Dia_Chi_Ban='_',  # noiban.text,
                    ID_Nhom=None,  # TODO
                    ID_Loai=None  # TODO
                )
                lis_jso.append(scri_jso)
        sanpham_s = htMl.find_all('li', {"class": lambda x: x and classsanpham in x})
        for sanpham in sanpham_s:
            link = sanpham.find('a', {"href": True})
            if link is None:  # trường hợp javascrip chưa kịp sinh code html phía dưới
                continue
            if debug:
                print(link.get("href"))
            thongtin_s = link.find_all('div', {"class": classthongtin})
            if debug:
                print("len(thongtin_s):", len(thongtin_s))
            # assert len(thongtin_s) == 1
            thongtin = thongtin_s[0]
            ten = thongtin.find('div', {"class": classten})
            tencuasanpham: str = ten.text
            if debug:
                print('ten:', ten.text)
            noiban = thongtin.find('div', {"class": classnoiban})
            if debug:
                print('noi ban:', noiban.text)
            danhgia_daban = thongtin.find('div', {"class": classdanhgiadaban})
            daban = danhgia_daban.find('div', {"class": lambda x: x and classdaban in x})
            if debug:
                print("đã bán:", daban.text)
            soluongdaban: int = parse_soluong(daban.text)
            for thutu, jso in enumerate(lis_jso):
                if oversimplify_string(jso["Ten_Hang"]) == oversimplify_string(tencuasanpham):  # '____' + tencuasanpham:
                    lis_jso[thutu]["Sl_Ban"] = soluongdaban
                    lis_jso[thutu]["Dia_Chi_Ban"] = noiban.text
                    break
    if debug:
        lis__jso = lis_jso.copy()
        print()



def crawlfromhtml(
        looplv1, classsanpham, classthongtin, classten, classdanhgiadaban, datasqe_danhgia, classdaban,
        classnoiban=None, classgiaban=None
):
    for htMl in html2bs4():
        sanpham_s = htMl.find_all('li', {"class": lambda x: x and classsanpham in x})
        for sanpham in sanpham_s:
            link = sanpham.find('a', {"href": True})
            if link is None:  # trường hợp javascrip chưa kịp sinh code html phía dưới
                continue
            if debug:
                print(link.get("href"))
            duongdancuasanpham: str = link.get("href")
            masanpham: str = duongdancuasanpham.split(masanphamshopee)[-1]
            img_s = link.find_all('img', {'src': True})
            if debug:
                print("len(img_s):", len(img_s))

            danhsachhinhanh: list = list()
            for img in img_s:
                danhsachhinhanh.append(img.get('src'))
            thongtin_s = link.find_all('div', {"class": classthongtin})
            if debug:
                print("len(thongtin_s):", len(thongtin_s))
            # assert len(thongtin_s) == 1
            thongtin = thongtin_s[0]
            ten = thongtin.find('div', {"class": classten})
            if debug:
                print('ten:', ten.text)
            noiban = thongtin.find('div', {"class": classnoiban})
            if debug:
                print('noi ban:', noiban.text)
            giaban = thongtin.find('span', {"class": classgiaban})
            if debug:
                print('noi ban:', giaban.text)
            tencuasanpham: str = ten.text
            danhgia_daban = thongtin.find('div', {"class": classdanhgiadaban})
            danhgia = danhgia_daban.find('div', {"data-sqe": datasqe_danhgia})
            daban = danhgia_daban.find('div', {"class": lambda x: x and classdaban in x})
            if debug:
                print("đã bán:", daban.text)
            soluongdaban: int = parse_soluong(daban.text)

            lis_jso.append({
                "Ma_Hang": masanpham,
                "Ten_Hang": tencuasanpham,
                "Mo_Ta": "<string>",
                "Gia_Bl": int(giaban.text.replace('.', '')),
                "Sl_Ban": soluongdaban,  # "<double>",
                "Danh_Gia": -1,
                "Link_Anh": danhsachhinhanh[-1],
                "Link_Sp": duongdancuasanpham,
                "Dia_Chi_Ban": noiban.text,
                "ID_Nhom": None,  # TODO
                "ID_Loai": None  # TODO
            })
    # readfile(file=looplv1, mod="w", cont=jso, jso=True)


def findelem(driver, xpath, scroll: bool = False, getall: bool = False):
    element = []
    lan = 0
    if scroll:
        # https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
        # driver.execute_script("window.scrollTo(0, 30)")
        # html = driver.find_element(By.TAG_NAME, 'html')
        # html.send_keys(Keys.END)
        for _ in range(5):
            driver.execute_script("window.scrollTo(0, window.scrollY + 1500)")
            time.sleep(3)
    while len(element) == 0:
        element = driver.find_elements(By.XPATH, xpath)
        lan += 1
        if lan > 3:
            raise NoSuchElementException
        time.sleep(1)
    if not getall: return element[0]
    return element


def get_in4from_elem(
        elem,
        fie: str = 'outerHTML',
        # fie: str = 'innerhtml'
):
    return elem.get_attribute(fie)


def clickkk(driver, xpath):
    element = findelem(driver, xpath)
    try:
        element.click()  # TODO: check elem clicked or not
    except ElementClickInterceptedException:  # https://stackoverflow.com/questions/57741875/selenium-common-exceptions-elementclickinterceptedexception-message-element-cl:
        pass
        # print_on_gui("ElementClickInterceptedException", text_widget=text_widget)
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

    options = webdriver.ChromeOptions()
    if PROXY is not None:
        # https://stackoverflow.com/questions/11450158/how-do-i-set-proxy-for-chrome-in-python-webdriver
        options.add_argument('--proxy-server=%s' % PROXY)
##    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--start-maximized")

    ua = UserAgent()
    user_agent = ua.random;print(user_agent)
##    https://stackoverflow.com/questions/68566449/how-to-fix-this-browser-or-app-may-not-be-secure-error-when-using-selenium-java
##    https://stackoverflow.com/questions/49565042/way-to-change-google-chrome-user-agent-in-selenium
    options.add_argument(f'--user-agent={user_agent}')

##    options.add_argument("--window-size=1000,1080")
##    options.add_argument("--window-position=1000,0")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    # options.add_argument('--headless')
##    disable the banner "Chrome is being controlled by automated test software"
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    # Pass the argument 1 to allow and 2 to block
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2
        })
    if incog:
        options.add_argument("--incognito")
    return webdriver.Chrome(
##        ChromeDriverManager(version='114.0.5735.16').install(),
        service=ChromeService(ChromeDriverManager().install()),
##        chrome_options=options,
        options=options,
        )


def brow__ser(
    url="https://shopee.vn/search?facet=11036946&keyword=do%20choi&noCorrection=true&page=0",
    browser_path=browser_path,
    scroll: bool = False,
    dongtab: int or None = None,
):
    webbrowser.register('custom_browser', None, webbrowser.BackgroundBrowser(browser_path))
    webbrowser.get('custom_browser').open(url)
    if not scroll:
        return
    for _ in range(5):
        time.sleep(3)
        pyautogui.scroll(scro)  # Scroll down 10 pixels
    if dongtab is not None:
        if dongtab % motsolanmomoi == 0:
            for _ in range(motsolanmomoi - 1):
                pyautogui.hotkey('ctrl', 'shift', 'tab')
                time.sleep(1)
            for _ in range(motsolanmomoi):
                pyautogui.hotkey('ctrl', 'w')
                time.sleep(1)


def phant():
##    https://stackoverflow.com/questions/71360239/how-to-use-python-selenium-to-automate-login-to-google/71360264#71360264
    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0'
    PHANTOMJS_ARG = {'phantomjs.page.settings.userAgent': UA}
    return webdriver.PhantomJS(desired_capabilities=PHANTOMJS_ARG)


def firefox(incog: bool = False):
##    https://stackoverflow.com/questions/66209119/automation-google-login-with-python-and-selenium-shows-this-browser-or-app-may
    import geckodriver_autoinstaller
    geckodriver_autoinstaller.install()
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.service import Service


    # service = Service(executable_path=r'C:\Users\HLC\Downloads\geckodriver-v0.33.0-win64\geckodriver.exe')
    service = Service()

    # options = webdriver.FirefoxOptions()
    options = Options()
    if incog:
        options.set_preference("browser.privatebrowsing.autostart", True)
    options.add_argument("--headless")
    options.binary_location = '/usr/bin/firefox'
    options.add_argument("download.default_directory=C:\\Music")
    profile = webdriver.FirefoxProfile(
        '/home/nguyenlamvu/snap/firefox/common/.mozilla/firefox/f1yu319w.default-release'
        )
    profile.set_preference("dom.webdriver.enabled", False)
    profile.set_preference('useAutomationExtension', False)
    # profile.set_preference('browser.download.folderList', 2)
    # profile.set_preference('browser.download.manager.showWhenStarting', False)
    # profile.set_preference('browser.download.dir', os.getcwd())
    # profile.set_preference('browser.helperApps.neverAsk.saveToDisk', ('application/vnd.ms-excel'))
    # profile.set_preference('general.warnOnAboutConfig', False)
    profile.update_preferences()
    desired = DesiredCapabilities.FIREFOX
##    https://stackoverflow.com/questions/76802588/python-selenium-unexpected-keyword-argument-executable-path
    return webdriver.Firefox(
        service=service,
        options=options,
        )


# def getin4():
#     listin4: list = readfile(file=get_in4)
#     liklist: list = readfile(file=likl_ist)
#     for enu, em__pa in enumerate(listin4):
#         em_pa: list = em__pa.split('|')
#         em_pa.append(liklist[enu])  # TODO need an other way
#         yield em_pa


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

# def helloCallBack():  # mở cửa sổ popup
#     messagebox.showinfo( "Hello Python", "Hello World")
#     print_on_gui("Hello Python!", text_widget=text_widget)
#     print_on_gui("Hello", "world!", text_widget=text_widget)


lis_jso: list = list()
lis_jso_laz: list = list()
lis_jso_1688: list = list()
lis_jso_alib: list = list()
lis_jso_tao: list = list()
jso_erroe: list = list()
initjson()
### Create a new tkinter window
##root = tk.Tk()
### Create a new `Text` widget
##text_widget = tk.Text(root, state="disabled")
### Show the widget on the screen
##text_widget.pack(fill="both", expand=True)
##B = tk.Button(root, text="Hello", command=helloCallBack)
##B.pack(fill="both", expand=True)

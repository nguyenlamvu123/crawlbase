import datetime
import os
from sys import platform

tmdt_s: list = [
    # 'sh',
    # 'la',
    # '1688',
    # 'alib',
    'ta',
]
danhmucnhom: list = [
    'Đồ chơi',
]
danhmucloai: list = [
    'shopee',
    'lazada',
    '1688',
    'taobao',
    'alibaba',
]
headers = {
    'Content-Type': 'application/json'
}

#############################################################################
debug: bool = True  # active or inactive print()

allproduct: bool = False  # crawl all product or just illustrate
def allproduct_(i, sotrang: int or None = None) -> int or None:
    if not allproduct:
        if i > 13:
            return -1  # break
        if i < 7:
            return None  # continue
        elif sotrang is not None:  # sotrang: int = 9 if allproduct else 2
            if not i < 7 + sotrang:
                return -1  # break
    return 1

cra_html: bool = True  # crawl html files or not
db: bool = True  # request to db or not
#############################################################################

soluongdaban_1688: str = '天成交'
motvan_1688: str = '万件'
mot_1688: str = '件'
findid_class: str = "title-report-operate"  # //a[@class="title-report-operate"]
noiban_class: str = 'logistics-city'  # //span[@class="logistics-city"]
xpathsanpham_1688: str = '//div[@class="cate1688-offer b2b-ocms-fusion-comp"]'

page: str = '?page='
sear_ch: str = '&page='
sear__ch: str = '/search?keyword='
masanphamshopee: str = '&xptdk='
prename: str = 'Mua sắm online sản phẩm'
amongname: str = 'Shopee Việt Nam'

idfromlink: str = 'id='
ma__hang: str = '//span[@id="aliww-click-trigger"]'  # {'id': "aliww-click-trigger"}  #
hinh_anh_alib: dict = {"class": lambda x: x and 'MainPic' in x and 'mainPic' in x}  # //img[@class="MainPic--mainPic--rcLNaCv"]

postapi = "https://api01.nhasachtientho.vn/api/DmHang/Add"


def form_json(
        Ma_Hang,
        Ten_Hang,
        Mo_Ta,
        Sl_Ban,
        Danh_Gia,
        Gia_Bl,
        Link_Anh,
        Link_Sp,
        Dia_Chi_Ban,
        ID_Nhom=None,
        ID_Loai=None,
) -> dict:
    for s in (Danh_Gia, Gia_Bl, Sl_Ban):
        if s is not None:
            assert isinstance(s, int) or isinstance(s, float)
    for s in (Ma_Hang, Ten_Hang, Mo_Ta, Link_Anh, Link_Sp, Dia_Chi_Ban):
        if s is not None:
            assert isinstance(s, str)
    return {
        "Ma_Hang": Ma_Hang,
        "Ten_Hang": Ten_Hang,
        "Mo_Ta": Mo_Ta,
        "Sl_Ban": Sl_Ban,
        "Danh_Gia": Danh_Gia,
        "Gia_Bl": Gia_Bl,
        "Link_Anh": Link_Anh,
        "Link_Sp": Link_Sp,
        "Dia_Chi_Ban": Dia_Chi_Ban,
        "ID_Nhom": ID_Nhom,
        "ID_Loai": ID_Loai,
    }


def add_r(tmdt):
    (
        fol, ad, danhmuc_s, classsanpham, classthongtin, classten, classdanhgiadaban, datasqe_danhgia,
        classdaban_, classdaban, classnoiban, classgiaban, classinprod_ten, classinprod_danhgia, classinprod_motadai
    ) = (
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
    )
    if tmdt == 'ta':
        fol: str = 'tao'
        ad: str = "https://world.taobao.com/"
        danhmuc_s: dict = {
            # 'd0_Home_Living': 'https://s.taobao.com/search?q=%E5%AE%B6%E5%85%B7%E5%AE%B6%E5%B1%85&type=p&tmhkh5=&spm=a21wu.241046-sg.a2227oh.d100&from=sea_1_searchbutton&catId=100',
            # 'd1_Women_Apparel': 'https://s.taobao.com/search?q=%E5%A5%B3%E8%A3%85%2F%E5%A5%B3%E5%A3%AB%E7%B2%BE%E5%93%81&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20210330&ie=utf8',
            # 'd2_Men_Wear': 'https://s.taobao.com/search?q=%E7%94%B7%E8%A3%85%2F%E7%94%B7%E5%A3%AB%E7%B2%BE%E5%93%81&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20210402&ie=utf8',
            # 'd3_Bags_Accessories': 'https://s.taobao.com/search?q=%E7%AE%B1%E5%8C%85&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20210402&ie=utf8',
            # 'd4_Sports_Outdoors': 'https://s.taobao.com/search?q=%E8%BF%90%E5%8A%A8%E6%88%B7%E5%A4%96&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20210330&ie=utf8',
            # 'd5_Mobile_Gadgets': 'https://s.taobao.com/search?q=3C%E6%95%B0%E7%A0%81%2F%E6%89%8B%E6%9C%BA%2F%E6%99%BA%E8%83%BD&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20210330&ie=utf8',
            # 'd6_Computers_Peripherals': 'https://s.taobao.com/search?ie=utf8&initiative_id=staobaoz_20210402&stats_click=search_radio_all%3A1&js=1&imgfile=&q=%E7%AC%94%E8%AE%B0%E6%9C%AC%E7%94%B5%E8%84%91&suggest=history_1&_input_charset=utf-8&wq=%E7%AC%94%E8%AE%B0%E6%9C%AC&suggest_query=%E7%AC%94%E8%AE%B0%E6%9C%AC&source=suggest',
            # 'd7_Model_Anime_Peripherals': 'https://s.taobao.com/search?q=%E6%A8%A1%E7%8E%A9%2F%E5%8A%A8%E6%BC%AB%2F%E5%91%A8%E8%BE%B9&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20210330&ie=utf8',
            'd8_Toys_Babies': 'https://s.taobao.com/search?q=%E7%8E%A9%E5%85%B7%2F%E6%AF%8D%E5%A9%B4%E7%94%A8%E5%93%81&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20210330&ie=utf8',
            # 'd9_Automotive_Services': 'https://s.taobao.com/search?q=%E6%B1%BD%E8%BD%A6%2F%E8%99%9A%E6%8B%9F&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20210330&ie=utf8',
            # 'd10_Home_Appliances': 'https://s.taobao.com/search?q=%E5%A4%A7%E5%B0%8F%E5%AE%B6%E7%94%B5&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20210330&ie=utf8',
            # 'd11_Beauty_Personal Care': 'https://s.taobao.com/search?q=%E7%BE%8E%E5%A6%86%E6%B4%97%E6%8A%A4&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20210330&ie=utf8',
            # 'd12_Food_Beverages': 'https://s.taobao.com/search?q=%E9%9B%B6%E9%A3%9F%E9%A5%AE%E6%96%99&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20210330&ie=utf8',
            # 'd13_Health_Wellness': 'https://s.taobao.com/search?q=%E5%8C%BB%E8%8D%AF%E5%81%A5%E5%BA%B7&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20210330&ie=utf8'
        }

        classsanpham: str = '//div[@class="Content--contentInner--QVTcU0M"]//a[contains(@class, "--doubleCardWrapper--")]'
        classthongtin: dict = {"class": lambda x: x and 'ShopInfo' in x and 'shopInfo' in x}  # //div[contains(@class, 'ShopInfo') and contains(@class, 'shopInfo')]
        classten: dict = {"class": lambda x: x and 'Title' in x and 'title' in x}  # //div[@class="Title--title--jCOPvpf"]
        classdanhgiadaban: dict = {"class": lambda x: x and 'Price' in x and 'price' in x}  # //span[contains(@class, "Price") and contains(@class, "price")]
        datasqe_danhgia: dict = {"data-name": lambda x: x and "itemExp" in x}  # //div[@data-name="itemExp"]//img[@src]
        classdaban_: dict = {"class": lambda x: x and 'Price' in x and 'priceWrapper' in x}  # //div[@class="Price--priceWrapper--Q0Dn7pN "]
        classdaban: dict = {"class": lambda x: x and 'Price' in x and 'realSales' in x}  # //span[contains(@class, "Price") and contains(@class, "realSales")]
        classnoiban: dict = {"class": lambda x: x and 'ShopInfo' in x and 'shopName' in x}  # //a[contains(@class, 'ShopInfo') and contains(@class, 'shopName')]
        classgiaban: str = '_'

        classinprod_ten: str = '//span[contains(@class, "ItemHeader") and contains(@class, "salesDesc")]'  # số lượng đã bán trong trang chi tiết
        classinprod_danhgia: str = '//li[contains(@class, "PicGallery") and contains(@class, "thumbnail")]//img'  # hình ảnh
        classinprod_motadai: str = '//span[@class="Attrs--attr--33ShB6X"]'
    elif tmdt == 'alib':
        fol: str = 'ali'
        ad: str = 'https://www.alibaba.com/'
        danhmuc_s: tuple = (
            'trade/search?spm=a2700.product_home_l0.home_login_first_screen_fy23_pc_search_bar.keydown__Enter&tab=all&SearchText=children+toys',  # SearchText = "children toys"
        )

        classsanpham: str = '//div[contains(@class, "organic-list")]//div[contains(@class, "fy23-search-card") and contains(@class, "fy23-gallery-card")]'
        classthongtin: dict = {"class": lambda x: x and 'card-info' in x and 'gallery-card-layout-info' in x}
        classten: dict = {"data-spm": "d_title"}
        classdanhgiadaban: dict = {"class": 'search-card-e-price-main'}
        datasqe_danhgia: dict = {"data-spm": 'd_image'}
        classdaban_: str = '_'
        classdaban: str = '_'
        classnoiban: dict = {"data-spm": "d_companyName"}
        classgiaban: str = '_'

        classinprod_ten: list = ['_', ]
        classinprod_danhgia: str = "_"
        classinprod_motadai: list = [
            '//div[@class="attribute-item"]//div[@class="left"]',
            '//div[@class="attribute-item"]//div[@class="right"]'
        ]
    elif tmdt == '1688':
        classinprod_motadai: list = ["offer-attr-item-name", "offer-attr-item-value", ]  # //div[@class="offer-attr-wrapper"]
        fol: str = '1688'
        # ad: str = 'https://www.1688.com/'
        ad: str = 'https://muying.1688.com/'
        danhmuc_s: tuple = (
            'wanju?spm=a262n.6633621.1997328637.14.3d584830GgsoY1',  # đồ chơi
        )

        classsanpham: str = '//li[@class="item"]//a[@href]'
        classthongtin: str = "offer-desc"
        classten: str = 'offer-title'
        classdanhgiadaban: str = "offer"  # đường dẫn
        datasqe_danhgia: str = "offer-img"  # hình ảnh
        classdaban_: str = "clearfix"
        classdaban: str = "offer-vol"
        classnoiban: str = "offer-location"
        classgiaban: str = 'offer-price'
        # classgiaban: str = '//div[@class="pdp-product-price"]//span[contains(@class, "price_color_orange")]'

        classinprod_ten: list = ["title-text", ]  # //div[@class="title-text"]
        classinprod_danhgia: str = "_"
        classinprod_motadai: list = ["offer-attr-item-name", "offer-attr-item-value", ]  # //div[@class="offer-attr-wrapper"]
    elif tmdt == 'la':
        fol: str = 'laz'
        ad: str = "https://www.lazada.vn"
        danhmuc_s: tuple = (
            '/tag/do-choi-tre-em/',
        )

        classsanpham: str = '//div[@class="Bm3ON"]'
        classthongtin: str = "RfADt"
        classten: str = 'title'
        classdanhgiadaban: str = "aBrP0"
        datasqe_danhgia: str = "picture-wrapper"  # hình ảnh
        classdaban_: str = "_6uN7R"
        classdaban: str = "_1cEkb"
        classnoiban: str = "oa6ri"
        classgiaban: str = '//div[@class="pdp-product-price"]//span[contains(@class, "price_color_orange")]'

        classinprod_ten: str = "_"
        classinprod_danhgia: str = '//span[@class="score-average"]'
        classinprod_motadai: str = '//div[@class="pdp-product-detail"]'
    elif tmdt == 'sh':
        fol: str = 'sho'
        ad: str = "https://shopee.vn"
        danhmuc_s: tuple = (
            # "/Thời-Trang-Nam-cat.11035567",
            # "/Thời-Trang-Nữ-cat.11035639",
            # "/Điện-Thoại-Phụ-Kiện-cat.11036030",
            # "/Mẹ-Bé-cat.11036194",
            # "/Thiết-Bị-Điện-Tử-cat.11036132",
            # "/Nhà-Cửa-Đời-Sống-cat.11036670",
            # "/Máy-Tính-Laptop-cat.11035954",
            # "/Sắc-Đẹp-cat.11036279",
            # "/Máy-Ảnh-Máy-Quay-Phim-cat.11036101",
            # "/Sức-Khỏe-cat.11036345",
            # "/Đồng-Hồ-cat.11035788",
            # "/Giày-Dép-Nữ-cat.11035825",
            # "/Giày-Dép-Nam-cat.11035801",
            # "/Túi-Ví-Nữ-cat.11035761",
            # "/Thiết-Bị-Điện-Gia-Dụng-cat.11036971",
            # "/Phụ-Kiện-Trang-Sức-Nữ-cat.11035853",
            # "/Thể-Thao-Du-Lịch-cat.11035478",
            # "/Bách-Hóa-Online-cat.11036525",
            # "/Ô-Tô-Xe-Máy-Xe-Đạp-cat.11036793",
            # "/Nhà-Sách-Online-cat.11036863",
            # "/Balo-Túi-Ví-Nam-cat.11035741",
            # "/Thời-Trang-Trẻ-Em-cat.11036382",
            "/Đồ-Chơi-cat.11036932",
            # "/Giặt-Giũ-Chăm-Sóc-Nhà-Cửa-cat.11036624",
            # "/Chăm-Sóc-Thú-Cưng-cat.11036478",
            # "/Voucher-Dịch-Vụ-cat.11035898",
            # "/Dụng-cụ-và-thiết-bị-tiện-ích-cat.11116484",
        )

        classsanpham: str = "shopee-search"
        classthongtin: str = "JxvxgB"
        classten: str = "efwNRW"
        classdanhgiadaban: str = "DN6Jp1"
        datasqe_danhgia: str = "rating"
        classdaban: str = "OwmBnn"
        classnoiban: str = "JVW3E2"
        classgiaban: str = "k9JZlv"

        classinprod_ten: tuple = (
            "_44qnta",
            "WBVL_7",
        )
        classinprod_danhgia: tuple = (
            "_1k47d8 _046PXf",
            "F9RHbS dQEiAI"
        )
        classinprod_motadai: tuple = (
            "MCCLkq",
            'e8lZp3',
        )
    return (
        fol, ad, danhmuc_s, classsanpham,classthongtin, classten, classdanhgiadaban, datasqe_danhgia,
        classdaban_, classdaban, classnoiban, classgiaban, classinprod_ten, classinprod_danhgia, classinprod_motadai
    )


def getid(tmdt):
    if tmdt == 'ta':
        fie: str = 'href'
    else:
        fie: str = 'data-item-id' if tmdt == 'la' else 'data-product_id'
    return fie


scro: int = -10
motsolanmomoi: int = 5  # số lần mở tab mới mà sau số lần này sẽ lùi lại các tab trước đó để đóng tab

if platform == "win32":
    loca_l: str = r'C:\Users\HLC\Downloads'
    browser_path: str = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
else:
    assert platform == "linux" or platform == "linux2"
    loca_l: str = '/home/zaibachkhoa/Downloads/'
    browser_path: str = "/usr/bin/google-chrome"


html_local = None
if 'sh' in tmdt_s:
    t: str = datetime.datetime.now().strftime('%Y%m%d%H%M')
    html_local = os.path.join(
        loca_l,
        'html_shopee' + t,
    )
    if cra_html:
        os.mkdir(html_local)
if '1688' in tmdt_s:
    t: str = datetime.datetime.now().strftime('%Y%m%d%H%M')
    html_local = os.path.join(
        loca_l,
        'html_1688' + t,
    )
    if cra_html:
        os.mkdir(html_local)

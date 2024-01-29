from sys import platform
import datetime, os

tmdt_s: list = [
    # 'sh',
    # 'la',
    '1688',
    # 'ta',
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

cra_html: bool = False  # crawl html files or not
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
        assert isinstance(s, int) or isinstance(s, float)
    for s in (Ma_Hang, Ten_Hang, Mo_Ta, Link_Anh, Link_Sp, Dia_Chi_Ban):
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
        danhmuc_s: tuple = (
            '_',
        )

        classsanpham: str = '_'
        classthongtin: str = '//a[@class="first-category-wrap"]'
        classten: str = "_"
        classdanhgiadaban: str = "_"
        datasqe_danhgia: str = "_"
        classdaban: str = "_"

        classinprod_ten: str = "_"
        classinprod_danhgia: str = "_"
        classinprod_motadai: str = '_'
    elif tmdt == '1688':
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

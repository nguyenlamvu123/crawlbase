from sys import platform


tmdt_s: list = [
    # 'sh',
    'la',
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


debug: bool = True  # active or inactive print()
allproduct: bool = True  # crawl all product or just illustrate
cra_html: bool = False  # crawl html files or not
db: bool = True  # request to db or not

page: str = '?page='
sear_ch: str = '&page='
sear__ch: str = '/search?keyword='
masanphamshopee: str = '&xptdk='
prename: str = 'Mua sắm online sản phẩm'
amongname: str = 'Shopee Việt Nam'
postapi = "https://api01.nhasachtientho.vn/api/DmHang/Add"


def add_r(tmdt):
    (
        fol, ad, danhmuc_s, classsanpham, classthongtin, classten, classdanhgiadaban, datasqe_danhgia,
        classdaban, classnoiban, classgiaban, classinprod_ten, classinprod_danhgia, classinprod_motadai
    ) = (
        None, None, None, None, None, None, None, None, None, None, None, None, None, None
    )
    if tmdt == 'la':
        fol: str = 'laz'
        ad: str = "https://www.lazada.vn"
        danhmuc_s: list = [
            '/tag/do-choi-tre-em/',
        ]

        classsanpham: str = '//div[@class="Bm3ON"]'
        classthongtin: str = "RfADt"
        classten: str = 'title'
        classdanhgiadaban: str = "aBrP0"
        datasqe_danhgia: str = "picture-wrapper"  # hình ảnh
        classdaban: str = "_6uN7R"

        classinprod_ten: str = "_"
        classinprod_danhgia: str = "_"
        classinprod_motadai: str = '//div[@class="pdp-product-detail"]'
    elif tmdt == 'sh':
        fol: str = 'sho'
        ad: str = "https://shopee.vn"
        danhmuc_s: list = [
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
        ]

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
        classdaban, classnoiban, classgiaban, classinprod_ten, classinprod_danhgia, classinprod_motadai
    )

scro: int = -10

if platform == "win32":
    loca_l: str = r'C:\Users\HLC\Downloads'
    browser_path: str = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
else:
    assert platform == "linux" or platform == "linux2"
    loca_l: str = '/home/zaibachkhoa/Downloads/'
    browser_path: str = "/usr/bin/google-chrome"

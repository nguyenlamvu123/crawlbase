from sys import platform


tmdt_s: list = [
    'sh',
    'la',
]


debug: bool = False  # active or inactive print()
allproduct: bool = False  # crawl all product or just illustrate
page: str = '?page='
sear_ch: str = '&page='
sear__ch: str = '/search?keyword='
prename: str = 'Mua sắm online sản phẩm'
amongname: str = 'Shopee Việt Nam'

classthongtin: str = "JxvxgB"
classten: str = "efwNRW"
classdanhgiadaban: str = "DN6Jp1"
datasqe_danhgia: str = "rating"
classdaban: str = "OwmBnn"

classinprod_ten: str = "_44qnta"
classinprod_danhgia: str = "_1k47d8 _046PXf"
classinprod_motadai: str = "MCCLkq"

scro: int = -10

if platform == "win32":
    loca_l: str = r'C:\Users\HLC\Downloads'
    browser_path: str = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
else:
    assert platform == "linux" or platform == "linux2"
    loca_l: str = '/home/zaibachkhoa/Downloads/'
    browser_path: str = "/usr/bin/google-chrome"

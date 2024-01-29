### Cào về 9 trang các sản phẩm thuộc danh mục trong list danhmuc_s (_addr.py_)

Crawl thông tin từ shopee
* cài extension <a>![SingleFile](https://chromewebstore.google.com/detail/singlefile/mpiodijhokgodhhofbcjdecpffjipkle)</a> (Chrome) để tự động lưu html các trang vừa duyệt
![select Auto save all tab](https://imgur.com/EI2Hyf3)
* dùng trình duyệt mặc định (chrome, firefox,...) để duyệt tới từng trang một (trước khi chạy, yêu cầu thu nhỏ màn hình trình duyệt xuống 33% hoặc thấp hơn)
* duyệt qua tất cả html trang tổng vừa cào về, dùng bs4 lấy thông tin lưu vào 1 dict (trong đó có trường link, lưu lại link của sản phẩm)
* vào link của từng sản phẩm, dùng bs4 lấy thông tin chi tiết rồi requests tới api

Crawl thông tin từ lazada
* dùng selenium 

Crawl thông tin từ 1688
* cào các trang tổng bằng selenium (như khi cào lazada) rồi kết hợp trình duyệt mặc định và extension <a>![SingleFile](https://chromewebstore.google.com/detail/singlefile/mpiodijhokgodhhofbcjdecpffjipkle)</a> (Chrome) để cào chi tiết sản phẩm (như khi cào shopee)
* đơn vị tiền tệ (giá bán lẻ) là '￥' ('￥21.88')
* số lượng bán tính trong 30 ngày gần nhất ('30天成交3件')
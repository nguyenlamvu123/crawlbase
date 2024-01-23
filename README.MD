Crawl thông tin từ shopee

### Cào về 9 trang các sản phẩm thuộc danh mục trong list danhmuc_s (_addr.py_)
* cài extension <a>![SingleFile](https://chromewebstore.google.com/detail/singlefile/mpiodijhokgodhhofbcjdecpffjipkle)</a> (Chrome) để tự động lưu html các trang vừa duyệt
![select Auto save all tab](https://imgur.com/EI2Hyf3)
* dùng trình duyệt mặc định (chrome, firefox,...) để duyệt tới từng trang một (trước khi chạy yêu cầu thu nhỏ màn hình trình duyệt xuống 33% hoặc thấp hơn)
* duyệt qua tất cả html trang tổng vừa cào về, dùng bs4 lấy thông tin (trong đó có trường link, lưu lại url của sản phẩm) lưu vào looplv1.json
* duyệt file looplv1.json, vào link của từng sản phẩm, dùng bs4 lấy thông tin chi tiết lưu vào looplv2.json

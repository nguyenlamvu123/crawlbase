from bs4 import BeautifulSoup


contents = """<ul class="image-carousel__item-list" style="width: 135%; transform: translate(0px, 0px);"><li class="image-carousel__item" style="padding: 0px; width: 5%;"><a class="home-category-list__category-grid" href="/Thời-Trang-Nam-cat.11035567"><div class="g3RFjs"><div class="_2QRysE"><div class="_3Jjuff +K-jRT"><div class="+K-jRT OooQQJ" style="background-image: url(&quot;https://down-vn.img.susercontent.com/file/687f3967b7c2fe6a134a2c11894eea4b_tn&quot;); background-size: contain; background-repeat: no-repeat;"></div></div></div><div class="GE2Jnm"><div class="_0qFceF">Thời Trang Nam</div></div></div></a></li><li class="image-carousel__item" style="padding: 0px; width: 5%;"><a class="home-category-list__category-grid" href="/Thời-Trang-Nữ-cat.11035639"><div class="g3RFjs"><div class="_2QRysE"><div class="_3Jjuff +K-jRT"><div class="+K-jRT OooQQJ" style="background-image: url(&quot;https://down-vn.img.susercontent.com/file/75ea42f9eca124e9cb3cde744c060e4d_tn&quot;); background-size: contain; background-repeat: no-repeat;"></div></div></div><div class="GE2Jnm"><div class="_0qFceF">Thời Trang Nữ</div></div></div></a></li><li class="image-carousel__item" style="padding: 0px; width: 5%;"><a class="home-category-list__category-grid" href="/Điện-Thoại-Phụ-Kiện-cat.11036030"><div class="g3RFjs"><div class="_2QRysE"><div class="_3Jjuff +K-jRT"><div class="+K-jRT OooQQJ" style="background-image: url(&quot;https://down-vn.img.susercontent.com/file/31234a27876fb89cd522d7e3db1ba5ca_tn&quot;); background-size: contain; background-repeat: no-repeat;"></div></div></div><div class="GE2Jnm"><div class="_0qFceF">Điện Thoại &amp; Phụ Kiện</div></div></div></a></li><li class="image-carousel__item" style="padding: 0px; width: 5%;"><a class="home-category-list__category-grid" href="/Mẹ-Bé-cat.11036194"><div class="g3RFjs"><div class="_2QRysE"><div class="_3Jjuff +K-jRT"><div class="+K-jRT OooQQJ" style="background-image: url(&quot;https://down-vn.img.susercontent.com/file/099edde1ab31df35bc255912bab54a5e_tn&quot;); background-size: contain; background-repeat: no-repeat;"></div></div></div><div class="GE2Jnm"><div class="_0qFceF">Mẹ &amp; Bé</div></div></div></a></li><li class="image-carousel__item" style="padding: 0px; width: 5%;"><a class="home-category-list__category-grid" href="/Thiết-Bị-Điện-Tử-cat.11036132"><div class="g3RFjs"><div class="_2QRysE"><div class="_3Jjuff +K-jRT"><div class="+K-jRT OooQQJ" style="background-image: url(&quot;https://down-vn.img.susercontent.com/file/978b9e4cb61c611aaaf58664fae133c5_tn&quot;); background-size: contain; background-repeat: no-repeat;"></div></div></div><div class="GE2Jnm"><div class="_0qFceF">Thiết Bị Điện Tử</div></div></div></a></li><li class="image-carousel__item" style="padding: 0px; width: 5%;"><a class="home-category-list__category-grid" href="/Nhà-Cửa-Đời-Sống-cat.11036670"><div class="g3RFjs"><div class="_2QRysE"><div class="_3Jjuff +K-jRT"><div class="+K-jRT OooQQJ" style="background-image: url(&quot;https://down-vn.img.susercontent.com/file/24b194a695ea59d384768b7b471d563f_tn&quot;); background-size: contain; background-repeat: no-repeat;"></div></div></div><div class="GE2Jnm"><div class="_0qFceF">Nhà Cửa &amp; Đời Sống</div></div></div></a></li><li class="image-carousel__item" style="padding: 0px; width: 5%;"><a class="home-category-list__category-grid" href="/Máy-Tính-Laptop-cat.11035954"><div class="g3RFjs"><div class="_2QRysE"><div class="_3Jjuff +K-jRT"><div class="+K-jRT OooQQJ" style="background-image: url(&quot;https://down-vn.img.susercontent.com/file/c3f3edfaa9f6dafc4825b77d8449999d_tn&quot;); background-size: contain; background-repeat: no-repeat;"></div></div></div><div class="GE2Jnm"><div class="_0qFceF">Máy Tính &amp; Laptop</div></div></div></a></li><li class="image-carousel__item" style="padding: 0px; width: 5%;"><a class="home-category-list__category-grid" href="/Sắc-Đẹp-cat.11036279"><div class="g3RFjs"><div class="_2QRysE"><div class="_3Jjuff +K-jRT"><div class="+K-jRT OooQQJ" style="background-image: url(&quot;https://down-vn.img.susercontent.com/file/ef1f336ecc6f97b790d5aae9916dcb72_tn&quot;); background-size: contain; background-repeat: no-repeat;"></div></div></div><div class="GE2Jnm"><div class="_0qFceF">Sắc Đẹp</div></div></div></a></li><li class="image-carousel__item" style="padding: 0px; width: 5%;"><a class="home-category-list__category-grid" href="/Máy-Ảnh-Máy-Quay-Phim-cat.11036101"><div class="g3RFjs"><div class="_2QRysE"><div class="_3Jjuff +K-jRT"><div class="+K-jRT OooQQJ" style="background-image: url(&quot;https://down-vn.img.susercontent.com/file/ec14dd4fc238e676e43be2a911414d4d_tn&quot;); background-size: contain; background-repeat: no-repeat;"></div></div></div><div class="GE2Jnm"><div class="_0qFceF">Máy Ảnh &amp; Máy Quay Phim</div></div></div></a></li><li class="image-carousel__item" style="padding: 0px; width: 5%;"><a class="home-category-list__category-grid" href="/Sức-Khỏe-cat.11036345"><div class="g3RFjs"><div class="_2QRysE"><div class="_3Jjuff +K-jRT"><div class="+K-jRT OooQQJ" style="background-image: url(&quot;https://down-vn.img.susercontent.com/file/49119e891a44fa135f5f6f5fd4cfc747_tn&quot;); background-size: contain; background-repeat: no-repeat;"></div></div></div><div class="GE2Jnm"><div class="_0qFceF">Sức Khỏe</div></div></div></a></li><li class="image-carousel__item" style="padding: 0px; width: 5%;"><a class="home-category-list__category-grid" href="/Đồng-Hồ-cat.11035788"><div class="g3RFjs"><div class="_2QRysE"><div class="_3Jjuff +K-jRT"><div class="+K-jRT OooQQJ" style="background-image: url(&quot;https://down-vn.img.susercontent.com/file/86c294aae72ca1db5f541790f7796260_tn&quot;); background-size: contain; background-repeat: no-repeat;"></div></div></div><div class="GE2Jnm"><div class="_0qFceF">Đồng Hồ</div></div></div></a></li><li class="image-carousel__item" style="padding: 0px; width: 5%;"><a class="home-category-list__category-grid" href="/Giày-Dép-Nữ-cat.11035825"><div class="g3RFjs"><div class="_2QRysE"><div class="_3Jjuff +K-jRT"><div class="+K-jRT OooQQJ" style="background-image: url(&quot;https://down-vn.img.susercontent.com/file/48630b7c76a7b62bc070c9e227097847_tn&quot;); background-size: contain; background-repeat: no-repeat;"></div></div></div><div class="GE2Jnm"><div class="_0qFceF">Giày Dép Nữ</div></div></div></a></li><li class="image-carousel__item" style="padding: 0px; width: 5%;"><a class="home-category-list__category-grid" href="/Giày-Dép-Nam-cat.11035801"><div class="g3RFjs"><div class="_2QRysE"><div class="_3Jjuff +K-jRT"><div class="+K-jRT OooQQJ" style="background-image: url(&quot;https://down-vn.img.susercontent.com/file/74ca517e1fa74dc4d974e5d03c3139de_tn&quot;); background-size: contain; background-repeat: no-repeat;"></div></div></div><div class="GE2Jnm"><div class="_0qFceF">Giày Dép Nam</div></div></div></a></li><li class="image-carousel__item" style="padding: 0px; width: 5%;"><a class="home-category-list__category-grid" href="/Túi-Ví-Nữ-cat.11035761"><div class="g3RFjs"><div class="_2QRysE"><div class="_3Jjuff +K-jRT"><div class="+K-jRT OooQQJ" style="background-image: url(&quot;https://down-vn.img.susercontent.com/file/fa6ada2555e8e51f369718bbc92ccc52_tn&quot;); background-size: contain; background-repeat: no-repeat;"></div></div></div><div class="GE2Jnm"><div class="_0qFceF">Túi Ví Nữ</div></div></div></a></li><li class="image-carousel__item" style="padding: 0px; width: 5%;"><a class="home-category-list__category-grid" href="/Thiết-Bị-Điện-Gia-Dụng-cat.11036971"><div class="g3RFjs"><div class="_2QRysE"><div class="_3Jjuff +K-jRT"><div class="+K-jRT OooQQJ" style="background-image: url(&quot;https://down-vn.img.susercontent.com/file/7abfbfee3c4844652b4a8245e473d857_tn&quot;); background-size: contain; background-repeat: no-repeat;"></div></div></div><div class="GE2Jnm"><div class="_0qFceF">Thiết Bị Điện Gia Dụng</div></div></div></a></li><li class="image-carousel__item" style="padding: 0px; width: 5%;"><a class="home-category-list__category-grid" href="/Phụ-Kiện-Trang-Sức-Nữ-cat.11035853"><div class="g3RFjs"><div class="_2QRysE"><div class="_3Jjuff +K-jRT"><div class="+K-jRT OooQQJ" style="background-image: url(&quot;https://down-vn.img.susercontent.com/file/8e71245b9659ea72c1b4e737be5cf42e_tn&quot;); background-size: contain; background-repeat: no-repeat;"></div></div></div><div class="GE2Jnm"><div class="_0qFceF">Phụ Kiện &amp; Trang Sức Nữ</div></div></div></a></li><li class="image-carousel__item" style="padding: 0px; width: 5%;"><a class="home-category-list__category-grid" href="/Thể-Thao-Du-Lịch-cat.11035478"><div class="g3RFjs"><div class="_2QRysE"><div class="_3Jjuff +K-jRT"><div class="+K-jRT OooQQJ" style="background-image: url(&quot;https://down-vn.img.susercontent.com/file/6cb7e633f8b63757463b676bd19a50e4_tn&quot;); background-size: contain; background-repeat: no-repeat;"></div></div></div><div class="GE2Jnm"><div class="_0qFceF">Thể Thao &amp; Du Lịch</div></div></div></a></li><li class="image-carousel__item" style="padding: 0px; width: 5%;"><a class="home-category-list__category-grid" href="/Bách-Hóa-Online-cat.11036525"><div class="g3RFjs"><div class="_2QRysE"><div class="_3Jjuff +K-jRT"><div class="+K-jRT OooQQJ" style="background-image: url(&quot;https://down-vn.img.susercontent.com/file/c432168ee788f903f1ea024487f2c889_tn&quot;); background-size: contain; background-repeat: no-repeat;"></div></div></div><div class="GE2Jnm"><div class="_0qFceF">Bách Hóa Online</div></div></div></a></li><li class="image-carousel__item" style="padding: 0px; width: 5%;"><a class="home-category-list__category-grid" href="/Ô-Tô-Xe-Máy-Xe-Đạp-cat.11036793"><div class="g3RFjs"><div class="_2QRysE"><div class="_3Jjuff +K-jRT"><div class="+K-jRT OooQQJ" style="background-image: url(&quot;https://down-vn.img.susercontent.com/file/3fb459e3449905545701b418e8220334_tn&quot;); background-size: contain; background-repeat: no-repeat;"></div></div></div><div class="GE2Jnm"><div class="_0qFceF">Ô Tô &amp; Xe Máy &amp; Xe Đạp</div></div></div></a></li><li class="image-carousel__item" style="padding: 0px; width: 5%;"><a class="home-category-list__category-grid" href="/Nhà-Sách-Online-cat.11036863"><div class="g3RFjs"><div class="_2QRysE"><div class="_3Jjuff +K-jRT"><div class="+K-jRT OooQQJ" style="background-image: url(&quot;https://down-vn.img.susercontent.com/file/36013311815c55d303b0e6c62d6a8139_tn&quot;); background-size: contain; background-repeat: no-repeat;"></div></div></div><div class="GE2Jnm"><div class="_0qFceF">Nhà Sách Online</div></div></div></a></li><li class="image-carousel__item" style="padding: 0px; width: 5%;"><a class="home-category-list__category-grid" href="/Balo-Túi-Ví-Nam-cat.11035741"><div class="g3RFjs"><div class="_2QRysE"><div class="_3Jjuff +K-jRT"><div class="+K-jRT OooQQJ" style="background-image: url(&quot;https://down-vn.img.susercontent.com/file/18fd9d878ad946db2f1bf4e33760c86f_tn&quot;); background-size: contain; background-repeat: no-repeat;"></div></div></div><div class="GE2Jnm"><div class="_0qFceF">Balo &amp; Túi Ví Nam</div></div></div></a></li><li class="image-carousel__item" style="padding: 0px; width: 5%;"><a class="home-category-list__category-grid" href="/Thời-Trang-Trẻ-Em-cat.11036382"><div class="g3RFjs"><div class="_2QRysE"><div class="_3Jjuff +K-jRT"><div class="+K-jRT OooQQJ" style="background-image: url(&quot;https://down-vn.img.susercontent.com/file/4540f87aa3cbe99db739f9e8dd2cdaf0_tn&quot;); background-size: contain; background-repeat: no-repeat;"></div></div></div><div class="GE2Jnm"><div class="_0qFceF">Thời Trang Trẻ Em</div></div></div></a></li><li class="image-carousel__item" style="padding: 0px; width: 5%;"><a class="home-category-list__category-grid" href="/Đồ-Chơi-cat.11036932"><div class="g3RFjs"><div class="_2QRysE"><div class="_3Jjuff +K-jRT"><div class="+K-jRT OooQQJ" style="background-image: url(&quot;https://down-vn.img.susercontent.com/file/ce8f8abc726cafff671d0e5311caa684_tn&quot;); background-size: contain; background-repeat: no-repeat;"></div></div></div><div class="GE2Jnm"><div class="_0qFceF">Đồ Chơi</div></div></div></a></li><li class="image-carousel__item" style="padding: 0px; width: 5%;"><a class="home-category-list__category-grid" href="/Giặt-Giũ-Chăm-Sóc-Nhà-Cửa-cat.11036624"><div class="g3RFjs"><div class="_2QRysE"><div class="_3Jjuff +K-jRT"><div class="+K-jRT OooQQJ" style="background-image: url(&quot;https://down-vn.img.susercontent.com/file/cd8e0d2e6c14c4904058ae20821d0763_tn&quot;); background-size: contain; background-repeat: no-repeat;"></div></div></div><div class="GE2Jnm"><div class="_0qFceF">Giặt Giũ &amp; Chăm Sóc Nhà Cửa</div></div></div></a></li><li class="image-carousel__item" style="padding: 0px; width: 5%;"><a class="home-category-list__category-grid" href="/Chăm-Sóc-Thú-Cưng-cat.11036478"><div class="g3RFjs"><div class="_2QRysE"><div class="_3Jjuff +K-jRT"><div class="+K-jRT OooQQJ" style="background-image: url(&quot;https://down-vn.img.susercontent.com/file/cdf21b1bf4bfff257efe29054ecea1ec_tn&quot;); background-size: contain; background-repeat: no-repeat;"></div></div></div><div class="GE2Jnm"><div class="_0qFceF">Chăm Sóc Thú Cưng</div></div></div></a></li><li class="image-carousel__item" style="padding: 0px; width: 5%;"><a class="home-category-list__category-grid" href="/Voucher-Dịch-Vụ-cat.11035898"><div class="g3RFjs"><div class="_2QRysE"><div class="_3Jjuff +K-jRT"><div class="+K-jRT OooQQJ" style="background-image: url(&quot;https://down-vn.img.susercontent.com/file/b0f78c3136d2d78d49af71dd1c3f38c1_tn&quot;); background-size: contain; background-repeat: no-repeat;"></div></div></div><div class="GE2Jnm"><div class="_0qFceF">Voucher &amp; Dịch Vụ</div></div></div></a></li><li class="image-carousel__item" style="padding: 0px; width: 5%;"><a class="home-category-list__category-grid" href="/Dụng-cụ-và-thiết-bị-tiện-ích-cat.11116484"><div class="g3RFjs"><div class="_2QRysE"><div class="_3Jjuff +K-jRT"><div class="+K-jRT OooQQJ" style="background-image: url(&quot;https://down-vn.img.susercontent.com/file/e4fbccba5e1189d1141b9d6188af79c0_tn&quot;); background-size: contain; background-repeat: no-repeat;"></div></div></div><div class="GE2Jnm"><div class="_0qFceF">Dụng cụ và thiết bị tiện ích</div></div></div></a></li></ul>"""
htMl = BeautifulSoup(contents, 'html.parser')
danhmuc_s = htMl.find_all('a', {"href": True})
for danhmuc in danhmuc_s:
    print(danhmuc.get("href"))

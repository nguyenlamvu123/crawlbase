import time, threading, requests
import tkinter as tk

from funct import (
    # chrooome, readfile, findelem, clickkk, dangnhap, thich, spam,
    print_on_gui, delete_cache, getin4, stopandkillthread, brow__ser, gethtmlslist_bycategories, crawlfromhtml
    # root,text_widget,
)
from addr import ad, danhmuc_s, page


# Hàm thực thi cho mỗi luồng
# def work(email, passw, falivetok, fanpage):
#     sema.acquire()
#     driver = dangnhap(text_widget, email, passw, falivetok)
#
#     # TODO: confirm that fanpage is in shortcut as below
#     """<ul><li class=""><div data-visualcompletion="ignore-dynamic" style="padding-left: 8px; padding-right: 8px;"><a class="x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x87ps6o x1lku1pv x1a2a7pz x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1lliihq" href="https://www.facebook.com/61550060837697/" role="link" tabindex="0"><div class="x6s0dn4 x1q0q8m5 x1qhh985 xu3j5b3 xcfux6l x26u7qi xm0m39n x13fuv20 x972fbf x9f619 x78zum5 x1q0g3np x1iyjqo2 xs83m0k x1qughib xat24cr x11i5rnm x1mh8g0r xdj266r xeuugli x18d9i69 x1sxyh0 xurb0ha xexx8yu x1n2onr6 x1ja2u2z x1gg8mnh"><div class="x78zum5 xdt5ytf xq8finb x1xmf6yo x1e56ztr x1n2onr6 xamitd3 x1ywmky0 xnd27nj xv2ei83 x1og3r51 xv3fwf9"><div class="x1rg5ohu x1n2onr6 x3ajldb x1ja2u2z"><svg aria-hidden="true" class="x3ajldb" data-visualcompletion="ignore-dynamic" role="none" style="height: 36px; width: 36px;"><mask id=":re4:"><circle cx="18" cy="18" fill="white" r="18"></circle></mask><g mask="url(#:re4:)"><image x="0" y="0" height="100%" preserveAspectRatio="xMidYMid slice" width="100%" xlink:href="https://scontent.fhan18-1.fna.fbcdn.net/v/t39.30808-1/369711417_260752113574386_7427539448981885469_n.jpg?stp=cp0_dst-jpg_p86x86&amp;_nc_cat=106&amp;ccb=1-7&amp;_nc_sid=5f2048&amp;_nc_ohc=Yio-DODOOrQAX9RSi66&amp;_nc_ht=scontent.fhan18-1.fna&amp;oh=00_AfDhm9yZJZvpSCS_nukKE1ZMUCDTVEsKpOQWefds0E07yw&amp;oe=655F98DB" style="height: 36px; width: 36px;"></image><circle class="xbh8q5q x1pwv2dq xvlca1e" cx="18" cy="18" r="18"></circle></g></svg></div></div><div class="x6s0dn4 xkh2ocl x1q0q8m5 x1qhh985 xu3j5b3 xcfux6l x26u7qi xm0m39n x13fuv20 x972fbf x9f619 x78zum5 x1q0g3np x1iyjqo2 xs83m0k x1qughib xat24cr x11i5rnm x1mh8g0r xdj266r x2lwn1j xeuugli x18d9i69 x4uap5 xkhd6sd xexx8yu x1n2onr6 x1ja2u2z"><div class="x1qjc9v5 x1q0q8m5 x1qhh985 xu3j5b3 xcfux6l x26u7qi xm0m39n x13fuv20 x972fbf x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1qughib xat24cr x11i5rnm x1mh8g0r xdj266r x2lwn1j xeuugli x4uap5 xkhd6sd xz9dl7a xsag5q8 x1n2onr6 x1ja2u2z"><div class=""><div class="x78zum5 xdt5ytf xz62fqu x16ldp7u"><div class="xu06os2 x1ok221b"><span class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h" dir="auto"><span class="x1lliihq x6ikm8r x10wlt62 x1n2onr6" style="-webkit-box-orient: vertical; -webkit-line-clamp: 2; display: -webkit-box;">Chân mày phong thủy tốt</span></span></div></div></div></div></div></div><div class="x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x1ey2m1c xds687c xg01cxk x47corl x10l6tqk x17qophe x13vifvy x1ebt8du x19991ni x1dhq9h x1wpzbip" data-visualcompletion="ignore"></div></a></div></li><li class=""><div data-visualcompletion="ignore-dynamic" style="padding-left: 8px; padding-right: 8px;"><a class="x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x87ps6o x1lku1pv x1a2a7pz x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1lliihq" href="https://www.facebook.com/61550017030156/" role="link" tabindex="0"><div class="x6s0dn4 x1q0q8m5 x1qhh985 xu3j5b3 xcfux6l x26u7qi xm0m39n x13fuv20 x972fbf x9f619 x78zum5 x1q0g3np x1iyjqo2 xs83m0k x1qughib xat24cr x11i5rnm x1mh8g0r xdj266r xeuugli x18d9i69 x1sxyh0 xurb0ha xexx8yu x1n2onr6 x1ja2u2z x1gg8mnh"><div class="x78zum5 xdt5ytf xq8finb x1xmf6yo x1e56ztr x1n2onr6 xamitd3 x1ywmky0 xnd27nj xv2ei83 x1og3r51 xv3fwf9"><div class="x1rg5ohu x1n2onr6 x3ajldb x1ja2u2z"><svg aria-hidden="true" class="x3ajldb" data-visualcompletion="ignore-dynamic" role="none" style="height: 36px; width:36px;"><mask id=":re5:"><circle cx="18" cy="18" fill="white" r="18"></circle></mask><g mask="url(#:re5:)"><image x="0" y="0" height="100%" preserveAspectRatio="xMidYMid slice" width="100%" xlink:href="https://scontent.fhan18-1.fna.fbcdn.net/v/t39.30808-1/368615990_257235617259369_9118801414306001815_n.jpg?stp=cp0_dst-jpg_p86x86&amp;_nc_cat=106&amp;ccb=1-7&amp;_nc_sid=5f2048&amp;_nc_ohc=Xr68m6Wz3bEAX-pYpJD&amp;_nc_ht=scontent.fhan18-1.fna&amp;oh=00_AfCY0ICDKBpJBqK0r-Anmcm0tlzKfyG8mjv-zpxkfHqsuQ&amp;oe=655F89E9" style="height: 36px; width: 36px;"></image><circle class="xbh8q5q x1pwv2dq xvlca1e" cx="18" cy="18" r="18"></circle></g></svg></div></div><div class="x6s0dn4 xkh2ocl x1q0q8m5 x1qhh985 xu3j5b3 xcfux6l x26u7qi xm0m39n x13fuv20 x972fbf x9f619 x78zum5 x1q0g3np x1iyjqo2 xs83m0k x1qughib xat24cr x11i5rnm x1mh8g0r xdj266r x2lwn1j xeuugli x18d9i69 x4uap5 xkhd6sd xexx8yu x1n2onr6 x1ja2u2z"><div class="x1qjc9v5 x1q0q8m5 x1qhh985 xu3j5b3 xcfux6l x26u7qi xm0m39n x13fuv20 x972fbf x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1qughib xat24cr x11i5rnm x1mh8g0r xdj266r x2lwn1j xeuugli x4uap5 xkhd6sd xz9dl7a xsag5q8 x1n2onr6 x1ja2u2z"><div class=""><div class="x78zum5 xdt5ytf xz62fqu x16ldp7u"><div class="xu06os2 x1ok221b"><span class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h" dir="auto"><span class="x1lliihq x6ikm8r x10wlt62 x1n2onr6" style="-webkit-box-orient: vertical; -webkit-line-clamp: 2; display: -webkit-box;">Dáng chân mày phong thuỷ nữ</span></span></div></div></div></div></div></div><div class="x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x1ey2m1c xds687c xg01cxk x47corl x10l6tqk x17qophe x13vifvy x1ebt8du x19991ni x1dhq9h" data-visualcompletion="ignore"></div></a></div></li></ul>"""
#
#     driver = thich(driver=driver, fanpage=fanpage, li=switchpage)
#     spam(driver)
#     sema.release()


def worker(email, passw, falivetok, fanpage, thread_id: int or None = None):
    if thread_id is not None:
        print(f"Luồng {thread_id} đang làm việc")
    t1 = threading.Thread(target=work, args=(email, passw, falivetok, fanpage, ))
    t1.start()


def mult_thre():
    # Tạo một danh sách các luồng
    threads = []
    for em_pa in getin4():
        email_, passw_, falivetok_, fanpage_ = em_pa[0], em_pa[1], em_pa[2], em_pa[3]

        thread = threading.Thread(
            target=worker,
            args=(email_, passw_, falivetok_, fanpage_, len(threads),)
        )
        thread.start()
        threads.append(thread)

    # # Đợi cho tất cả các luồng hoàn thành
    # for thread in threads:
    #     thread.join()

    print("Tất cả các luồng đã hoàn thành công việc")


if __name__ == '__main__':
    gethtmlslist_bycategories()
    crawlfromhtml()
    # # num_threads: int = 4
    # # sema = threading.Semaphore(value=num_threads)
    # # Bsthread = tk.Button(
    # #     root,
    # #     text="single thread",
    # #     command=lambda: worker(em_test, pa_test, get_tok, fanpage)
    # # )
    # # Bsthread.pack(fill="both", expand=True)
    # # Bmthread = tk.Button(root, text="mutilthread", command=mult_thre)
    # # Bmthread.pack(fill="both", expand=True)
    # # Bstop = tk.Button(root, text="stop", command=stopandkillthread)  # TODO
    # # Bstop.pack(fill="both", expand=True)
    # # root.mainloop()
    # # # https://stackoverflow.com/questions/67653912/how-do-you-make-tkinter-gui-output-text-from-print-statement

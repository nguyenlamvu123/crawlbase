from urllib.request import urlopen

link = "https://stackoverflow.com/questions/68120200/python-get-html-from-website-opened-in-users-browser"
openedpage = urlopen(link)
content = openedpage.read()
code = content.decode("utf-8")
title = code.find("<title>")
title_start = title + len("<title>")
title_end = code.find("</title>")
full_title = code[title_start:title_end]
print(full_title)
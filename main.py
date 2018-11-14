from urllib import request
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
from os import system



hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari'
                     '/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

site = "http://1337x.to/popular-movies"


def print_out(string, _type, end="\n"):
    if _type != "":
        if string != "":
            if _type == "error":
                print(Fore.RED + "\n[-] Error: " + string, Style.RESET_ALL, end=end)
            elif _type == "success":
                print(Fore.LIGHTGREEN_EX + "\n" + string, Style.RESET_ALL, end=end)
            elif _type == "warning":
                print(Fore.YELLOW + "\n" + string, Style.RESET_ALL, end=end)
            elif _type == "normal":
                print(Fore.WHITE + string, end=end)


def line_prepender(line):
    with open('1337x.to_popular-movies.txt', 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)


def ext_movies(response):
    file = open('1337x.to_popular-movies.txt', 'w')
    count = skipped = new_movie = 0
    movies = [["" for i in range(6)] for i in range(50)]

    soup = BeautifulSoup(response, 'html.parser')
    table = soup.find('table', class_='table-list table table-responsive table-striped')
    table_data = table.find_all('tr')

    for data in table_data[1:]:
        try:
            count += 1

            a = data.find_all('a', href=True)
            name = BeautifulSoup(str(a[1]), "html.parser")
            name_str = name
            print(name)
            name_str = name.string.encode('ascii', 'ignore')
            file.write("{} )-\n".format(str(count)))

            movies[new_movie][0] = (name_str.decode('utf-8'))
            file.write("Name = {}\n".format(name_str.decode('utf-8')))

            file.write("Seeds = {}\n".format(data.contents[3].string))
            movies[new_movie][1] = (data.contents[3].string)

            file.write("Leechers = {}\n".format(data.contents[5].string))
            movies[new_movie][2] = (data.contents[5].string)

            file.write("Time = {}\n".format(data.contents[7].string))
            movies[new_movie][3] = (data.contents[7].string)


            size = ""

            size_str = str(data.contents[9])

            size_parser = BeautifulSoup(size_str, "html.parser")
            rslt = size_parser.find('td', class_='coll-4 size mob-vip')

            if rslt is None: # mob-uploader in "class"
                size_str = size_str[37:]
            else:            # mob-vip in "class"
                size_str = size_str[32:]
            try:
                for i in size_str:
                    if i == '<':
                        size = size_str[:size_str.index(i)]
                        continue
            except Exception as e:
                print("Error: ", str(e))

            file.write("Size = {}\n".format(size))
            movies[new_movie][4] = (size)

            file.write("Uploader = {}\n".format(data.contents[11].string))
            movies[new_movie][5] = (data.contents[11].string)

            file.write("-" * 100 + "\n\n")
            new_movie += 1
        except UnicodeEncodeError:
            skipped += 1
    file.close()

    line_prepender("Skipped Movies: " + str(skipped) + "\n")
    line_prepender("Total Movies: " + str(count) + "\n")

    print_out("[+] Total Movies: " + str(count), "success")
    print_out("[+] Skipped Movies: " + str(skipped), "success")

    return movies


def ext_magnet_uri():
    pass

if __name__ == '__main__':
    init()

    print_out("[*] Connecting...", "warning")
    req = request.Request(site, headers=hdr)
    res = request.urlopen(req)

    print_out("[*] Reading Response...", "warning")
    raw = res.read()

    print_out("[*] Writing To File...", "warning")
    movies = ext_movies(raw.decode('utf-8'))
    system('1337x.to_popular-movies.txt')

    exit()
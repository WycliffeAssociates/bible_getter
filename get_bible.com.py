import urllib.request
from bs4 import BeautifulSoup
import sys
import re


class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"


opener = AppURLopener()

allbooks = [
    {"gen": 50},
    {"exo": 40},
    {"lev": 27},
    {"num": 36},
    {"deu": 34},
    {"jos": 24},
    {"jdg": 21},
    {"rut": 4},
    {"1sa": 31},
    {"2sa": 24},
    {"1ki": 22},
    {"2ki": 25},
    {"1ch": 29},
    {"2ch": 36},
    {"ezr": 10},
    {"neh": 13},
    {"est": 10},
    {"job": 42},
    {"psa": 150},
    {"pro": 31},
    {"ecc": 12},
    {"sng": 8},
    {"isa": 66},
    {"jer": 52},
    {"lam": 5},
    {"ezk": 48},
    {"dan": 12},
    {"hos": 14},
    {"jol": 3},
    {"amo": 9},
    {"oba": 1},
    {"jon": 4},
    {"mic": 7},
    {"nam": 3},
    {"hab": 3},
    {"zep": 3},
    {"hag": 2},
    {"zec": 14},
    {"mal": 4},
    {"mat": 28},
    {"mrk": 16},
    {"luk": 24},
    {"jhn": 21},
    {"act": 28},
    {"rom": 16},
    {"1co": 16},
    {"2co": 13},
    {"gal": 6},
    {"eph": 6},
    {"php": 4},
    {"col": 4},
    {"1th": 5},
    {"2th": 3},
    {"1ti": 6},
    {"2ti": 4},
    {"tit": 3},
    {"phm": 1},
    {"heb": 13},
    {"jas": 5},
    {"1pe": 5},
    {"2pe": 3},
    {"1jn": 5},
    {"2jn": 1},
    {"3jn": 1},
    {"jud": 1},
    {"rev": 22}
]

if len(sys.argv) < 2:
    sys.exit("Enter book ID from www.bible.com")

bible_book = sys.argv[1]
antology = 'all'

if len(sys.argv) > 2:
    antology = sys.argv[2]

urls = dict()
for bookitem in allbooks:
    for bookcode, book_number in bookitem.items():
        urls[bookcode] = {}
        urls[bookcode]["code"] = bookcode
        urls[bookcode]["chapters"] = []

        for chap in range(int(book_number)):
            urls[bookcode]["chapters"].append(chap + 1)

bk_num = 0
for bookcode, bk_info in urls.items():
    usfm = list()
    title_done = False
    book_name = "Bookname"

    bk_num += 1
    if bk_num == 40:
        bk_num += 1

    if antology == "ot" and bk_num > 39:
        continue
    elif antology == "nt" and bk_num < 41:
        continue

    print("--------- " + str(bk_num).zfill(2) + "-" + bk_info["code"].upper() + " --------")

    for chap in bk_info["chapters"]:
        chapter = str(chap)

        print("Chapter: " + chapter)

        with opener.open('https://www.bible.com/en-GB/bible/' + bible_book + '/' + bookcode.upper() + '.' + chapter) as response:
            html_byte = response.read()
            html = html_byte.decode('utf-8')
            parser = BeautifulSoup(html, 'html.parser')

            # Insert book title
            if not title_done:
                ul = parser.find('ul', class_="book-list")
                active = ul.find('li', class_="active")
                book_name = active.text.strip()

                # write headers to the usfm file
                usfm.append("\\id " + bk_info["code"].upper() + " Unlocked Literal Bible \n")
                usfm.append("\\ide UTF-8 \n")
                usfm.append("\\h " + book_name + " \n")
                usfm.append("\\toc1 " + book_name + " \n")
                usfm.append("\\toc2 " + book_name + " \n")
                usfm.append("\\toc3 " + bk_info["code"].lower() + " \n")
                usfm.append("\\mt1 " + book_name + " \n\n")

                title_done = True

            usfm.append("\n\\s5 \n")
            usfm.append("\\c " + chapter + "\n")
            usfm.append("\\p \n")

            verse = None
            text = None

            chapter_body = parser.find('div', class_="chapter")

            # Continue if there is no chapter
            if not chapter_body:
                continue

            # Get the list of verses
            verses = chapter_body.find_all('span', class_="verse")

            for child in verses:
                verse = child.find('span', class_="label")
                text = None
                contents = child.find_all('span', class_="content")
                for content in contents:
                    if not text:
                        text = ""
                    if content.text.strip() != "":
                        text += content.text.strip() + " "

                if verse and not re.match(r'^[0-9-]+$', verse.text.strip()):
                    verse = None

                if verse and text:
                    usfm.append("\\v " + verse.text.strip() + " " + text + "\n")
                elif text:
                    if text.strip() != "":
                        usfm.append(text + "\n")

    # save usfm to file
    with(open(str(bk_num).zfill(2) + "-" + bookcode.upper() + ".usfm", "w", encoding="utf8", newline='\n')) as file:
        for line in usfm:
            file.write(line)

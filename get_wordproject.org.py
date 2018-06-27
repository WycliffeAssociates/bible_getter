import urllib.request
from bs4 import BeautifulSoup, NavigableString
import sys
import os


class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"


opener = AppURLopener()

allbooks = [
    "gen",
    "exo",
    "lev",
    "num",
    "deu",
    "jos",
    "jdg",
    "rut",
    "1sa",
    "2sa",
    "1ki",
    "2ki",
    "1ch",
    "2ch",
    "ezr",
    "neh",
    "est",
    "job",
    "psa",
    "pro",
    "ecc",
    "sng",
    "isa",
    "jer",
    "lam",
    "ezk",
    "dan",
    "hos",
    "jol",
    "amo",
    "oba",
    "jon",
    "mic",
    "nam",
    "hab",
    "zep",
    "hag",
    "zec",
    "mal",
    "mat",
    "mrk",
    "luk",
    "jhn",
    "act",
    "rom",
    "1co",
    "2co",
    "gal",
    "eph",
    "php",
    "col",
    "1th",
    "2th",
    "1ti",
    "2ti",
    "tit",
    "phm",
    "heb",
    "jas",
    "1pe",
    "2pe",
    "1jn",
    "2jn",
    "3jn",
    "jud",
    "rev"
]

if len(sys.argv) < 2:
    sys.exit("Enter book code from www.wordproject.org/bibles/")

bible_book = sys.argv[1]
antology = 'all'

if len(sys.argv) > 2:
    antology = sys.argv[2]

print("Collecting the list of all the chapters. Please wait...")

urls = dict()

for i, bookcode in enumerate(allbooks):
    booknum = i + 1

    if antology == "ot" and booknum > 39:
        continue
    elif antology == "nt" and booknum < 40:
        continue

    with opener.open('https://www.wordproject.org/bibles/' + bible_book + '/' + str(booknum).zfill(2) + '/1.htm') as response:
        parser = BeautifulSoup(response, 'html5lib')

        book_body = parser.find('div', class_='textHeader')

        if not book_body or not book_body.h2:
            continue

        book = book_body.h2.text

        urls[str(booknum)] = dict()
        urls[str(booknum)]["code"] = bookcode
        urls[str(booknum)]["name"] = book.strip()
        urls[str(booknum)]["chapters"] = []
        urls[str(booknum)]["chapters"].append(1)

        chapters = parser.find_all('a', class_='chap')

        for chapter in chapters:
            urls[str(booknum)]["chapters"].append(chapter.text.strip())

for bk_num, bk_info in urls.items():
    book_number = str(bk_num)

    wa_book_num = int(bk_num)
    if wa_book_num > 39:
        wa_book_num += 1

    if antology == "ot" and wa_book_num > 39:
        continue
    elif antology == "nt" and wa_book_num < 41:
        continue

    usfm = list()

    # write headers to the usfm file
    usfm.append("\\id " + bk_info["code"].upper() + " Unlocked Literal Bible \n")
    usfm.append("\\ide UTF-8 \n")
    usfm.append("\\h " + bk_info["name"] + " \n")
    usfm.append("\\toc1 " + bk_info["name"] + " \n")
    usfm.append("\\toc2 " + bk_info["name"] + " \n")
    usfm.append("\\toc3 " + bk_info["code"].lower() + " \n")
    usfm.append("\\mt1 " + bk_info["name"] + " \n\n")

    print("--------- " + str(wa_book_num).zfill(2) + "-" + bk_info["code"].upper() + " --------")

    for chap in bk_info["chapters"]:
        chapter = str(chap)

        print("Chapter: " + chapter)

        with opener.open('https://www.wordproject.org/bibles/' + bible_book + '/' + str(book_number).zfill(
                2) + '/' + chapter + '.htm') as response:
            parser = BeautifulSoup(response, 'html5lib')

            book_body = parser.find('div', class_='textHeader')
            book = book_body.h2.text

            usfm.append("\n\\s5 \n")
            usfm.append("\\c " + chapter + "\n")
            usfm.append("\\p \n")

            verse = None
            text = None

            chapter_body = parser.find(id="textBody")
            p = chapter_body.p

            for a in p.findAll('a'):
                a.unwrap()
            for div in p.findAll('div'):
                div.unwrap()

            for child in p.children:
                if child.name == "br":
                    continue

                if child.name == "span" and 'verse' in child['class']:
                    next_verse = child.string.strip()

                    if verse and verse != next_verse and text:
                        usfm.append("\\v " + verse + " " + text + "\n")
                        text = None
                    verse = next_verse
                else:
                    if verse:
                        if not text:
                            if type(child) is NavigableString:
                                text = child.string.strip() + " "
                            else:
                                text = child.text.strip() + " "
                        else:
                            if type(child) is NavigableString:
                                text += child.string.strip() + " "
                            else:
                                text += child.text.strip() + " "

            if verse and text:
                usfm.append("\\v " + verse + " " + text + "\n")

    folder = os.path.join("wordproject.org", bible_book)
    if not os.path.exists(folder):
        os.makedirs(folder)

    path = os.path.join(folder, str(wa_book_num).zfill(2) + "-" + bk_info["code"].upper() + ".usfm")
    with(open(path, "w", encoding="utf8", newline='\n')) as file:
        for line in usfm:
            file.write(line)

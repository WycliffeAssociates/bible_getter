# Bible Getter
These scripts help to get bible in usfm format from wordproject.org and bible.com

# Installation
1. Download and install python 3. [64-bit version](https://www.python.org/ftp/python/3.6.5/python-3.6.5-amd64.exe "64-bit version") or [32-bit version](https://www.python.org/ftp/python/3.6.5/python-3.6.5.exe "32-bit version"). During installation make sure that "Add python 3.6 to PATH" is selected. Wait until installation is finished.
2. Open command prompt and install "Beautiful Soup" by entering the following command:

`pip install beautifulsoup4`

3. Install Html5Lib by entering the following command:

`pip install html5lib`

# How to use

Download and extract script files

#### Wordproject.org
1. Open [www.wordproject.org/bibles/](https://www.wordproject.org/bibles/ "wordproject.org") in your browser, find the desired bible version in the list and open it. Find the bible code in URL of address bar (i.e. "www.wordproject.org/bibles/***kj***/". In this case ***kj*** is the code you need. Keep it in mind.)
2. Open command prompt in the folder with script files. Simply hold down the Shift key and right-click a folder. The context menu will contain an entry, ‘Open command window here.”
3. To get the entire bible enter the following command:

`python get_wordproject.org.py kj`

where ***kj*** is the code you obtained in **step 1**

If you want to get just Old Testament or New Testament type following commands:

`python get_wordproject.org.py kj ot`

`python get_wordproject.org.py kj nt`

#### Bible.com
1. Open [www.bible.com/bible](https://www.bible.com/bible "bible.com") in your browser, find the desired bible version and open it. Find the bible ID in URL of address bar (i.e. "www.bible.com/bible/***59***/GEN.1.esv". In this case ***59*** is the ID you need. Keep it in mind.)
2. Open command prompt in the folder with script files.
3. To get the entire bible enter the following command:

`python get_bible.com.py 59`

where ***59*** is the code you obtained in **step 1**

If you want to get just Old Testament or New Testament type following commands:

`python get_bible.com.py 59 ot`

`python get_bible.com.py 59 nt`


**To Open/Edit usfm files Notepad++ is recommended**.

You can download it from here: [notepad-plus-plus.org/download](https://notepad-plus-plus.org/download "notepad-plus-plus.org/download")

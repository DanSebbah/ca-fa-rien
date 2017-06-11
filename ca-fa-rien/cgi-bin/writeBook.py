import os
import shutil
from ebooklib import epub
import glob
import re
import zipfile

def generate():
    #os.chdir(os.getcwd() + "/epubGen/tmp")
    os.chdir("/var/www/html/ca-fa-rien/cgi-bin/epubGen/tmp")
    #print(os.getcwd() )

    zip_ref = zipfile.ZipFile("sefariaContent.zip", 'r')
    zip_ref.extractall("sefariaContent")
    zip_ref.close()


    #shutil.copy("/var/tmp/droopy/sefariaContent.zip","./sefariaContent")


    def atoi(text):
        return int(text) if text.isdigit() else text

    def natural_keys(text):
        '''
        alist.sort(key=natural_keys) sorts in human order
        http://nedbatchelder.com/blog/200712/human_sorting.html
        (See Toothy's implementation in the comments)
        '''
        return [ atoi(c) for c in re.split('(\d+)', text) ]


    book = epub.EpubBook()

    # set metadata
    book.set_language('en')

    book.add_author('Edited by Danou')
    #book.add_author('sefaria.org')

    # add cover image

    credits = epub.EpubHtml(title='Credits', file_name='credits.xhtml', lang='en')
    credits.content=u'<html><head></head><body><h1>Credits</h1><p>Data from <a href=http://www.sefaria.org>sefaria.org</a> : please support them, their work is awesome !<br/>EPUB Document generated with <a href=https://pypi.python.org/pypi/EbookLib/0.15>ebooklib</a> python library<br/><br/>Developped and brought to you by Danou !</p></body></html>'

    # add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # define CSS style
    file = open("resource/safarien.css", "r")
    #style = file.read() 
    style = ""
    for line in file:
        #if("not_in_epub" not in line): #todo : uncomment when epub will work >_< correctly
            style += line;
    file.close()
    nav_css = epub.EpubItem(uid="safarien", file_name="safarien.css", media_type="text/css", content=style)

    # define font
    file = open("resource/fonts/TaameyFrankCLM-Medium.ttf", "r") 
    myFont = file.read() 
    file.close()

    font_file = epub.EpubItem(uid="TaameyFrankCLM-Medium", file_name="fonts/TaameyFrankCLM-Medium.ttf", media_type="application/x-font-truetype", content=myFont)

    listOfChapters = []

    # create chapter

    i = 1
    fileList = glob.glob('./sefariaContent/sefaria*.html')
    fileList = sorted(fileList, key=natural_keys)

    bookName = fileList[0].replace(".html","").replace("./sefariaContent/sefaria","")
    bookName = re.search("[^[0-9]*",bookName).group(0)
    
    book.set_identifier('Danou_Ca_fa_rien_'+bookName)
    book.set_title(bookName)

    commandLineAddTitleInCover = "convert -pointsize 75 -font FreeSerif -undercolor white -fill black -gravity center -draw 'text -100,-300 MY_TITLE_LONG_LONG' resource/baseCover.png cover.png"
    commandLineAddTitleInCover = commandLineAddTitleInCover.replace('MY_TITLE_LONG_LONG', bookName)
    os.system(commandLineAddTitleInCover)
    book.set_cover("image.png", open('cover.png', 'rb').read())


    ##for all files create a chapter
    for fileName in fileList:
        currentChapter = epub.EpubHtml(title=fileName.replace(".html","").replace("./sefariaContent/sefaria",""), file_name='chap_'+str(i)+'.xhtml', lang='en')
        file = open(fileName, "r")#, "utf-8") 
        currentChapter.content= file.read() 
        file.close()
        currentChapter.title = re.search("<h1[^>]*>(.*)</h1>", currentChapter.content).group(1).replace("_"," ")

        currentChapter.content = currentChapter.content.replace("<b/>","</b>").replace("<i/>","</i>").replace("<strong/>","</strong>").replace("<i></i>","").replace("<u/>","</u>")
        currentChapter.add_item(nav_css)
        listOfChapters.append(currentChapter)
        i = i + 1

    # add chapters in book
    for chapter in listOfChapters:
        book.add_item(chapter)
    book.add_item(credits)

    # define Table Of Contents
    book.toc = (epub.Link('http://dan.sebbah.fr/ca-fa-rien/index.html?book='+bookName, 'Visit us !',"intro"), 
        epub.Link('http://sefaria.org/'+bookName+'.1', 'Visit Sefaria.org !',"intro"), 
    (epub.Section(bookName),
    (listOfChapters))
    )


    # add CSS file in book
    book.add_item(nav_css)

    # add font file in book
    book.add_item(font_file)

    # basic spine
    book.spine = ['cover', 'nav']
    book.spine.extend(listOfChapters)
    book.spine.append(credits)

    # write to the file
    massechetFilename = bookName + '.epub'
    epub.write_epub(massechetFilename, book, {})

    #print("Generation ok")

    shutil.rmtree("./sefariaContent")
    os.remove("./sefariaContent.zip")
    os.makedirs("./sefariaContent")

    return os.getcwd().replace("/var/www/html/ca-fa-rien/","./") + "/" + massechetFilename


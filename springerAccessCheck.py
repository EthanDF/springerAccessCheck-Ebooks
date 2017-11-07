import csv
import codecs
import urllib.request, urllib.error

def readFile():
    """should be a CSV file called springerList.csv with Bib (local id), Title, Link"""
    fileName = 'springerList.csv'
    checkList = []
    with codecs.open(fileName, 'r', encoding='utf-8') as f:
        a = csv.reader(f)
        checkList = list(a)

    return checkList

def writeResults(resultList):
    """will write Bib, Title, Link, True means ok, False means problem, error 404 means bad link"""
    resultsLog = 'Results.csv'
    with codecs.open(resultsLog, 'a', encoding='utf-8') as x:
        wr = csv.writer(x,quoting=csv.QUOTE_ALL)
        wr.writerow(resultList)


def getPageSource(url):
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read()
    except urllib.error.HTTPError as e:
        html = str(e.code).encode()

    return html

def checkSpringerAccess():

    accessIndicator = "'HasAccess':'Y'"
    error404 = '404'
    useError = error404.encode()

    # get checkList
    checkList = readFile()
    for title in checkList:
        resultString = []
        if title[0] == 'BIB_DOC_NUM':
            continue
        bibNumber = title[0]
        bookTitle = title[1]
        bookURL = title[2]
        access = False

        readPageSource = getPageSource(bookURL)
        if readPageSource == useError:
            access = '404 Error'

        if readPageSource.decode().find(accessIndicator) > 0:
                access = True

        resultString = [bibNumber, bookTitle, bookURL, access]
        writeResults(resultString)

checkSpringerAccess()
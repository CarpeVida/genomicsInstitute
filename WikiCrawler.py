"""This tool gets every link from a page and pulls the html from each of those links."""

import bs4 as bs
import urllib.request


sauce=urllib.request.urlopen('http://genomewiki.ucsc.edu/genecats/index.php/Special:AllPages').read()
saucePublic = urllib.request.urlopen('http://genomewiki.ucsc.edu/index.php/Special:AllPages').read()
soupGenecats = bs.BeautifulSoup(sauce,'lxml')
soupPublic = bs.BeautifulSoup(saucePublic, 'lxml')

count = 0
searchedCount = 0
searchTerms = ['hgwdev.soe','hgwdev.cse','hgwdev.sdsc.edu','genome-test.soe','genome-test.cse']
pages = []
hitList = []


# Grabs all links from wiki All Pages page.
for url in soupPublic.find_all('a'):
    pages.append(str(url.get('href')))
    count += 1
print(str(count) + " page links grabbed")


# goes through found links html pages and searches for search terms.
for url in pages:
    searchedCount += 1
    if url == 'None' or 'http' in url or 'www' in url or 'Genecats:Privacy' in url or 'Genecats:About' in url:
        continue
    if 'Genecats:General' in url:
        continue
    prefixAddedUrl= 'http://genomewiki.ucsc.edu' + str(url)
    print('searching ' + prefixAddedUrl)

    eachPage = urllib.request.urlopen(prefixAddedUrl).read()
    strDump = str(bs.BeautifulSoup(eachPage,'lxml'))
    for searchTerm in searchTerms:
        if searchTerm in strDump:
            print(url + " HAS " + searchTerm)
            hitList.append(prefixAddedUrl)
            hitList.append(searchTerm)
    print(str(searchedCount))
print(len(hitList), " hits for search Terms")
print(hitList)




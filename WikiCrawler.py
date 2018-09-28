"""This tool gets every link from a page and pulls the html from each of those links."""

import bs4 as bs
import urllib.request
import urllib
import ssl
ssl._create_default_https_context = ssl._create_unverified_context #called monkeypatching
errorCount = 0
totalInnerLinkCount = 0

# context = ssl._create_unverified_context()

def main():
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
    for url in soupPublic.find_all('a') and soupGenecats.find_all('a'):
        pages.append(str(url.get('href')))
        count += 1
    print(str(count) + " page links grabbed")


    # goes through found links html pages and searches for search terms.
    for url in pages[0:50]: #remove slice to allow full search

        if url == 'None' or 'http' in url or 'www' in url or 'Genecats:Privacy' in url or 'Genecats:About' in url:
            continue
        if 'Genecats:General' in url:
            continue
        prefixAddedUrl= 'http://genomewiki.ucsc.edu' + str(url)
        print('searching ' + prefixAddedUrl)
        searchedCount += 1
        eachPage = urllib.request.urlopen(prefixAddedUrl)
        strDump = str(bs.BeautifulSoup(eachPage,'lxml'))
        # print(strDump)
        for searchTerm in searchTerms:
            if searchTerm in strDump:
                print(url + " HAS " + searchTerm)
                hitList.append(prefixAddedUrl)
                hitList.append(searchTerm)
        print(str(searchedCount)+" pages searched so far")
        recursiveLinkChecker(prefixAddedUrl)
    print(len(hitList), " total hits for search Terms")
    print(hitList)
    print(errorCount, " non-opening wiki links")
    print(totalInnerLinkCount, "total links searched")

#Goes through linkAddress, searches for links in html dump, gets status of each of those pages
def recursiveLinkChecker(linkAddress):
    linkSauce= urllib.request.urlopen(linkAddress) #removed context=context
    linkSoup = bs.BeautifulSoup(linkSauce,'lxml')
    innerLinkCount =0
    for aTag in linkSoup.find_all('a'):
        innerLinkCount += 1
        hrefLink = str(aTag.get('href'))
        if hrefLink[0] =='/':
            # print('Internal Link Skipped')
            continue
            # prefixAddedUrl = 'http://genomewiki.ucsc.edu' + str(innerLink)
        elif hrefLink == "None":
            # print('None found')
            continue
        elif hrefLink[0] =='#':
            continue
            # print('Hash found')
        elif 'genomewiki' in hrefLink:
            continue
            print('genome wiki link found')
        elif 'mediawiki' in hrefLink:
            # print(hrefLink)
            continue
            print('wiki link found')
        else:
            # print(hrefLink)
            # innerLink=urllib.urlopen(hrefLink)
            # innerLink.getCode()
            try:
                sauce = urllib.request.urlopen(hrefLink).read()
                soup = bs.BeautifulSoup(sauce, 'lxml')
                # print('No error opening ', hrefLink)
            # except (urllib.error.HTTPError, urllib.error.URLError) as error:
            except Exception as error:
                global errorCount
                errorCount += 1
                print(error, " found in below link")
                print(hrefLink)
    print(innerLinkCount, "inner links checked")
    global totalInnerLinkCount
    totalInnerLinkCount += innerLinkCount

main()

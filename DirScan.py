#! /usr/bin/python
#coding = utf-8
from multiprocessing.dummy import Pool as ThreadPool
import urlparse,argparse,requests

headers = {
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
'Accept-Encoding': 'gzip, deflate, compress',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
"Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0"
}


def ErrorGet(url):
    global errpagetext
    errpayload = "/0xFA.html"
    #url1 = urlparse.urljoin(url,errpayload)
    url1 = url+errpayload
    try:
        r = requests.get(url1, headers=headers, timeout=10)
        errpagetext = r.text
        code = r.status_code
    except Exception,e:
        print 'The %s Error' % url

def ScanDir(url):
    #print headers
    q = requests.get(url, headers=headers, allow_redirects=False, timeout=10)
    pagetext = q.text
    code = q.status_code
    if code == 200:
        if  pagetext != errpagetext:
            print url
    #elif code ==403:
        #print url
    return
    #print page
    #print code

def DirScan(url):
    hostuser = url.split('.')
    hostuser = hostuser[len(hostuser)-2]
    scan =  [hostuser+'.rar',hostuser+'.zip',hostuser+hostuser+'.rar',hostuser+'.rar',hostuser+'.tar.gz',hostuser+'.tar',hostuser+'123.zip',hostuser+'123.tar.gz',hostuser+hostuser+'.zip',hostuser+hostuser+'.tar.gz',hostuser+hostuser+'.tar',hostuser+'.bak']
    f = open('mulu.txt','r')
    lujing = f.read().split('\n')
    Wordlist = scan+lujing
    pool = ThreadPool(5)
    result = []
    for i in range(len(Wordlist)):
        Dict = Wordlist[i]
        url1 = urlparse.urljoin(url,Dict)
        result.append(url1)
    try:
        pool.map(ScanDir, result)
        pool.close()
        pool.join()
        print "All Dict Run Over"
    except Exception,e:
        print 'The %s Error!' %url

if __name__ == '__main__':
    fo = open('jd.txt','r')
    mubiao = fo.read().split('\n')
    for i in range(len(mubiao)):
        url = 'http://'+mubiao[i]
        ErrorGet(url)
        DirScan(url)

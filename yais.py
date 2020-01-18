import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
import os 
import sys
import argparse 
 
path='destdir' 
SCROLL_PAUSE_TIME = 0.5
nfetched=1000
DEBUG=False
urltobescraped=""
options = Options()

def init_driver():
    driver = webdriver.Firefox(options=options)
    driver.wait = WebDriverWait(driver, 15)
    return driver

def downloadall(list):
    suffix=0
    for url in list: 
        try:
            # image.get_attribute('src')
            response=requests.get(url, stream=True)
    #       print (response.headers['content-type'])
        except Exception:
            if DEBUG:
                print ("problem getting single image:" + "n=" + str(suffix)+" "+ url)
        try:
            extension = response.headers['content-type'].split('/')[-1]
            if "svg" in extension:
                raise Exception('undesired extension '+str(extension))
            f=open('{dirname}/img_{suffixstr}.{extension}'.format(dirname=path, suffixstr="{0:04d}".format(suffix),extension=extension ), 'wb')
            f.write(response.content)
            f.close() 
        except Exception:
            if DEBUG:
                print ("rejected dowload ... " + "n=" + str(suffix)+" "+ url)
        suffix=suffix+1

##########     customized url scraper

########## image.google.com section 

#### https://www.google.com/search?q=sturmovik&tbm=isch&
def lookup_google(driver, query,ntobefetched):
    #### don't take in account the pushing of the button to obtain more results. 
    urlslist= []
    urltobescraped="https://www.google.com/search?q="+query+"&tbm=isch&"
    driver.get(urltobescraped)

    try:

# Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
    # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    except TimeoutException:
        print("problem scrolling down")
    try:
        images = driver.find_elements_by_tag_name('img')
#        images = driver.find_elements_by_class_name("mimg");
    except Exception:
        print ("unable to find img tag")
    for image in images:
        url=image.get_attribute('src')
        print (url) 
#        if "https://" in url:
        urlslist.append(url)
#        else:
#            if DEBUG:
#                print ("unacceptable image url " +"n=" + str(suffix)+" "+ url  )
    return(urlslist) 

################################################

########## duckduckgo.com

### https://duckduckgo.com/?q=sturmovik+&t=h_&iax=images&ia=images
def lookup_duckduckgo(driver, query,ntobefetched):
    urlslist= []
    urltobescraped="https://duckduckgo.com/?q="+query+"&t=h_&iax=images&ia=images"
    driver.get(urltobescraped)

    try:
# Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
    # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    except TimeoutException:
        print("problem scrolling down")
    try:
#        images = driver.find_elements_by_tag_name('img')
##        images = driver.find_elements_by_class_name("mimg");
        images = driver.find_elements_by_class_name("tile--img__img");
    except Exception:
        print ("unable to find img tag")
    for image in images:
        url=image.get_attribute('src')
        if "https://" in url:
            urlslist.append(url)
        else:
            if DEBUG:
                print ("unacceptable image url " +"n=" + str(suffix)+" "+ url  )
    return(urlslist) 

################################################

########## yandex.com
### https://yandex.com/images/search?text=sturmovik &
# not yet implemented 

########## picsearch.com
### https://www.picsearch.com/index.cgi?q=sturmovik

def lookup_picsearch(driver, query,ntobefetched):
    urlslist= []
    urltobescraped="https://www.picsearch.com/index.cgi?q="+query
    driver.get(urltobescraped)

    try:

# Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
    # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    except TimeoutException:
        print("problem scrolling down")
    try:
#        images = driver.find_elements_by_tag_name('img')
        images = driver.find_elements_by_class_name("thumbnail");
    except Exception:
        print ("unable to find img tag")
    for image in images:
        url=image.get_attribute('src')
        if "https://" in url:
            urlslist.append(url)
        else:
            if DEBUG:
                print ("unacceptable image url " +"n=" + str(suffix)+" "+ url  )
    return(urlslist) 

################################################

#### BING

########## 
def lookup_bing(driver, query,ntobefetched):
    urlslist= []
    urltobescraped="https://www.bing.com/images/search?q="+query+"+&qs=n&form=QBILPG&sp=-1&pq="+query+"+&sc=1-13&ch="+str(ntobefetched)
    driver.get(urltobescraped)

    try:

# Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
    # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    except TimeoutException:
        print("problem scrolling down")
    try:
#        images = driver.find_elements_by_tag_name('img')
        images = driver.find_elements_by_class_name("mimg");
    except Exception:
        print ("unable to find img tag")
    for image in images:
        url=image.get_attribute('src')
        if "https://" in url:
            urlslist.append(url)
        else:
            if DEBUG:
                print ("unacceptable image url " +"n=" + str(suffix)+" "+ url  )
    return(urlslist) 

################################################

def getOptions(args=sys.argv[1:]):
    parser=argparse.ArgumentParser(description='a scraper to collect photo')
    parser.add_argument('searchstring', help="string to be searched") 
    parser.add_argument('-n','--ntobefetched', help='try to fetch at least n images', type=int, default='1000')
    parser.add_argument('-t','--scroll-pause-time', help='time to wait between two simulated scroll\nWarning the default value is 0.5 but if you experience problems feel free to modify', default='0.5',dest='scrollpausetime' ) 
    parser.add_argument('-d','--debug',help='enables debug info', action='store_true' )
    parser.add_argument('-H','--headless',help='enables headless mode', action='store_true' )
    opt=parser.parse_args(args)
    return(opt) 


if __name__ == "__main__":
    try:
        os.mkdir(path)
    except OSError:
        if DEBUG:
            print ( path + "already existing") 

    opt=getOptions() 
    sestring=opt.searchstring
    ntobefetched=opt.ntobefetched
    DEBUG=opt.debug
    SCROLL_PAUSE_TIME=float(opt.scrollpausetime)
    if opt.headless :
        options.headless = True
    driver = init_driver()

    ul=lookup_bing(driver, sestring, ntobefetched)
    ul1=lookup_duckduckgo(driver, sestring, ntobefetched)
    ul2=lookup_picsearch(driver, sestring, ntobefetched)
    ul=ul+ul1+ul2

    downloadall(ul) 
##    for i in ul:
##        print(i)
    time.sleep(5)
    driver.quit()


# -*- coding: utf-8 -*-

import os
import json
import requests
import cloudscraper

from time import sleep
from colorama import init
from moviepy.editor import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from html.parser import HTMLParser

length = 1
count = 0
maindata = []
RED = '\033[1;31m'
LRED = '\033[1;31m'
WHITE = '\033[1;37m'
GREEN = '\033[0;32m'

email = 'deepakplay14@gmail.com'

driver  =  webdriver.Chrome(executable_path='chromedriver.exe')

JS_DROP_FILES = "var c=arguments,b=c[0],k=c[1];c=c[2];for(var d=b.ownerDocument||document,l=0;;){var e=b.getBoundingClientRect(),g=e.le"
JS_DROP_FILES = JS_DROP_FILES + "ft+(k||e.width/2),h=e.top+(c||e.height/2),f=d.elementFromPoint(g,h);if(f&&b.contains(f))break;if(1<++l)throw b=Error('"
JS_DROP_FILES = JS_DROP_FILES + "Element not intractable'),b.code=15,b;b.scrollIntoView({behavior:'instant',block:'center',inline:'center'})}var a=d.c"
JS_DROP_FILES = JS_DROP_FILES + "reateElement('INPUT');a.setAttribute('type','file');a.setAttribute('multiple','');a.setAttribute('style','position:fix"
JS_DROP_FILES = JS_DROP_FILES + "ed;z-index:2147483647;left:0;top:0;');a.onchange=function(b){a.parentElement.removeChild(a);b.stopPropagation();var c="
JS_DROP_FILES = JS_DROP_FILES + "{constructor:DataTransfer,effectAllowed:'all',dropEffect:'none',types:['Files'],files:a.files,setData:function(){},get"
JS_DROP_FILES = JS_DROP_FILES + "Data:function(){},clearData:function(){},setDragImage:function(){}};window.DataTransferItemList&&(c.items=Object.setPr"
JS_DROP_FILES = JS_DROP_FILES + "ototypeOf(Array.prototype.map.call(a.files,function(a){return{constructor:DataTransferItem,kind:'file',type:a.type,get"
JS_DROP_FILES = JS_DROP_FILES + "AsFile:function(){return a},getAsString:function(b){var c=new FileReader;c.onload=function(a){b(a.target.result)};c.re"
JS_DROP_FILES = JS_DROP_FILES + "adAsText(a)}}}),{constructor:DataTransferItemList,add:function(){},clear:function(){},remove:function(){}}));['dragent"
JS_DROP_FILES = JS_DROP_FILES + "er','dragover','drop'].forEach(function(a){var b=d.createEvent('DragEvent');b.initMouseEvent(a,!0,!0,d.defaultView,0,0"
JS_DROP_FILES = JS_DROP_FILES + ",0,g,h,!1,!1,!1,!1,0,null);Object.setPrototypeOf(b,null);b.dataTransfer=c;Object.setPrototypeOf(b,DragEvent.prototype)"
JS_DROP_FILES = JS_DROP_FILES + ";f.dispatchEvent(b)})};d.documentElement.appendChild(a);a.getBoundingClientRect();return a;"

def drop_files(element, files, offsetX=0, offsetY=0):
    driver = element.parent
    isLocal = not driver._is_remote or '127.0.0.1' in driver.command_executor._url
    paths = []    
    for file in (files if isinstance(files, list) else [files]) :
        if not os.path.isfile(file) :
            raise FileNotFoundError(file)
        paths.append(file if isLocal else element._upload(file))
    value = '\n'.join(paths)
    elm_input = driver.execute_script(JS_DROP_FILES, element, offsetX, offsetY)
    elm_input._execute('sendKeysToElement', {'value': [value], 'text': value})
    return


WebElement.drop_files = drop_files


def hasxpath(x_path):
    try:
        driver.find_element_by_xpath(x_path)
        return True
    except:
        return False


def countxpath(x_path):
    count = 0
    try:
        while True:
            driver.find_element_by_xpath(x_path+'['+str(count+1)+']')
            count = count+1
    except:
        return count


def init_web():
    driver.get('https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent')
    driver.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click()
    driver.find_element_by_xpath('//input[@type="email"]').send_keys(email)
    driver.find_element_by_xpath('//*[@id="identifierNext"]/div/span/span').click()
    sleep(4)
    driver.find_element_by_xpath('//*[@id="password"]').click()
    input("Enter password in the browser and press Enter")
    #driver.find_element_by_xpath('//input[@type="password"]').send_keys(password)
    #driver.find_element_by_xpath('//*[@id="passwordNext"]/div/span/span').click()
    sleep(2)
    driver.get('https://studio.youtube.com/channel/UC5xNyuT_WPsOimPu0p2uD_w/')
    driver.find_element_by_xpath('//*[@id="avatar-btn"]').click()
    sleep(1)
    driver.find_element_by_xpath('//*[text()="Switch account"]').click()
    sleep(1)
    channel = 'FreeStockVid'
    for i in range(1,countxpath('//div[@id="contents"]/ytd-account-item-renderer')):
        x_path = '//div[@id="contents"]/ytd-account-item-renderer['+str(i)+']'
        if channel in driver.find_element_by_xpath(x_path).get_attribute('innerHTML'):
            driver.find_element_by_xpath(x_path).click()
            break
    return    


def shorturl(surl):
    response = requests.put( "https://api.shorte.st/v1/data/url",
                            {"urlToShorten":surl},
                            headers={"public-api-token": "2b613dc139bf558d6ae636ce9687f4fc"})
    decoded_response = json.loads(response.content)
    open('shrinkurl.txt','a').write(decoded_response['shortenedUrl']+'\n')
    return decoded_response['shortenedUrl']


def is_downloadable(url):
    content_type = requests.head(url, allow_redirects=True).headers.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True


def convertvideo(vidin, vidout):
    video = VideoFileClip(vidin, target_resolution=(720,1280))
    fontsize = 75
    txt_clip = ( TextClip("Download link in the description",
                                        fontsize=fontsize,
                                        font='Proxima-Nova-Bold',
                                        color="white")
                            .set_position(("center", (video.h-200)))
                            .set_duration(video.duration)
                            .set_opacity(.75)
                    )
    result = CompositeVideoClip([video, txt_clip])
    if not os.path.exists("temp"):
        os.makedirs("temp")
    result.write_videofile(vidout, codec='libx264', audio_codec="aac",temp_audiofile="temp/temp.m4a",remove_temp = True)
    return


def fileread():
    try:
        if os.stat("maindata.txt").st_size == 0:
            raise FileNotFoundError("File is empty") 
        main_file = open("maindata.txt", 'r')
        print(GREEN +"  [*] Reading File...")
        data_read = []
        while True:
            linedata = main_file.readline()
            if not linedata:
                break
            recording = False
            data_read = []
            string = ''
            for i in linedata:
                if i == '[' or i == ',' or i == ']':
                    continue
                elif i == '\'':
                    if recording == False:
                        string = ''
                        recording = True
                    else:
                        recording = False
                        data_read.append(string)
                else:
                    string = string + i
            maindata.append(data_read)
        global count
        count = int(data_read[0])
    except FileNotFoundError:
        main_file = open("maindata.txt", 'a')
    main_file.close()
    return

def upload_web(filen,title,keywords,description):
    sleep(2)
    driver.find_element_by_xpath('//a[@test-id="upload-icon-url"]').click()
    sleep(2)
    dropzone = driver.find_element_by_xpath('//div[@class="style-scope ytcp-uploads-file-picker"]')
    dropzone.drop_files(filen)
    sleep(3)
    back="\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b"
    driver.find_element_by_xpath('//div[@aria-label="Add a title that describes your video"]').send_keys(back+title)
    driver.find_element_by_xpath('//div[@aria-label="Tell viewers about your video"]').send_keys(description)
    driver.find_element_by_xpath('//*[@id="still-0"]/button').click()
    driver.find_element_by_xpath('//*[@name="NOT_MADE_FOR_KIDS"]/div[1]').click()
    driver.find_element_by_xpath('//*[text()="More options"]').click()
    driver.find_element_by_xpath('//input[@aria-label="Tags"]').send_keys(keywords)

    while True:
        x_path = '//span[@class="progress-label style-scope ytcp-video-upload-progress"]' 
        if "Finished processing" in driver.find_element_by_xpath(x_path).get_attribute('innerHTML'):
            break
    driver.find_element_by_xpath('//*[@id="next-button"]').click()
    sleep(1)
    driver.find_element_by_xpath('//*[@id="next-button"]').click()
    sleep(1)
    driver.find_element_by_xpath('//*[@name="PUBLIC"]/div[1]').click()
    driver.find_element_by_xpath('//*[@id="done-button"]/div').click()
    while True:
        if hasxpath('//*[@id="close-button"]/div'):
            driver.find_element_by_xpath('//*[@id="close-button"]/div').click()
            break


def upload(data):
    if not is_downloadable(data[2]):
        return False

    print(GREEN +"  [*] Downloading Video ["+str(count)+"]....")
    downvid = "temp/downvid.mp4"
    vidr = requests.get(data[2])
    filev = open(downvid,'wb')
    filev.write(vidr.content)
    filev.close()

    print(GREEN +"  [*] Editing Video....")
    editvid = "temp/editvid.mp4"
    convertvideo(downvid,editvid)

    print(GREEN +"  [*] Generating Upload data...")
    list_link1 = data[1].split('/')[2].split('-')
    short_link720 = shorturl("https://pixabay.com/videos/download/video-"+list_link1[-1]+"_medium.mp4?attachment")
    short_link1080 = shorturl("https://pixabay.com/videos/download/video-"+list_link1[-1]+"_large.mp4?attachment")
    short_linkorg = shorturl("https://pixabay.com/videos/download/video-"+list_link1[-1]+"_source.mp4?attachment")
    vidname = ' '.join(list(map(lambda st:st.capitalize(), list_link1[:-1]))) +" - Copyright Free stock video footage"
    keywords = ', '.join(list(map(lambda st:st.lower(), list_link1[:-1]))) 
    keywords = keywords + "stock, video, free, download, footage, background, copyright, youtube, hd, high, quality, professional"
    description = "Support us by Subscribe and Share\n\nDownload Link:\n      720p:      "
    description = description + short_link720 + "\n      1080p:      " + short_link1080 + "\n      Orginal video:      " + short_linkorg
    description = description +"\n\n\n\nHigh quality royality free stock videos for free download from Pixabay.\nFree for commercial use.\nNo attribution required"

    print(GREEN+"  [*] Uploading data Youtube... " + data[1])
    upload_web(os.path.abspath(editvid),vidname,keywords,description)
    os.system('cls')
    return True


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.found = 0
        self.found1 = 0
        self.found2 = 0
        self.main_file = open("maindata.txt", 'a')
        self.data = []


    def handle_starttag(self, tag, attrs):
        if tag == 'a' and self.found == 1:
            for name, value in attrs:
                if name == 'href':
                    self.data.clear()
                    self.data.append('0')
                    self.data.append(value)
            self.found = 0

        if tag == 'input':
            for name, value in attrs:
                if name=='name' and value == 'pagi':
                    self.found1 = 1
                    break

        if tag != 'div':
            return
        else:
            for name, value in attrs:
                if name == 'itemtype' and value == "schema.org/VideoObject":
                    self.found = 1
                elif name == 'data-mp4':
                    self.data.append("https:"+value)
                    
                    for item in maindata:
                        if item[1] == self.data[1]:
                            self.found2 = 1
                            break

                    if self.found2 == 1:
                        print('-'*80)
                        print(RED+"  Skipping..." + self.data[1])
                        self.found2 = 0
                    else:
                        global count
                        count = count + 1
                        self.data[0] = str(count)
                        print('-'*80)
                        if upload(self.data):
                            self.main_file.write(str(self.data)+'\n')
                            self.main_file.close()
                            self.main_file = open("maindata.txt", 'a')
                            print(GREEN +"  [*] Upload Successfully...")
                        else:
                            print(LRED +"  [*] Error: Broken Link...")


    def handle_data(self, data):
        if self.found1 == 1:
            global length
            length = [int(i) for i in data.split() if i.isdigit()][0]
            self.found1 = 0


if __name__ == "__main__": 

    init(autoreset=True)
    init_web()
    fileread()
    cou = 1
    weblist = ['latest','upcoming','popular','ec']
    scraper = cloudscraper.create_scraper()

    for st in weblist:
        cou = 1
        while cou <= length:
            url = 'https://pixabay.com/videos/search/?order='+st+'&pagi=' + str(cou)
            print (RED +"\n  Page :" + str(cou) + " " +url+"\n")
            res = str(''.join([i if ord(i) < 128 else ' ' for i in scraper.get(url).text]))
            parser = MyHTMLParser()
            parser.feed(res)
            cou = cou+1
    driver.close()


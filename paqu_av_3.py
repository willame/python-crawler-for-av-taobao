# -*- coding: utf-8 -*-

#导入模块
import requests, urllib, urllib2, re
from bs4 import BeautifulSoup

#获取所有视频的url地址和标题title
def get_video_url_and_title():
	page_number = 2   #因为第一页url不一致，故而从第二页开始
	lists = []   #收集所有视频的url地址
	while page_number < 4:  #需要爬取的页码，根据网页修改
	    url = 'http://www.avtb6.com/guochan/recent/' + str(page_number) #获得视频的播放地址
	    headers = {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}
	    request = urllib2.Request(url, headers=headers)
	    response = urllib2.urlopen(request)
	    html_content = BeautifulSoup(response.read())
        #找到每一页面的所有视频
	    videoLists = html_content.find_all("li", {"id":re.compile("video-.*?")})
	    page_number += 1   #页码加1
	    lists.append(videoLists) #把每一页的所有视频地址添加到lists列表中

	return lists  #通过while循环，得到所有页面的视频的地址


#下载视频
def download_video(lists):
    for videoLists in lists: #得到每一页的所有视频的地址           
        previous_video_urls = []   #收集每一页所有视频的播放地址

        for name in videoLists:  #每个视频的所对应的html文件
            #得到每个视频的实际播放地址和标题
            video_url = "http://www.avtb6.com/" + name.select(".thumbnail")[0].attrs["href"]
            video_title = name.select(".thumbnail")[0].attrs["title"]

            #不重复下载，判断此视频url是不是已经存在，若存在，则不下载
            if video_url not in previous_video_urls:
                previous_video_urls.append(video_url) #添加不存在视频的url到列表.
                #轻量头文件，防止反爬虫
                headers = {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}        
                html = requests.get(video_url, headers=headers)   #requests得到网页html
                html.encoding = 'utf-8' #指定网页编码
                html_content = html.text   #得到网页内容，均为Unicode格式

                #正则表达式，找到视频的实际真实下载地址
                pattern = re.compile('<video id=.*?source src="(.*?)"', re.S)  
                content_url = re.findall(pattern, html_content)

                num = 1  #给下载视频编号命名
                for item in content_url:
                    print(u"正在下载: %s" % video_title)
                    #调用urlretrieve下载视频
                    download_video = urllib.urlretrieve(item, '%s.mp4' % num + "." + video_title)
                    num += 1
                    print(u"%s已下载完成" % video_title)


lists = get_video_url_and_title()
videos = download_video(lists)

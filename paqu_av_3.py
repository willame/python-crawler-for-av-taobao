# -*- coding: utf-8 -*-

import requests, urllib, urllib2, re
from bs4 import BeautifulSoup


def get_video_url_and_title():
	page_number = 2
	lists = []
	while page_number < 4:
	    url = 'http://www.avtb6.com/guochan/recent/' + str(page_number)
	    headers = {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}
	    request = urllib2.Request(url, headers=headers)
	    response = urllib2.urlopen(request)
	    html_content = BeautifulSoup(response.read())
	    videoLists = html_content.find_all("li", {"id":re.compile("video-.*?")})
	    page_number += 1
	    lists.append(videoLists)
    			
	return lists


def download_video(lists):
        for videoLists in lists:
                

                previous_video_urls = []

                for name in videoLists:
                        video_url = "http://www.avtb6.com/" + name.select(".thumbnail")[0].attrs["href"]
                        video_title = name.select(".thumbnail")[0].attrs["title"]

                        if video_url not in previous_video_urls:
                                previous_video_urls.append(video_url)
                                headers = {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}        
                                html = requests.get(video_url, headers=headers)
                                html.encoding = 'utf-8'
                                html_content = html.text

                                pattern = re.compile('<video id=.*?source src="(.*?)"', re.S)
                                content_url = re.findall(pattern, html_content)

                                num = 1
                                for item in content_url:
                                        print(u"正在下载: %s" % video_title)
                                        # download_video = urllib.urlretrieve(item, '%s.mp4' % num + "." + video_title)
                                        # num += 1
                                        # print(u"%s已下载完成" % video_title)


lists = get_video_url_and_title()

videos = download_video(lists)

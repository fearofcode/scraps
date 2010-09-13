import urllib
import xml.dom.minidom
import logging
import sys
from datetime import datetime

class Video(object):
    def __init__(self, title, published, viewCount, url):
        self.title = title

        if type(published) == type(u"") or type(published) == type(""):
            self.published = datetime.strptime(published, "%Y-%m-%dT%H:%M:%S.000Z") # assume iso 8601 format
        else:
            self.published = published

        self.viewCount = viewCount
        self.url = url

    def __repr__(self):
        return "<Video object %s>" % dict(title=self.title, published=self.published, 
                                          viewCount=self.viewCount, url=self.url, rank=self.rank())

    def rank(self):
        "Compute how hot a video is. Borrowed from Hacker News' ranking formula."
        daysOld = (datetime.today()-self.published).days

        return (self.viewCount - 1.)/(daysOld+2.)**1.5

    @classmethod
    def rankVideos(self, videoList):
        return sorted(videoList, key=lambda video: video.rank(), reverse=True)

class VideoFeedRetriever(object):
    @classmethod
    def fetchAndParseFeed(self, url):
        logging.debug("Attempting to retrieve %s" % url)

        try:
            retrievedText = urllib.urlopen(url).read()
            return xml.dom.minidom.parseString(retrievedText)
        except:
            logging.error("Network error. Please make sure you supplied a valid channel/playlist.")
            sys.exit(-1)

    @classmethod
    def parseVideoEntriesFromFeed(self, parsed):
        entries = parsed.getElementsByTagName("entry")

        videos = []

        for entry in entries:
            title = entry.getElementsByTagName("title")[0].childNodes[0].data
            published = entry.getElementsByTagName("published")[0].childNodes[0].data
            viewCount = int(entry.getElementsByTagName("yt:statistics")[0].getAttribute("viewCount"))
            url = [elem for elem in entry.getElementsByTagName("link") 
                   if elem.hasAttribute("rel") and elem.getAttribute("rel") == "alternate"][0].getAttribute("href")
            videos.append(Video(title, published, viewCount, url))


        return videos

    @classmethod
    def getAllEntriesFromChannel(self, username):
        startIndex = 1
        maxResults = 50

        videos = []

        logging.info("Fetching feed information from user %s" % username)

        while True:
            url = "http://gdata.youtube.com/feeds/api/users/%s/uploads?start-index=%d&max-results=%d" % (username, startIndex, maxResults)

            feed = self.fetchAndParseFeed(url)

            videos.extend(self.parseVideoEntriesFromFeed(feed))

            hasNextLink = [elem for elem in feed.getElementsByTagName("link") if 
                           elem.hasAttribute("rel") and elem.getAttribute("rel") == "next"]

            if len(hasNextLink) == 0:
                break

            startIndex += maxResults

        return videos

    @classmethod
    def getRankedEntriesFromChannel(self, username):
        return Video.rankVideos(self.getAllEntriesFromChannel(username))

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    videos = VideoFeedRetriever.getRankedEntriesFromChannel("thunderdome94")

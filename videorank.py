import urllib
import xml.dom.minidom
import logging
import sys

class Video(object):
    def __init__(self, title, published, viewCount, url):
        self.title = title
        self.published = published
        self.viewCount = viewCount
        self.url = url

    def __repr__(self):
        return "<Video object %s>" % dict(title=self.title, published=self.published, 
                                          viewCount=self.viewCount, url=self.url)

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
            try:
                title = entry.getElementsByTagName("title")[0].childNodes[0].data
                published = entry.getElementsByTagName("published")[0].childNodes[0].data
                viewCount = int(entry.getElementsByTagName("yt:statistics")[0].getAttribute("viewCount"))
                url = [elem for elem in entry.getElementsByTagName("link") 
                       if elem.hasAttribute("rel") and elem.getAttribute("rel") == "alternate"][0].getAttribute("href")
                videos.append(Video(title, published, viewCount, url))
            except:
                logging.error("Something went wrong with the XML feed.")
                sys.exit(-1)

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

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    videos = Video.getAllEntriesFromChannel("haveadot")

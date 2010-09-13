import urllib
import xml.dom.minidom

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
    def parseVideoEntriesFromFeed(self, url):
        retrievedText = urllib.urlopen(url).read()

        parsed = xml.dom.minidom.parseString(retrievedText)
    
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




if __name__ == "__main__":
    # sample feed from a channel with many videos that have been uploaded over the course of a couple years
    sampleUrl = "http://gdata.youtube.com/feeds/api/users/thunderdome94/uploads?start-index=1&max-results=25"

    videos = Video.parseVideoEntriesFromFeed(sampleUrl)

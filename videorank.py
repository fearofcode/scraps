import urllib
import xml.dom.minidom

if __name__ == "__main__":
    sampleUrl = "http://gdata.youtube.com/feeds/api/users/thunderdome94/uploads?start-index=1&max-results=25"

    retrievedText = urllib.urlopen(sampleUrl).read()

    parsed = xml.dom.minidom.parseString(retrievedText)
    
    entries = parsed.getElementsByTagName("entry")

    for entry in entries:
        title = entry.getElementsByTagName("title")[0].childNodes[0].data
        print title

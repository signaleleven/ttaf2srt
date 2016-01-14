#!/usr/bin/env python3

"""
Usage:
ttaf2srt subtitlefilettafinput.xml > output.srt

From https://github.com/haraldF/ttaf2srt
edited for 'SWR - Pälzisch im Abgang' subtitles
www.swr.de/paelzisch-im-abgang/
and 'Tatort' subtitles.
"""
"""
From https://github.com/haraldF/ttaf2srt

ttaf2srt

Simple python script to convert ttaf subtitles to srt subtitles.
Note - only tested on German 'Tatort' subtitles.
Note2 - if using vlc or mplayer, make sure to specify 'utf8' as encoding, otherwise, special characters will not render correctly.
"""
import sys
import datetime
from xml.dom import minidom

def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

def dumpText(item):
    for child in item.childNodes:
        if child.nodeType == child.TEXT_NODE:
            print(child.nodeValue, end="")
        elif child.nodeType == child.ELEMENT_NODE:
            if child.nodeName == "br":
                print()
            elif child.nodeName == "span":
                dumpText(child)
            else:
                print("Unknown Node: " + child.nodeName, file=sys.stderr)

def dumpHeader(item, subCount):
    print(subCount)
    begin = item.getAttribute("begin")
    end = item.getAttribute("end")
    # ### this is a silly hack - for some reason, my ttaf files all start at hour 10? Resetting
    # the hour makes it work again
    #begin = '0' + begin[1:]
    #end = '0' + end[1:]
    tbegin=datetime.timedelta(seconds=float(begin))
    tend=datetime.timedelta(seconds=float(end))
    subsecb=int(str(float(begin) % 1)[2:5])
    subsece=int(str(float(end) % 1)[2:5])
    print("%.2d:%.2d:%.2d,%.3d --> %.2d:%.2d:%.2d,%.3d" % (tbegin.seconds//3600,(tbegin.seconds//60)%60,tbegin.seconds%60,subsecb,tend.seconds//3600,(tend.seconds//60)%60,tend.seconds%60,subsece))
    #print(begin + " --> "+ end)

def parseStyles(styles):
    result = {}
    for style in styles:
        result[style.getAttribute('xml:id')] = style.getAttribute('color')
    return result

with open(sys.argv[1]) as f:
    xmldoc = f.read().replace('\n', ' ').replace('\r', '')
xmldoc = minidom.parseString(xmldoc)

header = xmldoc.getElementsByTagName('head')
if len(header):
    styling = header[0].getElementsByTagName('styling')
    if len(styling):
        styles = parseStyles(styling[0].getElementsByTagName('style'))

body = xmldoc.getElementsByTagName('body')

itemlist = body[0].getElementsByTagName('p') 

subCount = 1

for item in itemlist:
        dumpHeader(item, subCount)
        subCount += 1
        color = item.getAttribute("tts:style")
        dumpText(item)
        print("\n")

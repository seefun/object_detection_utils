import os
import xml.dom.minidom
from xml.dom.minidom import Document

doc = Document()

# creat root 
images = doc.createElement('images')
# creat dom tree
doc.appendChild(images)


def writeInfoToXml(filename, info):
    image = doc.createElement('image')
    image.setAttribute('file',filename)
    #image.attrib = {'file':filename}
    images.appendChild(image)

    for xyxy in info:	
        box = doc.createElement('box')
        x = int(xyxy[0])
        y = int(xyxy[1])
        w = int(xyxy[2]) - x
        h = int(xyxy[3]) - y
        box.setAttribute('top',str(y))
        box.setAttribute('left',str(x))
        box.setAttribute('width',str(w))
        box.setAttribute('height',str(h))
        #box.attrib = {'top':str(x),'left':str(y),'width':str(w),'height':str(h)}
        image.appendChild(box)
        


with open('anno_all.txt') as label:
    line = label.readline()
    while line:
        suffix = '.' + line.split()[0].split('/')[-1].split('.')[-1]
        filename = line.split()[0].split('/')[-1].split(suffix)[0] + '.jpg'
        info = []
        info.append(line.split()[1:5])
        line = label.readline()
        while line and ((line.split()[0].split('/')[-1].split(suffix)[0] + '.jpg') == filename):
            info.append(line.split()[1:5])
            line = label.readline()
        writeInfoToXml(filename, info)

    with open('output.xml', 'wb') as f:
        f.write(doc.toprettyxml(indent='\t', encoding='utf-8'))

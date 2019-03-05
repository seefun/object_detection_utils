# convert txt file to pascal voc format
# "image_name.jpg x1 y1 x2 y2" (each line in input txt file)
# for single type object annotation

import os
from xml.dom.minidom import Document
import cv2

IMG_FOLDER = 'Images'        # images folder
XML_FOLDER = 'Annotations/'  # output folder
INPUT_TXT = 'anno.txt'       # input txt file
#foldername = 'data'
object_name = 'face'         # object name (eg. person, face, car ...)

def writeInfoToXml(filename, info):
    img_name = 'JPEGImages/' + filename
    img_read = cv2.imread(img_name)
    try:
        h = img_read.shape[0]
        w = img_read.shape[1]
    except: # img not exist
        return

    # creat dom document
    doc = Document()

    # creat root node
    annotation = doc.createElement('annotation')
    # creat dom tree
    doc.appendChild(annotation)

    folder = doc.createElement('folder')
    folder_text = doc.createTextNode(IMG_FOLDER)
    folder.appendChild(folder_text)
    annotation.appendChild(folder)
	
    file_name = doc.createElement('filename')
    file_name_text = doc.createTextNode(filename)
    file_name.appendChild(file_name_text)
    annotation.appendChild(file_name)
    
    size = doc.createElement('size')
    width = doc.createElement('width')
    width_text = doc.createTextNode(str(w))
    width.appendChild(width_text)
    size.appendChild(width)
    height = doc.createElement('height')
    height_text = doc.createTextNode(str(h))
    height.appendChild(height_text)
    size.appendChild(height)
    depth = doc.createElement('depth')
    depth_text = doc.createTextNode('3')
    depth.appendChild(depth_text)
    size.appendChild(depth)
    annotation.appendChild(size)

    for xyxy in info:	
        object = doc.createElement('object')
        bndbox = doc.createElement('bndbox')
        xmin = doc.createElement('xmin')
        xmin_text = doc.createTextNode(xyxy[0])
        xmin.appendChild(xmin_text)
        bndbox.appendChild(xmin)
        ymin = doc.createElement('ymin')
        ymin_text = doc.createTextNode(xyxy[1])
        ymin.appendChild(ymin_text)
        bndbox.appendChild(ymin)
        xmax = doc.createElement('xmax')
        xmax_text = doc.createTextNode(xyxy[2])
        xmax.appendChild(xmax_text)
        bndbox.appendChild(xmax)
        ymax = doc.createElement('ymax')
        ymax_text = doc.createTextNode(xyxy[3])
        ymax.appendChild(ymax_text)
        bndbox.appendChild(ymax)
        name = doc.createElement('name')
        name_text = doc.createTextNode(object_name)
        name.appendChild(name_text)
        difficult = doc.createElement('difficult')
        difficult_text = doc.createTextNode('0')
        difficult.appendChild(difficult_text)
        object.appendChild(name)
        object.appendChild(difficult)
        object.appendChild(bndbox)
        
        annotation.appendChild(object)
	
    # write xml files
    xml_name = os.path.join(XML_FOLDER, filename.split('.')[0] + '.xml')
    print (xml_name)
    with open(xml_name, 'wb') as f:
        f.write(doc.toprettyxml(indent='\t', encoding='utf-8'))


with open(INPUT_TXT) as label:
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
        

# convert pascal voc format annotation files to txt file 
# "image_name.jpg x1 y1 x2 y2" (each line in output txt file)
# for single type object annotation

import os
import xml.dom.minidom

VOC_XML_FOLDER = 'Annotations'
OUTPUT_FILE = 'annotation.txt'
MIN_BBOX_SIZE = 20

f = open(OUTPUT_FILE, 'w')
anno_dir = VOC_XML_FOLDER
images = os.listdir(anno_dir)

for name in images:
    if name.split('.')[-1]!='xml':
        continue
    name = name.split('.xml')[0]
    dom = xml.dom.minidom.parse(anno_dir + '/' + name + '.xml')
    root = dom.documentElement
    heads = root.getElementsByTagName('object')
    filename = root.getElementsByTagName('filename')[0].childNodes[0].data
    size = root.getElementsByTagName('size')[0]
    w = eval(size.getElementsByTagName('width')[0].childNodes[0].data)
    h = eval(size.getElementsByTagName('height')[0].childNodes[0].data)
    for head in heads:
        bbox = head.getElementsByTagName('bndbox')[0]
        xmin = bbox.getElementsByTagName('xmin')[0]
        ymin = bbox.getElementsByTagName('ymin')[0]
        xmax = bbox.getElementsByTagName('xmax')[0]
        ymax = bbox.getElementsByTagName('ymax')[0]
        xmin = max(eval(xmin.childNodes[0].data),1)
        ymin = max(eval(ymin.childNodes[0].data),1)
        xmax = min(eval(xmax.childNodes[0].data),w-1)
        ymax = min(eval(ymax.childNodes[0].data),h-1)
        if (xmax-xmin >= MIN_BBOX_SIZE): 
            f.write(filename + ' ' + str(xmin) + ' ' + str(ymin) + ' ' + str(xmax) + ' ' + str(ymax) + '\n')

f.close()

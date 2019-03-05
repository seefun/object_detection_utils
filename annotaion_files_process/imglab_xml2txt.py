# convert imglab (a dlib tool) annotation files to txt file 
# "image_name.jpg x1 y1 x2 y2" (each line in output txt file)
# for single type object annotation

import xml.dom.minidom

INPUT_FILE_NAME = 'imglab_anno.xml'
OUTPUT_FILE_NAME = 'output.txt'
MIN_BBOX_SIZE = 20

f = open(OUTPUT_FILE_NAME, 'w')

dom = xml.dom.minidom.parse(INPUT_FILE_NAME)
root = dom.documentElement

images = root.getElementsByTagName('images')[0]
for image in images.getElementsByTagName('image'):
    filename = image.getAttribute('file')
    filename = filename.split('/')[-1]
    for box in image.getElementsByTagName('box'):
        top = eval(box.getAttribute('top'))
        left = eval(box.getAttribute('left'))
        width = eval(box.getAttribute('width'))
        height = eval(box.getAttribute('height'))
        if width < MIN_BBOX_SIZE:
            continue
        x1 = left
        y1 = top
        x2 = x1 + width
        y2 = y1 + height
        f.write(filename + ' ' + str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2) + '\n')
        print(filename)
               
f.close()

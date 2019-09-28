# https://github.com/JialianW/pascal2coco/blob/master/pascal2coco.py

import json
import xml.etree.ElementTree as ET
import os

def load_load_image_labels(LABEL_PATH, class_name=[]):
    # temp=[]
    images=[]
    type="instances"
    annotations=[]
    #assign your categories which contain the classname and calss id
    #the order must be same as the class_nmae
    categories = [
		{
			"id" : 1,
			"name" : "xxx",
			"supercategory" : "none"
		},
        {
            "id": 2,
            "name": "xxx",
            "supercategory": "none"
        },
	]
    # load ground-truth from xml annotations
    id_number=0
    for image_id, label_file_name in enumerate(os.listdir(LABEL_PATH)):
        print(str(image_id)+' '+label_file_name)
        label_file=LABEL_PATH + label_file_name
        image_file = label_file_name.split('.')[0] + '.jpg'
        tree = ET.parse(label_file)
        root = tree.getroot()

        size=root.find('size')
        width = float(size.find('width').text)
        height = float(size.find('height').text)

        images.append({
            "file_name": image_file,
			"height": height,
			"width": width,
			"id": image_id
		})# id of the image. referenced in the annotation "image_id"

        for anno_id, obj in enumerate(root.iter('object')):
            name = obj.find('name').text
            bbox=obj.find('bndbox')
            cls_id = class_name.index(name)
            xmin = float(bbox.find('xmin').text)
            ymin = float(bbox.find('ymin').text)
            xmax = float(bbox.find('xmax').text)
            ymax = float(bbox.find('ymax').text)
            xlen = xmax-xmin
            ylen = ymax-ymin
            annotations.append({
                                "segmentation" : [[xmin, ymin, xmin, ymax, xmax, ymax, xmax, ymin],],
                                "area" : xlen*ylen,
                                "iscrowd": 0,
                                "image_id": image_id,
                                "bbox" : [xmin, ymin, xlen, ylen],
                                "category_id": cls_id,
                                "id": id_number,
                                "ignore":0
                                })
            # print([image_file,image_id, cls_id, xmin, ymin, xlen, ylen])
            id_number += 1

    return {"images":images,"annotations":annotations,"categories":categories}

if __name__=='__main__':
    LABEL_PATH='your pascal voc annotation path'
    classes=['background','add your class name']

    label_dict = load_load_image_labels(LABEL_PATH,classes)
    jsonfile='/home/xxx/train.json'#location where you would like to save the coco format annotations
    with open('/home/wjl/DataSet/707dataset/label/train.json','w') as json_file:
        json_file.write(json.dumps(label_dict, ensure_ascii=False))
        json_file.close()

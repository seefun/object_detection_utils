import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import seaborn as sns
from tqdm import tqdm

def read_bbox_txt(file):
    '''
    read bbox annotation .txt file : eg. "filename x1 y1 x2 y2\n"
    :param file: path to ground truth annotation
    :return: a dictionary {img_name:[[x1, y1, x2, y2],[x1_, y1_, x2_, y2_], ......]}
    '''
    anno_dict = defaultdict()
    with open(file, 'r') as label:
        line = label.readline()
        while line and line.strip()!='':
            filename = line.split()[0]
            anno = []
            line_split = line.split()
            for i in range((len(line_split)-1)//4):
                anno.append(line_split[i*4+1:i*4+5])
            line = label.readline()
            while line and line.strip()!='' and (line.split()[0] == filename):
                line_split = line.split()
                for i in range((len(line_split) - 1) // 4):
                    anno.append(line_split[i * 4 + 1:i * 4 + 5])
                line = label.readline()
            anno_dict[filename] = anno

    return anno_dict

# def read_bbox_txt_split_folder_and_suffix(file, type='png'):
#     '''
#     read bbox annotation .txt file : eg. "filename x1 y1 x2 y2\n"
#     :param file: path to ground truth annotation
#     :param type: imgs type (eg: jpg , png)
#     :return: a dictionary {img_name:[[x1, y1, x2, y2],[x1_, y1_, x2_, y2_], ......]}
#     '''
#     anno_dict = defaultdict()
#     with open(file, 'r') as label:
#         line = label.readline()
#         while line:
#             filename = line.split()[0].split('/')[-1].split('.')[0] + '.' + type
#             anno = []
#             anno.append(line.split()[1:5])
#             line = label.readline()
#             while line and ((line.split()[0].split('/')[-1].split('.')[0] + '.' + type) == filename):
#                 anno.append(line.split()[1:5])
#                 line = label.readline()
#             anno_dict[filename] = anno
#
#     return anno_dict

def IoU(bbox_predict: list, bbox_label: list, type = 'xyxy'):
    '''
    calculate IoU of two box
    :param bbox_predict: predict result box [num1,num2,num3,num4]
    :param bbox_label: ground truth box [num1,num2,num3,num4]
    :param type: annotation type :'xyxy' or 'xywh'
    :return: IoU ratio
    '''
    x1 = int(bbox_predict[0])
    y1 = int(bbox_predict[1])
    if type=='xyxy':
        width1 = int(bbox_predict[2]) - x1
        height1 = int(bbox_predict[3]) - y1
    elif type=='xywh':
        width1 = int(bbox_predict[2])
        height1 = int(bbox_predict[3])
    else:
        print('Error! IoU calculate:annotation type error')
        width1 = int(bbox_predict[2]) - x1
        height1 = int(bbox_predict[3]) - y1

    x2 = int(bbox_label[0])
    y2 = int(bbox_label[1])
    width2 = int(bbox_label[2]) - x2
    height2 = int(bbox_label[3]) - y2

    endx = max(x1 + width1, x2 + width2)
    startx = min(x1, x2)
    width = width1 + width2 - (endx - startx)

    endy = max(y1 + height1, y2 + height2)
    starty = min(y1, y2)
    height = height1 + height2 - (endy - starty)

    if width <= 0 or height <= 0:
        ratio = 0
    else:
        Area = width * height
        Area1 = width1 * height1
        Area2 = width2 * height2
        ratio = Area * 1. / (Area1 + Area2 - Area)
    # return IOU
    return ratio


def precision_recall(predict_list, truth_list, IoU_thre):
    '''
    calculate number of true posible, false posible and false negative
    :param predict_list: a list of prediction bbox  eg. [[x1, y1, x2, y2], [x1_, y1_, x2_, y2_], ......]
    :param truth_list: a list of ground truth anno  eg. [[x1, y1, x2, y2], [x1_, y1_, x2_, y2_], ......]
    :param IoU_thre: IoU threshold
    :return: (true posible, false posible, false negative)
    '''
    tp = 0
    fp = 0
    fn = 0
    is_recall_truth_list = [False] * len(truth_list)
    for positive in predict_list:
        is_find = False
        for k, truth in enumerate(truth_list):
            if  IoU(positive,truth) > IoU_thre:
                is_find = True
                is_recall_truth_list[k] = True
                break
        if is_find:
            tp += 1
        else:
            fp += 1

    for is_recall in is_recall_truth_list:
        if not is_recall:
            fn += 1

    return (tp, fp, fn)


def detection(anno_path, detection_result_txt, thre_list, IoU_thre = 0.5):
    '''
    detection all images and return the all number of true posible, false posible and false negative in each level of thre
    :param anno_path: path of ground truth anno txt file
    :param detection_result_txt: path of detection results file
    :param thre_list: several detection threshold level
    :param IoU_thre: IoU threshold
    :return: a list [[tp,fp,fn], ...] in different detection threshold level
    '''
    anno_dict = read_bbox_txt(anno_path)
    
    pbar = tqdm(total=len(anno_dict))
    count = 0
    
    result_list = []
    for i in range(len(thre_list)):
        result_list.append([0,0,0]) # [tp,fp,fn]

    det_txt = open(detection_result_txt, 'r')

    line = det_txt.readline()

    while line and line.strip():
        img_name = line.strip()
        num_detections = int(det_txt.readline().strip())
        det_result = []
        for i in range(num_detections):
            line = det_txt.readline().split()
            det_result.append(line)
                
        for k, thre in enumerate(thre_list):
            predict_list = []
            for det in det_result:
                score = float(det[4])
                if score > thre:  ### threshould
                    x = float(det[0])
                    y = float(det[1])
                    right = float(det[2])
                    bottom = float(det[3])
                    predict_list.append([x,y,right,bottom])

            detection_result = precision_recall(predict_list,anno_dict[img_name],IoU_thre)
            tp = detection_result[0]
            fp = detection_result[1]
            fn = detection_result[2]
            result_list[k][0] += tp
            result_list[k][1] += fp
            result_list[k][2] += fn
            
        line = det_txt.readline()
        count += 1
        if count%10 == 0:
            pbar.update(10)
            #print('number:%d , finish:%.3f'%(count ,count/len(imgs)))
    return result_list


def main():
    # ------ change this param ---------
    ANNO_PATH = 'anno.txt'
    DETECTION_RESULT = 'result.txt'
    thre_list = list(np.arange(0.0001,1.0001,0.01))
    IoU_thre = 0.5
    # ----------------------------------
    result_list = detection(ANNO_PATH, DETECTION_RESULT, thre_list, IoU_thre)
    precision_list = []
    recall_list = []
    result_txt = open('eval_result.txt', 'w')
    print('[[[ IoU threshold is %.2f ]]]'%IoU_thre)
    result_txt.write('[[[ IoU threshold is %.2f ]]] \n'%IoU_thre)
    for i in range(len(thre_list)):
        thre = thre_list[i]
        tp = result_list[i][0]
        fp = result_list[i][1]
        fn = result_list[i][2]
        precision = (tp + 0.00001) / (tp + fp + 0.00001)
        recall =  (tp) / (tp + fn + 0.00001)
        precision_list.append(precision)
        recall_list.append(recall)
        print("[]Threshold:%.3f  Precision:%.3f  Recall:%.3f"%(thre,precision,recall))
        result_txt.write("[]Threshold:%.3f  Precision:%.3f  Recall:%.3f \n"%(thre,precision,recall))

    AP = precision_list[0] * (1-recall_list[0]) * 0.5
    precision_list.append(1.0)
    recall_list.append(0.0)
    for i in range(len(precision_list)-1):
        h = (precision_list[i+1] + precision_list[i]) / 2
        w = recall_list[i] - recall_list[i+1]
        AP = AP + h * w
    print('[AP]:%.5f'%AP)
    result_txt.write('[AP]:%.5f \n'%AP)
    result_txt.close()

    ## draw the P-R curve
    sns.set()
    plt.title('P-R curve')  
    plt.xlabel('Recall')  
    plt.ylabel('Precision')  
    plt.plot(recall_list[:-1:5], precision_list[:-1:5])
    #plt.plot(recall_list[:-1], precision_list[:-1])
    plt.savefig("PR_curve.png") 
    plt.show()
    

if __name__ == '__main__':
    main()
    
# TODO: add flip image and annotation eval;
# TODO: add TTA(test time augmentation)

import numpy as np 
import cv2
import json 
import datetime
import threading
import sched, time 
import collections


#global variables
w = 1280
h= 720


class getDetectionBot(object):

    def genSimRes(self):
        bo = [np.random.rand(1)[0]/20 for _ in range(4)]
        box = [(0.21+bo[1])*w, (0.26+bo[3])*w, (0.59+bo[0])*h, (0.73+bo[2])*h]
        res={}
        res["label"] = "Standing person"
        res["box"] = box
        res["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return res 



    def genRes(self):
        bo = [np.random.rand(1)[0] for _ in range(4)]
        box = [bo[1]*w, bo[3]*w, bo[0]*h, bo[2]*h]
        res={}
        res["label"] = "Standing person"
        res["box"] = box
        res["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return res 

    def getIOU(self, bbox1, bbox2):
    
        bbox1 = [float(x) for x in bbox1]
        bbox2 = [float(x) for x in bbox2]

        (x0_1, x1_1, y0_1, y1_1) = bbox1
        (x0_2, x1_2, y0_2, y1_2) = bbox2

        overlap_x0 = max(x0_1, x0_2)
        overlap_y0 = max(y0_1, y0_2)
        overlap_x1 = min(x1_1, x1_2)
        overlap_y1 = min(y1_1, y1_2)

        if overlap_x1 - overlap_x0 <= 0 or overlap_y1 - overlap_y0 <= 0:
            return 0

        size_1 = (x1_1 - x0_1) * (y1_1 - y0_1)
        size_2 = (x1_2 - x0_2) * (y1_2 - y0_2)
        size_intersection = (overlap_x1 - overlap_x0) * (overlap_y1 - overlap_y0)
        size_union = size_1 + size_2 - size_intersection

        return size_intersection / size_union 
    
    def filt(self, res,num):
        boxes = []
        output = dict(res)
        if num == 1:
            return output
        for k in range(num):
            boxes.append(res[str(k)]["box"])
        for i in range(num-1):
            for j in range(i+1,num):
                iou = self.getIOU(boxes[i],boxes[j])
                if iou > 0.3:
                    if str(j) in output:
                        del output[str(j)]
        return output

    def getDetections(self,jsonFileName):
        while True:
            num = np.random.randint(0,8)
            output = {}
            for i in range(num):
                res = self.genSimRes()
                output[str(i)] = res
            result_boxes =self.filt(output,num)
            with open(jsonFileName,'w') as f:
                json.dump(result_boxes,f)
            time.sleep(1)
           # detection_result = self.parseResult(jsonFileName)
           # print(detection_result)
           # print("detection_result count is {}".format(len(detection_result)))

    def getDetectionLocal(self):
        while True:
            num = np.random.randint(0,3)
            output = {}
            for i in range(num):
                res = self.genSimRes()
                output[str(i)] = res
            result_boxes =self.filt(output,num)
            time.sleep(1)
            return result_boxes 

        
    def parseResult(self,resultJson):
        with open(resultJson) as json_file:
            result = json.load(json_file)
        return result

if __name__ == "__main__":
    jsonFileName = 'detectionResult.json'
    bot = getDetectionBot()
    bot.getDetections(jsonFileName)

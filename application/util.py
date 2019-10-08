def getIOU(bbox1, bbox2):

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

def filt(res,num):
    boxes = []
    output = dict(res)
    if num == 1:
        return output
    for k in range(num):
        boxes.append(res[str(k)]["box"])
    for i in range(num-1):
        for j in range(i+1,num):
            iou = getIOU(boxes[i],boxes[j])
            if iou > 0.3:
                if str(j) in output:
                    del output[str(j)]
    return output



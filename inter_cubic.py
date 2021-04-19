import os
import cv2

imgs = os.listdir("/media/jhonatan/Data/h6f86gl(2)/final/X4/lr_test")

for img in imgs:
    i = cv2.imread("/media/jhonatan/Data/h6f86gl(2)/final/X4/lr_test/"+img)
    i = cv2.resize(i, (1920,1080), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite("/media/jhonatan/Data/h6f86gl(2)/final/X4/sr_test/inter_cubic/"+img, i)
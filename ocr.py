import pandas as pd 
import cv2
import pytesseract
from Levenshtein import distance as levenshtein_distance

df = pd.read_csv("/media/jhonatan/Data/h6f86gl(2)/final/test.csv")
# df = pd.read_csv("test_dist.csv")

img_paths = ["/media/jhonatan/Data/h6f86gl(2)/final/X4/sr_test/lr_test/rdn-C6-D20-G64-G064-x4/2020-10-18_2239/", "/media/jhonatan/Data/h6f86gl(2)/final/X4/sr_test/lr_test/rrdn-C4-D3-G64-G064-T10-x4/2020-10-15_2308/", "/media/jhonatan/Data/h6f86gl(2)/final/X4/lr_test/"]
# img_paths = ["/media/jhonatan/Data/h6f86gl(2)/final/X4/lr_test/"]
for img_path in img_paths:
    ocr = []
    bin_ocr = []
    for index, row in df.iterrows():
        if index > 200: break
        
        img = cv2.imread(img_path + str(row.img_id).zfill(5)+'.png')
        # if img_path.split('/')[-2] == 'lr_test':
        #     img = cv2.resize(img, (1920,1080), interpolation=cv2.INTER_CUBIC)
        x0 = int(float(row.x0)*img.shape[1])
        x1 = int(float(row.x1)*img.shape[1])
        y0 = int(float(row.y0)*img.shape[0])
        y1 = int(float(row.y1)*img.shape[0])
        roi = img[y0:y1, x0:x1]
        write_path = ''
        if img_path.split('/')[-2] == 'lr_test':
            write_path = 'out_bicubic/'
            cv2.imwrite('out_original/'+ str(row.img_id).zfill(5)+'.png', roi)
            roi = cv2.resize(roi, (4*roi.shape[1], 4*roi.shape[0]), interpolation=cv2.INTER_CUBIC)
        elif img_path.split('/')[-2] == '2020-10-18_2239':
            write_path = 'out_srgan/'
        else:
            write_path = 'out_esrgan/' 
        
        cv2.imwrite(write_path+ str(row.img_id).zfill(5)+'.png', roi)
        
        roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        ret, roi_gray = cv2.threshold(roi_gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        # cv2.imshow('roi', roi)
        # cv2.waitKey(-1)
        config = ("-l eng")
        out =' pytesseract.image_to_string(roi_gray, config=config)'
        out2 = 'pytesseract.image_to_string(roi, config=config)'
        # print(row.img_id)
        # print(out)
        bin_ocr.append(out)
        ocr.append(out2)
        
        
    # df[img_path.split('/')[-2]] = ocr
    # df[img_path.split('/')[-2]+"_bin"] = bin_ocr
    
    # print(df.head())
# df.to_csv('test_otsu.csv')

keys = ['2020-10-18_2239', '2020-10-18_2239_bin', '2020-10-15_2308', '2020-10-15_2308_bin','lr_test', 'lr_test_bin']
# keys = ['lr_test', 'lr_test_bin']

# for key in keys:
#     out = []
#     for index, row in df.iterrows():
#         l = row[key].split('\n')
#         longest_string = max(l, key=len)
#         out.append(''.join(e for e in longest_string if e.isalnum()))
#     df[key] = out
        
# # df.to_csv('test_alnum.csv')


    
# for key in keys:
#     out = []
#     for index, row in df.iterrows():
#         dist = levenshtein_distance(str(row[key]), str(row['text']))
#         out.append(dist)
#     df[key+'_dist'] = out

# df.to_csv('final_eng.csv')

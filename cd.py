
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt 
import os
import os.path
from PIL import Image
import glob

OUTPUT_FOLDER = "Output"
CAPTCHA_IMAGE_FOLDER = "samples"


# Get a list of all the captcha images we need to process
captcha_image_files = glob.glob(os.path.join(CAPTCHA_IMAGE_FOLDER, "*"))
counts = {}
a=1;
# loop over the image paths
for (i, captcha_image_file) in enumerate(captcha_image_files):
    print("[INFO] processing image {}/{}".format(i + 1, len(captcha_image_files)))
    
    img_i= cv.imread(captcha_image_file).astype('uint8');
    img = cv.cvtColor(img_i, cv.COLOR_BGR2GRAY);
    plt.imshow(img,'gray'); 
    ret,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY);
    th2 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C,
                               cv.THRESH_BINARY,11,2);
    ret2,th3 = cv.threshold(img,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU);
    blur = cv.GaussianBlur(img,(5,5),0)
    ret3,th4 = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)   
    kernel = np.ones((2,2), np.uint8); 
    img_di = cv.dilate(th4, kernel, iterations=1); 
    img_d = cv.dilate(img_di, kernel, iterations=1); 
    img_er = cv.erode(img_d, kernel, iterations=1); 
    titles = ['gray Image','global',
              'Adaptive Mean','simple otsu','gaussian otsu','dilate','second dilate', 'erode']
    images = [img, th1, th2, th3, th4, img_di, img_d, img_er]
    for i in range(8):
        plt.subplot(3,3,i+1),plt.imshow(images[i],'gray')
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])
    plt.show()
        
    head,tail = os.path.split(captcha_image_file);    
    x, y, w, h=25, 12, 25, 38
    
    for j in range(5):
        cv.rectangle(img_er, (x, y), (x + w, y + h), (0, 255, 0), 2)
        var=tail[j];
        print (var);
        crp_img=img_er[y-2:y+h+2, x-2:x+w+2];
        name= os.path.join('G:/Project/Captcha Detection/output/',var+str(a)+".png")
        cv.imwrite(name,crp_img)
        x =x + w;
    a=a+1;
    
               
  




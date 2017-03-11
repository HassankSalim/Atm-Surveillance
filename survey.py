import cv2
from label_image import classify
import numpy as np
import sys

cap = cv2.VideoCapture(sys.argv[1])

_, calibrated_img = cap.read() 
gray_calibrated_img = cv2.cvtColor(calibrated_img, cv2.COLOR_BGR2GRAY)
row, col = gray_calibrated_img.shape
pixel_count = row * col 
cv2.imshow('img_check', calibrated_img)

flag = ""
color = (0, 0, 0)

while cap.isOpened():
	
	ret, img = cap.read()
	gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	
	diff = gray_img - gray_calibrated_img
	non_zero_count = np.count_nonzero(diff)
	
	if non_zero_count > pixel_count * 0.75:
		print non_zero_count
		cv2.imwrite('temp.jpg', img)
		temp = classify('temp.jpg')
		flag = temp['string']
		print temp['string'], '  ', temp["confidence"]
		if flag == 'illegal':
			color = (0, 0, 225)
		else:
			color = (0, 255, 0)
	
	cv2.putText(img, flag, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color)	
	cv2.imshow('video_check', img)
	
	gray_calibrated_img = gray_img
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()		


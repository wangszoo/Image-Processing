import cv2
import numpy as np 
import matplotlib.pyplot as plt

def rotsImg(image, angle, scale):
	"""旋转缩放图像"""

	height = image.shape[0]
	width = image.shape[1]

	matRot = cv2.getRotationMatrix2D((height*0.5, width*0.5), angle, scale)
	# 中心，角度，缩放系数

	I_rot = cv2.warpAffine(image, matRot, (width, height))

	return I_rot

def SIFT_CV(image):
	"""实现简单的SIFT检测"""
	sift = cv2.xfeatures2d.SIFT_create()

	imageRot = rotsImg(image, -45, 0.8) #旋转缩放
	imageGray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	imageRotGray = cv2.cvtColor(imageRot, cv2.COLOR_RGB2GRAY)


	kp1, des1 = sift.detectAndCompute(imageGray, None)
	kp2, des2 = sift.detectAndCompute(imageRotGray, None)

	imageSIFT = cv2.drawKeypoints(image,kp1,image,color=(255,0,255)) #画出特征点，并显示为红色圆圈
	imageRotSIFT = cv2.drawKeypoints(imageRot,kp2,imageRot,color=(255,0,255)) #画出特征点，并显示为红色圆圈

	hmerge = np.hstack((imageSIFT, imageRotSIFT))#水平拼接
	
	return hmerge, des1, des2, kp1, kp2, imageRot

def BFmatch(image, des1, des2, kp1, kp2, imageRot, dis=True):
	"""使用KNN算法进行匹配，如果dis为false，直接匹配，默认为True"""
	bf = cv2.BFMatcher()
	matches = bf.knnMatch(des1, des2, k=2)
	if(dis == True):
		good = []
		for m,n in matches:
			if m.distance < 0.75*n.distance:
				good.append([m])
		imgRes = cv2.drawMatchesKnn(image, kp1, imageRot, kp2, good, None,flags=2)
	else:
		imgRes = cv2.drawMatchesKnn(image, kp1, imageRot, kp2, matches, None,flags=2)

	return imgRes

if __name__ == '__main__':
	image = cv2.imread("./image/image.jpg")
	imageRe = cv2.resize(image, (300,400))

	imageSift, des1, des2, kp1, kp2, imageRot = SIFT_CV(imageRe)

	imageRes = BFmatch(imageRe, des1, des2, kp1, kp2, imageRot)

	cv2.imshow("imageSift", imageRes)
	cv2.waitKey(20000)
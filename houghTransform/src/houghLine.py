import cv2
import numpy as np
import math

def houghL(image, angleStep=1, linesAreWhite=True):
	"""
	得到霍夫变换的投票结果

	Input:
	image: canny算子边缘检测后的结果
	angleStep: 角度的间距，默认为1
	lineAreWhite: 白色的为边（bool）
	
	Output:
	accumulator: 投票后得到的曲线
	theta: 可能取得角度
	rhos: 可能取得长度
	""" 

	# 为边缘的阈值，感觉有些多余
	value_threshold = 5

	theta = np.deg2rad(np.arange(-180.0, 180.0, angleStep)) # 角度数组，弧度表示
	width, height = image.shape # 图片的长和宽
	# 直线可能的取值
	diag_len = int(round(math.sqrt(width*width + height*height)))
	rhos = np.linspace(0, diag_len, diag_len)

	cos_t = np.cos(theta)
	sin_t = np.sin(theta)
	num_theta = len(theta)

	# 定义投票矩阵
	accumulator = np.zeros((2 * diag_len, num_theta), dtype=np.uint8)
	are_edges = image > value_threshold if linesAreWhite else image < value_threshold

	y_idx, x_idx = np.nonzero(are_edges)

	# Vote in the hough accumulator
	for i in range(len(x_idx)):
		x = x_idx[i]
		y = y_idx[i]

		for t_idx in range(num_theta):
			# Calculate rho. diag_len is added for a positive index
			rho = diag_len + int(round(x * cos_t[t_idx] + y * sin_t[t_idx]))
			accumulator[rho, t_idx] += 1

	return accumulator, theta, rhos

def showHoughLine(image, accumulator, thetas, rhos, save_path=None):
	"""这一步还不知道怎么写"""
	pass

if __name__ == '__main__':
	I = cv2.imread('./1.jpg')

	I_gray = cv2.cvtColor(I, cv2.COLOR_RGB2GRAY)
	I_gray = cv2.resize(I_gray, (300,400))

	# canny
	I_edge = cv2.Canny(I_gray, 50, 150)

	acc, theta, rhos = houghL(I_edge)

	res = showHoughLine(I_edge, acc, theta, rhos)

	cv2.imwrite('./canny.jpg', I_edge)
	cv2.imwrite('./accumulator.jpg', acc)


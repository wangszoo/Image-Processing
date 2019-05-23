import cv2
import numpy as np 

# def NMS():

def sobel(image):
	"""返回sobel边缘检测的结果"""
	x = cv2.Sobel(image, cv2.CV_16S, 1, 0)
	y = cv2.Sobel(image, cv2.CV_16S, 0, 1)

	absX = cv2.convertScaleAbs(x)
	absY = cv2.convertScaleAbs(y)

	image = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
	grad = np.arctan2(absY, absX)

	return image, grad

def suppression(img, D):
    """ Non-maximum suppression
    只有是极大值的时候，才赋值，否则为0
    Args:
        img: Sobel算子检测后的图像
        D: 梯度值
    Returns:
        image
    """

    M, N = img.shape
    res = np.zeros((M,N), dtype=np.int32)

    for i in range(M):
        for j in range(N):
            # find neighbour pixels to visit from the gradient directions
            where = round_angle(D[i, j])
            try:
                if where == 0:
                    if (img[i, j] >= img[i, j - 1]) and (img[i, j] >= img[i, j + 1]):
                        res[i,j] = img[i,j]
                elif where == 90:
                    if (img[i, j] >= img[i - 1, j]) and (img[i, j] >= img[i + 1, j]):
                        res[i,j] = img[i,j]
                elif where == 135:
                    if (img[i, j] >= img[i - 1, j - 1]) and (img[i, j] >= img[i + 1, j + 1]):
                        res[i,j] = img[i,j]
                elif where == 45:
                    if (img[i, j] >= img[i - 1, j + 1]) and (img[i, j] >= img[i + 1, j - 1]):
                        res[i,j] = img[i,j]
            except IndexError as e:
                """ Todo: Deal with pixels at the image boundaries. """
                pass
    return res

def round_angle(angle):
    """ Input angle must be in [0,180) 
    返回梯度方向的角度
    """

    angle = np.rad2deg(angle) % 180 #弧度转换成角度
    if (0 <= angle < 22.5) or (157.5 <= angle < 180):
        angle = 0
    elif (22.5 <= angle < 67.5):
        angle = 45
    elif (67.5 <= angle < 112.5):
        angle = 90
    elif (112.5 <= angle < 157.5):
        angle = 135
    return angle

def threshold(img, t, T):
    """ Thresholding
    Iterates through image pixels and marks them as WEAK and STRONG edge
    pixels based on the threshold values.
    双阈值提取强边缘和弱边缘
    Args:
        img: Numpy ndarray of image to be processed (suppressed image)
        t: lower threshold
        T: upper threshold
    Return:
        img: Thresholdes image
    """
    # define gray value of a WEAK and a STRONG pixel
    cf = {
        'WEAK': np.int32(50),
        'STRONG': np.int32(255),
    }

    # get strong pixel indices
    strong_i, strong_j = np.where(img > T)

    # get weak pixel indices
    weak_i, weak_j = np.where((img >= t) & (img <= T))

    # get pixel indices set to be zero
    zero_i, zero_j = np.where(img < t)

    # set values
    img[strong_i, strong_j] = cf.get('STRONG')
    img[weak_i, weak_j] = cf.get('WEAK')
    img[zero_i, zero_j] = np.int32(0)

    return (img, cf.get('WEAK'))

def tracking(img, weak, strong=255):
    """ 
    Checks if edges marked as weak are connected to strong edges.
    Note that there are better methods (blob analysis) to do this,
    but they are more difficult to understand. This just checks neighbour
    edges.
    Also note that for perfomance reasons you wouldn't do this kind of tracking
    in a seperate loop, you would do it in the loop of the tresholding process.
    Since this is an **educational** implementation ment to generate plots
    to help people understand the major steps of the Canny Edge algorithm,
    we exceptionally don't care about perfomance here.
    这里原文中用了6个邻域，改动之后用了8个邻域
    Args:
        img: Numpy ndarray of image to be processed (thresholded image)
        weak: Value that was used to mark a weak edge in Step 4
    Returns:
        final Canny Edge image.
    """

    M, N = img.shape
    for i in range(M):
        for j in range(N):
            if img[i, j] == weak:
                # check if one of the neighbours is strong (=255 by default)
                try:
                    if ((img[i + 1, j] == strong) or (img[i - 1, j] == strong)
                         or (img[i, j + 1] == strong) or (img[i, j - 1] == strong)
                         or (img[i+1, j + 1] == strong) or (img[i-1, j - 1] == strong)
                         or (img[i-1, j + 1] == strong) or (img[i-1, j + 1] == strong)):
                        img[i, j] = strong
                    else:
                        img[i, j] = 0
                except IndexError as e:
                    pass
    return img


if __name__ == '__main__':
	I = cv2.imread('./1.jpg')
	I = cv2.resize(I, (300,400))
	I = cv2.cvtColor(I, cv2.COLOR_RGB2GRAY)

	sobelI, gradI = sobel(I) # 返回sobel结果和梯度方向

	imageNMS = suppression(sobelI, gradI) # 返回非极大抑制后的结果

	imageThres, weak = threshold(imageNMS,40,80) # 返回阈值后的结果

	imageRes = tracking(imageThres, weak, strong=255) # 抑制孤立的边缘

	cv2.imwrite('./soble.jpg', sobelI)
	cv2.imwrite('./imageNMS.jpg', imageNMS)
	cv2.imwrite('./imageThres.jpg', imageThres)
	cv2.imwrite('./imageRes.jpg', imageRes)





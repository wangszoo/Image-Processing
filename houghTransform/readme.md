# 霍夫变换（直线）

## 算法

霍夫变化检测直线时，主要用到公式：

$$y = (-\frac{cos\theta}{sin\theta})x + (\frac{r}{sin\theta})$$

由这个公式可以得到：

$$r = x*cos\theta + y*sin\theta$$

既把坐标映射到霍夫空间中去。

## 步骤

- 使用canny算法得到边缘图
- 定义$\theta$，和直线的长度
- 定义霍夫变换的投票矩阵
- 遍历二值图像
  - 为边缘的话，由公式2计算所有的r，和$\theta$的值
  - 这样投票矩阵就计算出来了

之后的部分需要判定直线的起始位置，还没有写。

## 结果

![canny](https://github.com/wangchau/Image-Processing/blob/master/houghTransform/pic/canny.jpg?raw=true)

![accumulator](https://github.com/wangchau/Image-Processing/blob/master/houghTransform/pic/accumulator.jpg?raw=true)

## 优缺点

- 优点：Hough直线检测的优点是抗干扰能力强，对图像中直线的殘缺部分、噪声以及其它共存的非直线结构不敏感。
- 缺点：Hough变换算法的特点导致其时间复杂度和空间复杂度都很高，并且在检测过程中只能确定直线方向，丢失了线段的长度信息。

## 参考文献

- <https://www.zhihu.com/search?q=%E9%9C%8D%E5%A4%AB%E5%8F%98%E6%8D%A2&type=content>
- <https://blog.csdn.net/caomin1hao/article/details/81081880>
- <https://blog.csdn.net/YuYunTan/article/details/80141392>
- <https://github.com/alyssaq/hough_transform>
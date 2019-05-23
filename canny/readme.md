# canny边缘检测

## 步骤

- 使用高斯滤波器滤波，平滑和滤去噪声
- 计算梯度强度和方向（本文中使用Sobel算子实现）
- 应用非极大抑制
- 双阈值滤波
- 抑制孤立的弱边缘

## 代码

​	主要实现的事3，4，5三部分

## 效果

![屏幕快照 2019-05-20 下午2.16.26](https://github.com/wangchau/working/blob/master/%E5%9B%BE%E5%83%8F%E5%A4%84%E7%90%86/canny/pic/res.png)

## 参考文献

- <https://www.zhihu.com/question/37172820>
- <https://www.cnblogs.com/techyan1990/p/7291771.html>
- <https://github.com/fubel/PyCannyEdge>
- <https://github.com/fubel/PyCannyEdge/blob/master/CannyEdge>

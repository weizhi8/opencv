# 一、基于opencv-python开发的测距，测角度算法
# opencv版本
本人使用的是opencv4版本，使用opencv3版本的需要小小调整代码，不然会报错
# 运行结果如下：
![220081684ecf99cc10a3f76d54856b8](https://user-images.githubusercontent.com/109148529/228763622-0fae22f4-bc11-472e-89c8-5bb5db0632eb.png)

![6608d72c2fed26e7336653917714d19](https://user-images.githubusercontent.com/109148529/228763730-258ff1f5-f11e-4ba1-a904-36dfab417b73.png)
# 使用方法：
替换下面参数即可：
![7b53883d02eb889474587f03ae78828](https://user-images.githubusercontent.com/109148529/228764669-79d765a7-d25b-4389-a397-8b62aba3f1c1.png)
# 注意事项：
 必须有一个最小面积的矩形提供长度参考,在main里面的W,H参数也是这个参考的长度(默认单位为cm)
 如果没有最小矩形面积会报错
 下版本优化
# 算法问题可联系：
2275716724@qq.com

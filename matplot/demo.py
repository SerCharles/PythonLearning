import numpy as np
import matplotlib.pyplot as plt

#定义基本信息
# Figure 并指定大小
#一号图，大小是16*10英寸
plt.figure(num = 1, figsize = (16,10))
#设置整体标题
plt.suptitle(r'demo',fontsize = 20, color = 'black')
#设置 x，y 轴的范围以及 label 标注
#x的范围：-1到20,y范围：-2到30,标签分别为x，y
plt.xlim(-1,20)
plt.ylim(-2,30)
plt.xlabel('x')
plt.ylabel('y')
# 设置坐标轴刻度线 
# Tick X 范围 (0,20),11个标签（相当于每两个一个标签）
new_ticks = np.linspace(0,20,11)
plt.xticks(new_ticks)
# Tick Y 范围，别名(下面的英文)
plt.yticks([0, 5, 10, 15, 20, 25, 30],
          [r'$zero$',r'$five$',r'$ten$',r'$fifteen$',r'$twenty$',r'$twenty\ five$',r'$thirty$'])
# 设置坐标轴 gca() 获取坐标轴信息
ax = plt.gca()


#定义数据
#离散变量
x = [2, 6, 9, 13]
y = [4, 8, 12, 21]
#近似连续变量
#定义xx变量的范围 (0，6) 数量 100 
xx = np.linspace(0, 6, 100)
yy = xx ** 2
xxx = np.linspace(0, 6, 100)
yyy = 2 ** xxx 
xxxx = np.linspace(1, 13, 4)
yyyy_man_1 = [20, 23, 30, 27]
yyyy_woman_1 = [19, 27, 25, 23]
yyyy_man_2 = [18, 22, 29, 24]
yyyy_woman_2 = [23, 30, 27, 24]
#第一个图：散点图
#两行两列的图，这个是第一行第一个
plt.subplot(221)
#子图标题
plt.title(r'scatter',fontsize = 10, color = 'black')
plt.scatter(x, y, color = 'black', label = 'scatter')
plt.plot(xx, yy, color = 'red', label = '$y = x^{2}$')
#图例
#ax.legend()
plt.legend()

#第二个图:拟合图
plt.subplot(222)
plt.title(r'linear',fontsize = 10, color = 'black')
#线性拟合y值
f1 = np.polyfit(x, y, 1)
#p1是拟合函数
p1 = np.poly1d(f1)
y_linear = p1(x)  
plt.plot(x, y_linear, color = 'blue', label = '$y = 1.53x - 0.23$')
plt.scatter(x, y, color = 'black', label = 'scatter')
plt.plot(xx, yy, color = 'red', label = '$y = x^{2}$')
#标记
#xy：箭头左下角位置，xytext：字最左边位置
plt.annotate('zero point', xy=(0, 0),
            xytext=(2, 13),
            arrowprops=dict(facecolor='black', shrink=0.05)
            )
plt.legend()

#第三个图：坐标变换后
plt.subplot(223)
plt.title(r'log',fontsize = 10, color = 'black')
plt.semilogy(xxx, yyy, color = 'blue', label = '$y = 2 ^{x}$')
plt.semilogy(xx, yy, color = 'red', label = '$y = x ^ {2}$')
plt.legend()

#第四个图： 条形图
plt.subplot(224)
plt.title(r'bar',fontsize = 10, color = 'black')
#画图
width = 0.5
plt.bar(xxxx - 0.6 * width, yyyy_man_1, width, color = 'red', label = 'men')
plt.bar(xxxx - 0.6 * width, yyyy_woman_1, width, bottom = yyyy_man_1, color = 'blue', label = 'women')
plt.bar(xxxx + 0.6 * width, yyyy_man_2, width, color = 'red')
plt.bar(xxxx + 0.6 * width, yyyy_woman_2, width, bottom = yyyy_man_2, color = 'blue')
#设置x，y轴标题和图例
plt.ylabel('Scores')
plt.xticks(xxxx, ('2015', '2016', '2017', '2018', '2019'))
plt.yticks(np.arange(0, 60, 5))
plt.legend()

  


#显示函数
plt.show()
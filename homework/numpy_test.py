import numpy as np
#创建数组a
a = np.array([[10,20],[30,40]])
a1 = np.array([[10,20]])
print (a)
#创建数组b
b = np.array([[50,60],[70,80]])
b1 = np.array([[50],[70]])
print (b)
#沿轴 0 连接两个数组
print (np.concatenate((a1,b)))
#沿轴 1 连接两个数组
print (np.concatenate((a,b1),axis = 1))
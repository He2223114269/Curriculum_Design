import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor
from sklearn import linear_model
from sklearn import svm
from sklearn import neighbors
from sklearn import ensemble
#测试sklearn中不同的回归方法
# 为了实验用，我自己写了一个二元函数，y=0.5*np.sin(x1)+ 0.5*np.cos(x2)+0.1*x1+3。其中x1的取值范围是0~50，x2的取值范围是-10~10，x1
# x2的训练集一共有500个，测试集有100个。其中，在训练集的上加了一个-0.5~0.5的噪声。生成函数的代码如下：
def f(x1, x2):
    y = 0.5 * np.sin(x1) + 0.5 * np.cos(x2)  + 0.1 * x1 + 3
    return y

def load_data():
    x1_train = np.linspace(0,50,500)
    x2_train = np.linspace(-10,10,500)
    data_train = np.array([[x1,x2,f(x1,x2) + (np.random.random(1)-0.5)] for x1,x2 in zip(x1_train, x2_train)])
    x1_test = np.linspace(0,50,100)+ 0.5 * np.random.random(100)
    x2_test = np.linspace(-10,10,100) + 0.02 * np.random.random(100)
    data_test = np.array([[x1,x2,f(x1,x2)] for x1,x2 in zip(x1_test, x2_test)])
    return data_train, data_test

def try_different_method(clf,str,i):
    train, test = load_data()
    x_train, y_train = train[:, :2], train[:, 2]  # 数据前两列是x1,x2 第三列是y,这里的y有随机噪声
    x_test, y_test = test[:, :2], test[:, 2]  # 同上,不过这里的y没有噪声

    clf.fit(x_train,y_train)
    score = clf.score(x_test, y_test)
    result = clf.predict(x_test)
    plt.figure(i)
    plt.plot(np.arange(len(result)), y_test,'go-',label='true value')
    plt.plot(np.arange(len(result)),result,'ro-',label='predict value')
    plt.title(f"{i}: "+str+' score: %f'%score)
    plt.legend()


# def main():
clf = DecisionTreeRegressor() #决策树回归
str='DecisionTreeRegressor'
try_different_method(clf,str,1)
linear_reg = linear_model.LinearRegression()
str='LinearRegression'
try_different_method(clf,str,2)
svr = svm.SVR()
str='SVR'
try_different_method(clf,str,3)
knn = neighbors.KNeighborsRegressor()
str='KNN'
try_different_method(clf,str,4)
rf =ensemble.RandomForestRegressor(n_estimators=20)#这里使用20个决策树
str='RandomForestRegressor'
try_different_method(clf,str,5)
ada = ensemble.AdaBoostRegressor(n_estimators=50)
str='AdaBoostRegressor'
try_different_method(clf,str,6)
gbrt = ensemble.GradientBoostingRegressor(n_estimators=100)
str='GradientBoostingRegressor'
try_different_method(clf,str,7)
plt.show()

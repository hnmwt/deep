#P14 in[1]~

from sklearn.datasets import load_iris
iris_dataset = load_iris()

print("Keys of iris_dataset: \n{}".format(iris_dataset.keys()))

print(iris_dataset['DESCR'][:193]+ "\n...")

print("Target names: {}".format(iris_dataset['target_names']))

print("Feature names: \n{}".format(iris_dataset["feature_names"]))

print("Type of data:{}".format(type(iris_dataset['data'])))

print("shape of data: {}".format(iris_dataset['data'].shape))

print("First five columns of data:\n {}".format(iris_dataset['data'][:5]))

print("Type of target: {}".format(type(iris_dataset['target'])))

print("Shape of target: {}".format(iris_dataset['target'].shape))

print("Target:\n{}".format(iris_dataset['target']))

#P18 in{21}~
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    iris_dataset['data'], iris_dataset['target'], random_state=0)
print("X_train shape; {}".format(X_train.shape))
print("y_train shape; {}".format(y_train.shape))

print("X_test shape; {}".format(X_test.shape))
print("y_test shape; {}".format(y_test.shape))

#P21 in[24]~
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=1)

knn.fit(X_train,y_train)

#P22 in[26]~
import numpy as np
X_new = np.array([[5, 2.9, 1, 0.2]])
print("X_new.shape: {}".format(X_new.shape))

prediction = knn.predict(X_new)
print("Prediction: {}".format(prediction))
print("Predicted target name: {}".format(iris_dataset['target_names'][prediction]))

#P28 in[28]~
y_pred = knn.predict(X_test)
print("Test set predictions:\n {}" .format(y_pred))

#---------------------第2章　教師あり学習--------------------------------------------------
print("第２章")
import mglearn
import matplotlib.pyplot as plt

print(mglearn.datasets.make_forge())#データセットの確認
# p32 In[1]~
#データセットの生成
X,y = mglearn.datasets.make_forge()
#データセットをプロット
mglearn.discrete_scatter(X[:,0],X[:,1],y)
plt.legend(["Class 0","Class 1"], loc = 4)
plt.xlabel("First feature")
plt.ylabel("Second feature")
print("X.shape: {}".format(X.shape))
plt.show()                                  #pycharm上で表を出力する


print(mglearn.datasets.make_wave())  # データセットの確認
# In[2]
X, y = mglearn.datasets.make_wave(n_samples=40)
plt.plot(X, y, 'o')
plt.ylim(-3, 3)
plt.xlabel("Feature")
plt.ylabel("Target")
plt.show()                                  #pycharm上で表を出力する

#In[3]
from sklearn.datasets import load_breast_cancer
cancer = load_breast_cancer()
print(cancer)  # データセットの確認
print("cancer.keys(): \n{}" .format(cancer.keys()))
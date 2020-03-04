import pandas as pd
import helper
import cv2
import matplotlib.pyplot as plt

# df = pd.read_csv(r'./Data/example.csv')
# count = df.index[-1] + 1
# df.loc[0] = [0, 20, 1]
# print(count)
# print(df.head())
# df.drop([x for x in range(1934,1947)], inplace=True)
# df.reset_index(drop=True, inplace=True)
# df.to_csv(r'./Data/example.csv', index=False)
# count = df.index[-1] + 1
# print(count)

image_array = plt.imread("444.jpg")
plst = []
tempimage = []
for i in range(5):
    plst.append(helper.random_shear(image_array, 0))
    tempimage.append(helper.crop(plst[-1][0], 0.4, 0.3))
    tempimage[-1] = helper.resize(tempimage[-1],(64,64))
    cv2.imshow("keytest" + str(i), tempimage[-1])
    print(plst[-1][1])
cv2.waitKey(100000)





import serial
import cv2
import pandas as pd
import os

#mode = "RW"
mode = "CW"

ResetFlag = 0

path = "./Data"
file_names = os.listdir(path)
if "example.csv" not in file_names:
    md = [{'x': 0, 'y': 0, 'FB_para': 0}]
    df1 = pd.DataFrame(md)
    df1.to_csv(r'./Data/example.csv', index=False)
elif mode is "RW":
    md = [{'x': 0, 'y': 0, 'FB_para': 0}]
    df1 = pd.DataFrame(md)
    df1.to_csv(r'./Data/example.csv', index=False)
elif mode is "CW":
    pass

cap = cv2.VideoCapture(0)
if (cap.isOpened() == False):
    print("Unable to read camera feed")
count = 0
key = 0
df = pd.read_csv(r'./Data/example.csv')
count = df.index[-1]
print("Started...")

print("Loop Start...")
while True:
    ret, frame = cap.read()
    key = cv2.waitKey(50)
    print(key)
    if key is 97:
        valueList = [-1, 20, 1]
    elif key is 100:
        valueList = [1, 20, 1]
    elif key is 120:
        df.to_csv(r'./Data/example.csv', index=False)
        break
    elif key is -1:
        valueList = [0, 20, 1]

    if key is 99 and ResetFlag is 0:
        count -= 100
        if count < 0:
            count = 0
        ResetFlag = 1
        continue
    elif key is not '3':
        ResetFlag = 0

    #md = [{'x': valueList[0], 'y': valueList[1], 'FB_para': valueList[2]}]
    #df = pd.concat([df, pd.DataFrame(md)], ignore_index=True)

    df.loc[count] = valueList
    resized_img = cv2.resize(frame, (320, 180))
    cv2.imwrite('./Images/' + str(count) + '.jpg', resized_img)
    cv2.imshow("keytest", resized_img)
    count += 1



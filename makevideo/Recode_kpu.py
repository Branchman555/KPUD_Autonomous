import serial
import cv2
import pandas as pd
import os

mode = "RW"
#Re Write
#mode = "CW"
##Continue Write

ResetFlag = 0

ser = serial.Serial(
    port='COM8',
    baudrate=115200,
)

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
df = pd.read_csv(r'./Data/example.csv')
count = df.index[-1]
print("Started...")

if ser.readable():
    res = ser.readline()
    valueString = res.decode()[:len(res) - 1]
    print(valueString)
    res = ser.readline()
    valueString = res.decode()[:len(res) - 1]
    print(valueString)
    res = ser.readline()
    valueString = res.decode()[:len(res) - 1]
    print(valueString)

print("Loop Start...")
while True:
    if ser.readable():
        ser.flushInput()
        while True:
            res = ser.readline()
            valueString = res.decode()[:len(res) - 1]
            if len(valueString) < 2:
                continue
            elif valueString[0] is '<' and valueString[-1] is '>':
                valueString = valueString[1:-1]
                valueList = valueString.split(',')
                print(valueList)
                break
            else:
                print("err: " + valueString)

        if valueList[2] is '4':
            df.to_csv(r'./Data/example.csv', index=False)
            break

        if valueList[2] is '5' and ResetFlag is 0:
            count -= 100
            if count < 0:
                count = 0
            ResetFlag = 1
            continue
        elif valueList[2] is not '5':
            ResetFlag = 0

        if valueList[2] is '1':
            if int(valueList[0]) < -245:
                valueList[0] = str(-245)
            elif int(valueList[0]) > 245:
                valueList[0] = str(245)

            valueList[1] = 0
            df.loc[count] = valueList
            ret, frame = cap.read()
            resized_img = cv2.resize(frame, (320, 180))
            cv2.imwrite('./Images/' + str(count) + '.jpg', resized_img)
            cv2.imshow("keytest", resized_img)
            count += 1
    else:
        print("Not readable")

    key = cv2.waitKey(30)


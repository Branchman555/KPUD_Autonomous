import pandas as pd

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

import os

for filename in os.listdir("./Images"):
# 파일 확장자가 (properties)인 것만 처리
    filename_int = filename.split('.')[0]
    if int(filename_int) > 1946:
        os.rename('./Images/' + filename, './Images/' + str(int(filename_int)-13) + '.jpg')

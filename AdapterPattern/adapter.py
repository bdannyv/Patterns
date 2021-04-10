import pandas as pd
import os


class DataFrameToExcelSaver:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def to_excel(self):
        self.df.to_excel('test.xlsx')


class ToDataFrameAdapter(DataFrameToExcelSaver):
    def __init__(self, obj):
        self.object = obj

    def to_excel(self):
        df = pd.DataFrame(data=self.object)
        df.to_excel('test.xlsx')


if __name__ == "__main__":
    dict = {chr(k+65): [k+j for j in range(10)] for k in [i for i in range(5)]}
    target = DataFrameToExcelSaver(dict)
    try:
        target.to_excel()
    except AttributeError:
        print("'dict' object has no attribute 'to_excel' so i can use adapter")
        target = ToDataFrameAdapter(dict)
        target.to_excel()

    os.remove('test.xlsx')
    print('terminated successfully')
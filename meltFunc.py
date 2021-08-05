from numpy import pi
import pandas as pd

df = pd.read_csv("address.csv")

col_len = len(df.columns)

def meltFunc():
    df1= df.melt(id_vars=['Name'], var_name='Item', value_name='Value')
    df1.to_csv("address.csv", index = False)
    print(df1)

#unmelting
def pivotFunc():
    df2 = df.pivot(index = 'Name', columns = 'Item')
    df2 = df2['Value'].reset_index()
    df2.columns.name = None
    df2.to_csv("address.csv", index = False)
    print(df2)

if col_len == 3:
    pivotFunc()
else:
    meltFunc()
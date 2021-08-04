import pandas as pd

df = pd.read_csv("address.csv")
df1= df.melt(id_vars=['Name'], var_name='Item', value_name='Value')
df1.to_csv("address.csv", index = False)
print(df1)
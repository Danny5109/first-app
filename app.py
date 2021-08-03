from flask import Flask, request, render_template, session, redirect
import numpy as np
import pandas as pd

app = Flask(__name__)

df = pd.read_csv("address.csv")
df.to_csv("address.csv", header=["First Name", "Last Name", "Address", "Town", "Position", "Zip Code"], index = False)
df["Name"] = df["First Name"] +" "+ df["Last Name"]
df.drop(columns=["First Name", "Last Name"], inplace=True)

full_name = df.pop('Name')
df.insert(0, 'Name', full_name)

df1 = df['Address'].str.extract('(?P<Number>\d+)(?P<Address>.*)', expand=True)
df.drop(columns=["Address"], inplace=True)

number = df1.pop('Number')
df.insert(1, 'Number', number)

address = df1.pop('Address')
df.insert(2, 'Address', address)
df.to_csv("address.csv", index=False)

@app.route('/', methods=("POST", "GET"))
def html_table():
    return df.to_html()
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')
from flask import Flask, request, render_template, session, redirect
import numpy as np
import pandas as pd
import sqlite3 as sql
from employeedb import con

app = Flask(__name__)

df = pd.read_csv("address.csv")

def csv_task():
    df.columns = header=["First Name", "Last Name", "Address", "Town", "State", "Zip Code"]
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
    print(df)

if 'Name' in df.columns:
    print(df)
else:
    csv_task()

def create_table():
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS employee (name TEXT, door_num TEXT, address TEXT, town TEXT, state TEXT, zcode TEXT)')
    cur.close()

@app.route('/', methods=("POST", "GET"))
def html_table():
    return df.to_html()

@app.route('/db')
def form():
    return render_template("employees.html")

@app.route('/emp_detail', methods = ("POST", "GET"))

def emp_detail():
    create_table()
    try:
        name = request.form.get("name")
        door_num = request.form.get("door_num")
        address = request.form.get("address")
        town = request.form.get("town")
        state = request.form.get("state")
        zcode = request.form.get("zcode")

        cur = con.cursor()
        cur.execute("INSERT INTO employee (name, door_num, address, town, state, zcode) VALUES (?,?,?,?,?,?)",(name, door_num, address, town, state, zcode))
        msg = "Record successfully added"
        con.commit()
    except:
        con.rollback()
        msg = "error in insert operation"
    finally:
        cur.close()
        return render_template("result.html",msg = msg)

@app.route('/details', methods = ["GET"])
def show_emp_details():
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from employee")
    
    rows = cur.fetchall()
    print(rows)
    con.commit()
    cur.close()
    return render_template("list.html",rows = rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
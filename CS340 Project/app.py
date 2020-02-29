"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, request, redirect
from flask import render_template as render
from db_connector.db_connector import connect_to_database, execute_query
from jinja2 import Template
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

@app.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate)

@app.route('/')
def index():
    return render("index.html")

@app.route('/Items')
def Items():
    print("Fetching and rendering Items web page")
    db_connection = connect_to_database()
    query = "SELECT * from Items;"
    result = execute_query(db_connection, query).fetchall();
    print(result)
    return render("Items.html", rows=result)

@app.route('/Orders')
def Orders():
    print("Fetching and rendering Orders web page")
    db_connection = connect_to_database()

    rowQuery = "SELECT order_id, CONCAT(Customers.first_name,' ',Customers.last_name) AS cust_name, CONCAT(Employees.first_name,' ',Employees.last_name) AS emp_name, date, total, credit_card_num, exp_date, credit_card_code FROM Orders INNER JOIN Customers ON Orders.cust_id = Customers.cust_id INNER JOIN Employees ON Orders.emp_id = Employees.emp_id;"
    rowResult = execute_query(db_connection, rowQuery).fetchall();
    print(rowResult)

    customerDDQuery = "SELECT CONCAT(Customers.first_name,' ',Customers.last_name) FROM Customers;"
    customerDDResult = execute_query(db_connection, customerDDQuery).fetchall();
    print(customerDDResult)

    employeeDDQuery = "SELECT CONCAT(Employees.first_name,' ',Employees.last_name) FROM Employees;"
    employeeDDResult = execute_query(db_connection, employeeDDQuery).fetchall();
    print(employeeDDResult)

    itemDDQuery = "SELECT Items.item_name, Items.price FROM Items;"
    itemDDResult = execute_query(db_connection, itemDDQuery).fetchall();
    print(itemDDResult)

    itemRowQuery = "SELECT Orders.order_id, Items.item_name, Order_Items.quantity, Items.price * Order_Items.quantity AS item_total FROM Orders INNER JOIN Order_Items ON Orders.order_id = Order_Items.order_id INNER JOIN Items ON Order_Items.item_id = Items.item_id;"
    itemRowResult = execute_query(db_connection, itemRowQuery).fetchall();
    print(itemRowResult);

    return render("Orders.html", rows=rowResult, itemRow=itemRowResult, custDD=customerDDResult, empDD=employeeDDResult, itemDD=itemDDResult)

@app.route('/Customers')
def Customers():
    print("Fetching and rendering Customers web page")
    db_connection = connect_to_database()
    query = "SELECT * from Customers;"
    result = execute_query(db_connection, query).fetchall();
    print(result)
    return render("Customers.html", rows=result)

@app.route('/Employees')
def Employees():
    print("Fetching and rendering Employees web page")
    db_connection = connect_to_database()
    query = "SELECT * from Employees;"
    result = execute_query(db_connection, query).fetchall();
    print(result)
    return render("Employees.html", rows=result)


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)

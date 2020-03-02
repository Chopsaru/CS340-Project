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

@app.route('/Items', methods=['POST', 'GET'])
def Items():
    db_connection = connect_to_database()

    if request.method == 'GET':
        print("Fetching and rendering Items web page")
        query = "SELECT * from Items;"
        result = execute_query(db_connection, query).fetchall();
        print(result)
        return render("Items.html", rows=result)
    elif request.method == 'POST':
        print("Adding a row Items web page")
        price = request.form['price']
        item_name = request.form['item_name']
        description = request.form['description']
        quantity_available = request.form['quantity_available']
        query = "INSERT INTO Items (price, item_name, description, quantity_available) VALUES (%s, %s, %s, %s);"
        data = (price, item_name, description, quantity_available)
        result = execute_query(db_connection, query, data).fetchall();
        print(result)
        print("Item added.")
        print("Fetching and rendering Items web page")
        query2 = "SELECT * from Items;"
        result2 = execute_query(db_connection, query2).fetchall();
        print(result2)
        return render("Items.html", rows=result2)

@app.route('/Orders', methods=['POST', 'GET'])
def Orders():
    db_connection = connect_to_database()

    if request.method == 'GET':
        print("Fetching and rendering Orders web page")

        rowQuery = "SELECT order_id, CONCAT(Customers.first_name,' ',Customers.last_name) AS cust_name, CONCAT(Employees.first_name,' ',Employees.last_name) AS emp_name, date, total, credit_card_num, exp_date, credit_card_code FROM Orders INNER JOIN Customers ON Orders.cust_id = Customers.cust_id INNER JOIN Employees ON Orders.emp_id = Employees.emp_id;"
        rowResult = execute_query(db_connection, rowQuery).fetchall();
        print(rowResult)

        customerDDQuery = "SELECT Customers.cust_id, CONCAT(Customers.first_name,' ',Customers.last_name) FROM Customers;"
        customerDDResult = execute_query(db_connection, customerDDQuery).fetchall();
        print(customerDDResult)

        employeeDDQuery = "SELECT Employees.emp_id, CONCAT(Employees.first_name,' ',Employees.last_name) FROM Employees;"
        employeeDDResult = execute_query(db_connection, employeeDDQuery).fetchall();
        print(employeeDDResult)

        itemDDQuery = "SELECT Items.item_id, Items.item_name, Items.price FROM Items;"
        itemDDResult = execute_query(db_connection, itemDDQuery).fetchall();
        print(itemDDResult)

        itemRowQuery = "SELECT Orders.order_id, Items.item_name, Order_Items.quantity, Items.price * Order_Items.quantity AS item_total FROM Orders INNER JOIN Order_Items ON Orders.order_id = Order_Items.order_id INNER JOIN Items ON Order_Items.item_id = Items.item_id;"
        itemRowResult = execute_query(db_connection, itemRowQuery).fetchall();
        print(itemRowResult);

        return render("Orders.html", rows=rowResult, itemRow=itemRowResult, custDD=customerDDResult, empDD=employeeDDResult, itemDD=itemDDResult)

    elif request.method == 'POST':
        print("Adding a row Orders web page")
        cust_id = request.form['cust_id']
        emp_id = request.form['emp_id']
        date = request.form['date']
        total = request.form['total']
        credit_card_num = request.form['credit_card_num']
        exp_date = request.form['exp_date']
        credit_card_code = request.form['credit_card_code']
        item_id = request.form['item_id']
        quantity = request.form['quantity']
        query = "INSERT INTO Orders (cust_id, emp_id, date, total, credit_card_num, exp_date, credit_card_code) VALUES (%s, %s, %s, %s, %s, %s, %s); INSERT INTO Order_Items (order_id, item_id, quantity) VALUES (SELECT last_insert_id(), %s, %s);"
        data = (cust_id, emp_id, date, total, credit_card_num, exp_date, credit_card_code, item_id, quantity)
        result = execute_query(db_connection, query, data).fetchall();
        print(result)
        print("Order added.")

        print("Fetching and rendering Items web page")
        rowQuery = "SELECT order_id, CONCAT(Customers.first_name,' ',Customers.last_name) AS cust_name, CONCAT(Employees.first_name,' ',Employees.last_name) AS emp_name, date, total, credit_card_num, exp_date, credit_card_code FROM Orders INNER JOIN Customers ON Orders.cust_id = Customers.cust_id INNER JOIN Employees ON Orders.emp_id = Employees.emp_id;"
        rowResult = execute_query(db_connection, rowQuery).fetchall();
        print(rowResult)

        customerDDQuery = "SELECT Customers.cust_id, CONCAT(Customers.first_name,' ',Customers.last_name) FROM Customers;"
        customerDDResult = execute_query(db_connection, customerDDQuery).fetchall();
        print(customerDDResult)

        employeeDDQuery = "SELECT Employees.emp_id, CONCAT(Employees.first_name,' ',Employees.last_name) FROM Employees;"
        employeeDDResult = execute_query(db_connection, employeeDDQuery).fetchall();
        print(employeeDDResult)

        itemDDQuery = "SELECT Items.item_id, Items.item_name, Items.price FROM Items;"
        itemDDResult = execute_query(db_connection, itemDDQuery).fetchall();
        print(itemDDResult)

        itemRowQuery = "SELECT Orders.order_id, Items.item_name, Order_Items.quantity, Items.price * Order_Items.quantity AS item_total FROM Orders INNER JOIN Order_Items ON Orders.order_id = Order_Items.order_id INNER JOIN Items ON Order_Items.item_id = Items.item_id;"
        itemRowResult = execute_query(db_connection, itemRowQuery).fetchall();
        print(itemRowResult);

        return render("Orders.html", rows=rowResult, itemRow=itemRowResult, custDD=customerDDResult, empDD=employeeDDResult, itemDD=itemDDResult)

@app.route('/Customers', methods=['POST', 'GET'])
def Customers():
    db_connection = connect_to_database()

    if request.method == 'GET':
        print("Fetching and rendering Customers web page")
        query = "SELECT * from Customers;"
        result = execute_query(db_connection, query).fetchall();
        print(result)
        return render("Customers.html", rows=result)
    elif request.method == 'POST':
        print("Adding a row Customers web page")
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        query = "INSERT INTO Customers (email, first_name, last_name, phone_number) VALUES (%s, %s, %s, %s);"
        data = (email, first_name, last_name, phone_number)
        result = execute_query(db_connection, query, data).fetchall();
        print(result)
        print("Customer added.")
        print("Fetching and rendering Customers web page")
        query2 = "SELECT * from Customers;"
        result2 = execute_query(db_connection, query2).fetchall();
        print(result2)
        return render("Customers.html", rows=result2)

@app.route('/Employees', methods=['POST', 'GET'])
def Employees():
    db_connection = connect_to_database()

    if request.method == 'GET':
        print("Fetching and rendering Employees web page")
        query = "SELECT * from Employees;"
        result = execute_query(db_connection, query).fetchall();
        print(result)
        return render("Employees.html", rows=result)
    elif request.method == 'POST':
        print("Adding a row Employees web page")
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        query = "INSERT INTO Employees (first_name, last_name) VALUES (%s, %s);"
        data = (first_name, last_name)
        result = execute_query(db_connection, query, data).fetchall();
        print(result)
        print("Employee added.")
        print("Fetching and rendering Employees web page")
        query2 = "SELECT * from Employees;"
        result2 = execute_query(db_connection, query2).fetchall();
        print(result2)
        return render("Employees.html", rows=result2)


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)

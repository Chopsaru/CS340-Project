"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, request, redirect, url_for
from flask import render_template as render
from db_connector.db_connector import connect_to_database, execute_query
from jinja2 import Template
import itertools
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

#=========================================================
# Homepage route
#=========================================================
@app.route('/')
def index():
    return render("index.html")

#=========================================================
# Item routes
#=========================================================
@app.route('/Items', methods=['POST', 'GET'])
def Items():
    db_connection = connect_to_database()

    if request.method == 'GET':             # render the Items webpage
        print("Fetching and rendering Items web page")
        query = "SELECT * from Items;"
        result = execute_query(db_connection, query).fetchall();
        print(result)
        return render("Items.html", rows=result)
    elif request.method == 'POST':          # add an item
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

        # render the web page again after adding an item
        print("Fetching and rendering Items web page")
        query2 = "SELECT * from Items;"
        result2 = execute_query(db_connection, query2).fetchall();
        print(result2)
        return render("Items.html", rows=result2)

@app.route('/Items/edit/<int:id>', methods=['POST', 'GET'])
def editItem(id):
    db_connection = connect_to_database()

    if request.method == 'GET':             # render the edit Items webpage
        print("Fetching and rendering edit item web page")
        query = "SELECT * from Items WHERE item_id = %s;"
        data = (id,)
        result = execute_query(db_connection, query, data).fetchall();
        print(result)
        return render("editItem.html", rows=result)
    elif request.method == 'POST':          # edit an item
        print("Adding a row Items web page")
        price = request.form['price']
        item_name = request.form['item_name']
        description = request.form['description']
        quantity_available = request.form['quantity_available']
        query = "UPDATE Items SET price = %s, item_name = %s, description = %s, quantity_available = %s WHERE item_id = %s;"
        data = (price, item_name, description, quantity_available, id)
        result = execute_query(db_connection, query, data).fetchall();
        print(result)
        print("Item edited.")

        #return to the Items web page
        return redirect(url_for('Items'))

@app.route('/deleteItem/<int:id>')
def deleteItem(id):
    db_connection = connect_to_database()
    query = "DELETE FROM Items WHERE item_id = %s"
    data = (id,)

    execute_query(db_connection, 'SET FOREIGN_KEY_CHECKS=0;')
    result = execute_query(db_connection, query, data)
    execute_query(db_connection, 'SET FOREIGN_KEY_CHECKS=1;')
    print(str(result.rowcount) + "row deleted")
    return redirect(url_for('Items'))

#=========================================================
# Orders routes
#=========================================================
@app.route('/Orders', methods=['POST', 'GET'])
def Orders():
    db_connection = connect_to_database()

    if request.method == 'GET':             # render the Orders webpage
        print("Fetching and rendering Orders web page")

        rowQuery = "SELECT order_id, CONCAT(Customers.first_name,' ',Customers.last_name) AS cust_name, CONCAT(Employees.first_name,' ',Employees.last_name) AS emp_name, date, total, credit_card_num, exp_date, credit_card_code FROM Orders LEFT JOIN Customers ON Orders.cust_id = Customers.cust_id LEFT JOIN Employees ON Orders.emp_id = Employees.emp_id;"
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

        itemRowQuery = "SELECT Orders.order_id, Items.item_name, Order_Items.quantity, Items.price * Order_Items.quantity AS item_total FROM Orders LEFT JOIN Order_Items ON Orders.order_id = Order_Items.order_id LEFT JOIN Items ON Order_Items.item_id = Items.item_id;"
        itemRowResult = execute_query(db_connection, itemRowQuery).fetchall();
        print(itemRowResult);

        return render("Orders.html", rows=rowResult, itemRow=itemRowResult, custDD=customerDDResult, empDD=employeeDDResult, itemDD=itemDDResult)

    elif request.method == 'POST':          # add an order
        count = 1               # the count of Order Items
        item_ids = []           # holds the item_id of each item in Order_Items
        quantities = []         # holds the quantity of each item in Order_Items 

        print("Adding a row Orders web page")
        cust_id = request.form['cust_id']
        emp_id = request.form['emp_id']
        date = request.form['date']
        credit_card_num = request.form['credit_card_num']
        exp_date = request.form['exp_date']
        credit_card_code = request.form['credit_card_code']
        item_id = request.form['item_id']           # holds the first item_id
        quantity = request.form['quantity']         # holds the first quantity

        while(str(request.form.get('item_id_' + str(count))) != "None"):
            item_ids.append(request.form.get("item_id_" + str(count)))          # add remaining item_ids
            quantities.append(request.form.get("quantity_" + str(count)))       # add remaining quantities
            count += 1

        # insert the order 
        query = "INSERT INTO Orders (cust_id, emp_id, date, total, credit_card_num, exp_date, credit_card_code) VALUES (%s, %s, %s, NULL, %s, %s, %s);"
        query2 = "INSERT INTO Order_Items (order_id, item_id, quantity) VALUES ((SELECT Orders.order_id FROM Orders ORDER BY Orders.order_id DESC LIMIT 1), %s, %s);"
        data = (cust_id, emp_id, date, credit_card_num, exp_date, credit_card_code)
        data2 = (item_id, quantity)
        result = execute_query(db_connection, query, data).fetchall();
        print(result)
        print("Order added.")

        # insert the first row in Order_Items
        result2 = execute_query(db_connection, query2, data2).fetchall();
        print(result2)
        print("The first row was added to Order_Items.")

        # insert the remaining rows in Order_Items
        for item_id, quantity in zip(item_ids, quantities):
            data3 = (item_id, quantity)
            print("item_id is equal to: ", item_id, "and quantity is equal to: ", quantity)
            result3 = execute_query(db_connection, query2, data3).fetchall();
            print(result3)
            print("A additional row was added to Order_Items.")
           
        # insert total into the order that was just added
        query3 = "UPDATE Orders SET total = (SELECT SUM(Items.price * Order_Items.quantity) FROM Order_Items INNER JOIN Items ON Order_Items.item_id = Items.item_id WHERE Order_Items.order_id = (SELECT Orders.order_id FROM Orders ORDER BY Orders.order_id DESC LIMIT 1)) WHERE Orders.order_id = (SELECT Orders.order_id FROM Orders ORDER BY Orders.order_id DESC LIMIT 1);"
        result4 = execute_query(db_connection, query3).fetchall();
        print(result4)
        print("Order total added.")

        # render the web page again after adding an order and the order items
        print("Fetching and rendering Items web page")
        rowQuery = "SELECT order_id, CONCAT(Customers.first_name,' ',Customers.last_name) AS cust_name, CONCAT(Employees.first_name,' ',Employees.last_name) AS emp_name, date, total, credit_card_num, exp_date, credit_card_code FROM Orders LEFT JOIN Customers ON Orders.cust_id = Customers.cust_id LEFT JOIN Employees ON Orders.emp_id = Employees.emp_id;"
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

        itemRowQuery = "SELECT Orders.order_id, Items.item_name, Order_Items.quantity, Items.price * Order_Items.quantity AS item_total FROM Orders LEFT JOIN Order_Items ON Orders.order_id = Order_Items.order_id LEFT JOIN Items ON Order_Items.item_id = Items.item_id;"
        itemRowResult = execute_query(db_connection, itemRowQuery).fetchall();
        print(itemRowResult);

        return render("Orders.html", rows=rowResult, itemRow=itemRowResult, custDD=customerDDResult, empDD=employeeDDResult, itemDD=itemDDResult)

@app.route('/Orders/edit/<int:id>', methods=['POST', 'GET'])
def editOrder(id):
    db_connection = connect_to_database()

    if request.method == 'GET':             # render the edit Orders webpage
        print("Fetching and rendering edit order web page")

        rowQuery = "SELECT order_id, Customers.cust_id, Employees.emp_id, date, total, credit_card_num, exp_date, credit_card_code FROM Orders LEFT JOIN Customers ON Orders.cust_id = Customers.cust_id LEFT JOIN Employees ON Orders.emp_id = Employees.emp_id WHERE Orders.order_id = %s;"
        data = (id,)
        rowResult = execute_query(db_connection, rowQuery, data).fetchall();
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

        itemRowQuery = "SELECT Orders.order_id, Order_Items.item_id, Order_Items.quantity FROM Orders LEFT JOIN Order_Items ON Orders.order_id = Order_Items.order_id LEFT JOIN Items ON Order_Items.item_id = Items.item_id WHERE Orders.order_id = %s;"
        itemRowResult = execute_query(db_connection, itemRowQuery, data).fetchall();
        print(itemRowResult);

        return render("editOrders.html", rows=rowResult, itemRow=itemRowResult, custDD=customerDDResult, empDD=employeeDDResult, itemDD=itemDDResult)

    elif request.method == 'POST':
        return "....but nothing happened"
    #will finish this bit later ¯\_(ツ)_/¯

@app.route('/deleteOrder/<int:id>')
def deleteOrder(id):
    db_connection = connect_to_database()
    query1 = "DELETE FROM Orders WHERE order_id = %s"
    query2 = "DELETE FROM Order_Items WHERE order_id = %s"
    data = (id,)

    execute_query(db_connection, 'SET FOREIGN_KEY_CHECKS=0;')
    result = execute_query(db_connection, query1, data)
    result = execute_query(db_connection, query2, data)
    execute_query(db_connection, 'SET FOREIGN_KEY_CHECKS=1;')
    print(str(result.rowcount) + "row deleted")
    return redirect(url_for('Orders'))

#=========================================================
# Customers routes
#=========================================================
@app.route('/Customers', methods=['POST', 'GET'])
def Customers():
    db_connection = connect_to_database()

    if request.method == 'GET':             # render the Customers webpage
        print("Fetching and rendering Customers web page")
        query = "SELECT * from Customers;"
        result = execute_query(db_connection, query).fetchall();
        print(result)
        return render("Customers.html", rows=result)
    elif request.method == 'POST':          # add a customer
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

        # render the web page again after adding a customer
        print("Fetching and rendering Customers web page")
        query2 = "SELECT * from Customers;"
        result2 = execute_query(db_connection, query2).fetchall();
        print(result2)
        return render("Customers.html", rows=result2)

@app.route('/Customers/edit/<int:id>', methods=['POST', 'GET'])
def editCustomer(id):
    db_connection = connect_to_database()

    if request.method == 'GET':             # render the edit customer webpage
        print("Fetching and rendering edit customer web page")
        query = "SELECT * from Customers WHERE cust_id = %s;"
        data = (id,)
        result = execute_query(db_connection, query, data).fetchall();
        print(result)
        return render("editCustomer.html", rows=result)
    elif request.method == 'POST':          # edit a customer
        print("Editing a row Customers web page")
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        query = "UPDATE Customers SET email = %s, first_name = %s, last_name = %s, phone_number = %s WHERE cust_id = %s;"
        data = (email, first_name, last_name, phone_number, id)
        result = execute_query(db_connection, query, data).fetchall();
        print(result)
        print("Customer edited.")

        #return to the Items web page
        return redirect(url_for('Customers'))

@app.route('/deleteCust/<int:id>')
def deleteCust(id):
    db_connection = connect_to_database()
    query = "DELETE FROM Customers WHERE cust_id = %s"
    data = (id,)

    execute_query(db_connection, 'SET FOREIGN_KEY_CHECKS=0;')
    result = execute_query(db_connection, query, data)
    execute_query(db_connection, 'SET FOREIGN_KEY_CHECKS=1;')
    print(str(result.rowcount) + "row deleted")
    return redirect(url_for('Customers'))


#=========================================================
# Employees routes
#=========================================================
@app.route('/Employees', methods=['POST', 'GET'])
def Employees():
    db_connection = connect_to_database()

    if request.method == 'GET':             # render the Employees webpage
        print("Fetching and rendering Employees web page")
        query = "SELECT * from Employees;"
        result = execute_query(db_connection, query).fetchall();
        print(result)
        return render("Employees.html", rows=result)
    elif request.method == 'POST':          # add an employee
        print("Adding a row Employees web page")
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        query = "INSERT INTO Employees (first_name, last_name) VALUES (%s, %s);"
        data = (first_name, last_name)
        result = execute_query(db_connection, query, data).fetchall();
        print(result)
        print("Employee added.")

        # render the web page again after adding an employee
        print("Fetching and rendering Employees web page")
        query2 = "SELECT * from Employees;"
        result2 = execute_query(db_connection, query2).fetchall();
        print(result2)
        return render("Employees.html", rows=result2)

@app.route('/Employees/edit/<int:id>', methods=['POST', 'GET'])
def editEmp(id):
    db_connection = connect_to_database()

    if request.method == 'GET':             # render the edit Employees webpage
        print("Fetching and rendering edit employees web page")
        query = "SELECT * from Employees WHERE emp_id = %s;"
        data = (id,)
        result = execute_query(db_connection, query, data).fetchall();
        print(result)
        return render("editEmployees.html", rows=result)
    elif request.method == 'POST':          # edit an employee
        print("Editing a row on Employees web page")
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        query = "UPDATE Employees SET first_name = %s, last_name = %s WHERE emp_id = %s;"
        data = (first_name, last_name, id)
        result = execute_query(db_connection, query, data).fetchall();
        print(result)
        print("Employee edited.")

        #return to the Items web page
        return redirect(url_for('Employees'))

@app.route('/deleteEmp/<int:id>')
def deleteEmp(id):
    db_connection = connect_to_database()
    query = "DELETE FROM Employees WHERE emp_id = %s"
    data = (id,)

    execute_query(db_connection, 'SET FOREIGN_KEY_CHECKS=0;')
    result = execute_query(db_connection, query, data)
    execute_query(db_connection, 'SET FOREIGN_KEY_CHECKS=1;')
    print(str(result.rowcount) + "row deleted")
    return redirect(url_for('Employees'))


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)

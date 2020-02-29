/* Item Page Queries*/
SELECT * FROM Items

INSERT INTO Items (price, item_name, description, quantity_available) 
	VALUES (:priceIn, :item_nameIn, :descriptionIn, :quantity_availableIn)

UPDATE Items SET price=:priceIn, item_name=:item_nameIn, description=:descriptionIn, quantity_avaliable=:quantity_availableIn
WHERE item_id=:item_idINPUT_FROM_CLICK

DELETE FROM Items WHERE item_id=:item_idINPUT_FROM_CHECKBOXES	/*loop this query for each id selected



/* Customer Page Queries*/
SELECT * FROM Customers

INSERT INTO Customers (email, first_name, last_name, phone_number) 
	VALUES (:emailInput, :first_nameIn, :last_nameIn, :phone_numberIn)

UPDATE Customers SET email=:emailIn, first_name=:first_nameIn, last_name=:last_nameIn, phone_number=:phone_numberIn WHERE cust_id=:cust_idINPUT_FROM_CLICK

DELETE FROM Customers WHERE cust_id=:cust_idINPUT_FROM_CHECKBOXES	/*loop this query for each id selected



/* Employee Page Queries*/
SELECT * FROM Employees

INSERT INTO Employees (first_name, last_name) 
	VALUES (:first_nameIn, :last_nameIn,)

UPDATE Employees SET first_name=:first_nameIn, last_name=:last_nameIn WHERE emp_id=:emp_idINPUT_FROM_CLICK

DELETE FROM Employees WHERE emp_id=:emp_idINPUT_FROM_CHECKBOXES	/*loop this query for each id selected



/* Order Page Queries*/
-- queries for displaying the Orders table
SELECT order_id, CONCAT(Customers.first_name,' ',Customers.last_name) AS cust_name, CONCAT(Employees.first_name,' ',Employees.last_name) AS emp_name,
date, total, credit_card_num, exp_date, credit_card_code
FROM Orders
INNER JOIN Customers ON Orders.cust_id = Customers.cust_id
INNER JOIN Employees ON Orders.emp_id = Employees.emp_id

-- queries for displaying Customers, Employees, and Items dropdown menus
SELECT CONCAT(Customers.first_name,' ',Customers.last_name) FROM Customers
SELECT CONCAT(Employees.first_name,' ',Employees.last_name) FROM Employees
SELECT Items.item_name, Items.price FROM Items

-- queries for displaying Order_Items under each order in the Orders table
SELECT Items.item_name, Order_Items.quantity, Items.price * Order_Items.quantity AS item_total
FROM Orders
WHERE Orders.order_id = :order_idINPUT_FROM_CLICK
INNER JOIN Order_Items ON Orders.order_id = Order_Items.order_id
INNER JOIN Items ON Order_Items.item_id = Items.item_id

--OR 
SELECT Orders.order_id, Items.item_name, Order_Items.quantity, Items.price * Order_Items.quantity AS item_total
FROM Orders
INNER JOIN Order_Items ON Orders.order_id = Order_Items.order_id
INNER JOIN Items ON Order_Items.item_id = Items.item_id

-- query for the total of an order
SELECT Orders.total FROM Orders WHERE Orders.order_id = :order_idINPUT_FROM_CLICK

-- query for adding a new order
INSERT INTO Orders (cust_id, emp_id, date, total, credit_card_num, exp_date, credit_card_code)
	VALUES (:cust_idINPUT_FROM_DROPDOWN, :emp_idINPUT_FROM_DROPDOWN, :dateIn, NULL, :credit_card_numIn, :exp_dateIn, :credit_card_codeIn)

-- query for adding order items
INSERT INTO Order_Items (order_id, item_id, quantity)
	VALUES (:order_idFROM_NEW_ORDER, :item_idINPUT_FROM_DROPDOWN, :quantityIn)

-- query for editing an order
UPDATE Orders SET cust_id=:cust_idINPUT_FROM_DROPDOWN, emp_id=:emp_idINPUT_FROM_DROPDOWN, date=:dateIn, credit_card_num=:credit_card_numIn,
	exp_date=:exp_dateIn, credit_card_code=:credit_card_codeIn
WHERE order_id=:order_idINPUT_FROM_CLICK

-- query for editing order items
UPDATE Order_Items SET item_id=:item_idINPUT_FROM_DROPDOWN, quantity=:quantityIn
WHERE order_id=:order_idINPUT_FROM_CLICK

-- query for deleting an order
DELETE FROM Orders WHERE order_id=:order_idINPUT_FROM_CHECKBOXES

-- query for deleting order items
DELETE FROM Order_Items WHERE order_id=:order_idINPUT_FROM_CLICK AND item_id=:item_idINPUT_FROM_CHECKBOXES

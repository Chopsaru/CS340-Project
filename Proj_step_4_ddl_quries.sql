/* Item Page Queries*/

SELECT * FROM Items

INSERT INTO Items (item_id, price, item_name, description, quantity_avaliable) 
	VALUES (NULL, :priceIn, :nameIn, :descIn, :quantityIn)

UPDATE Items SET price=:priceIn, item_name=:nameIn, description=:descIn, quantity_avaliable=:quantityIn WHERE item_id=item_idIn

DELETE FROM Items WHERE item_id=:item_idIn /*loop this query for each id selected


/* Customer Page Queries*/

SELECT * FROM Customers

INSERT INTO Customers (cust_id, email, first_name, last_name, phone_number) 
	VALUES (NULL, :emailIn, :fnIn, :lnIn, :phoneIn)

UPDATE Items SET email=:emailIn, first_name=:fnIn, last_name=:lnIn, phone_number=:phoneIn WHERE cust_id=cust_idIn

DELETE FROM Customers WHERE cust_id=:cust_idIn /*loop this query for each id selected

/* Customer Page Queries*/
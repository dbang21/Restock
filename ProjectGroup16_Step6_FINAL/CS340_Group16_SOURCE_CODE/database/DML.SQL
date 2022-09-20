--
-- Households Queries
--

-- READ/SELECT
SELECT Households.id_household AS ID, Households.name AS Name, Households.address AS Address
FROM Households;

-- READ/SELECT for update household form
SELECT Households.id_household AS ID, Households.name AS Name, Households.address AS Address
FROM Households
WHERE id_household = %s

-- CREATE/INSERT
INSERT INTO Households (name, address)
VALUES (%s, %s);

-- UPDATE
UPDATE Households
SET Households.name = %s, Households.address = %s
WHERE id_household = %s;

-- DELETE
DELETE FROM Households
WHERE id_household = %s;


--
-- Household Members Queries
--

-- READ/SELECT
SELECT Households_Members.id_household_member AS ID, Households_Members.name AS Name, IF(runner_status=1, 'Dedicated Runner', '') AS 'Runner Status', Households.name AS Household
FROM Households_Members
LEFT JOIN Households ON Households_Members.id_household = Households.id_household;

-- READ/SELECT for update household form
SELECT Households_Members.id_household_member AS ID, Households_Members.name AS Name, Households.id_household AS Household, runner_status as "Runner Status"
FROM Households_Members
LEFT JOIN Households ON Households_Members.id_household = Households.id_household
WHERE id_household_member = %s;

-- CREATE/INSERT (NO NULL)
INSERT INTO Households_Members (name, runner_status, id_household)
VALUES (%s, %s, %s);

-- CREATE/INSERT (NULLABLE FK -- id_household)
INSERT INTO Households_Members (name, runner_status)
VALUES (%s, %s);

-- UPDATE (NO NULLABLE)
UPDATE Households_Members
SET Households_Members.name = %s, Households_Members.id_household = %s, Households_Members.runner_status = %s
WHERE id_household_member = %s;

-- UPDATE (NULLABLE FK -- id_household)
UPDATE Households_Members
SET Households_Members.name = %s, Households_Members.runner_status = %s, Households_Members.id_household = NULL
WHERE id_household_member = %s;

-- DELETE
DELETE FROM Households_Members
WHERE id_household_member = %s;


--
-- Household Inventories Queries
--

-- READ/SELECT
SELECT Households_Inventories.id_household_inventory AS ID, Households.name AS Household, Households_Items.name
    AS Item, Households_Inventories.amount_left AS 'Amount Left', IF(restock_status=1, 'Restock', '') AS 'Restock Status'
FROM Households_Inventories
INNER JOIN Households ON Households.id_household = Households_Inventories.id_household
INNER JOIN Households_Items ON Households_Items.id_item = Households_Inventories.id_item
ORDER BY Households_Inventories.id_household_inventory ASC;

-- READ/SELECT for update household form
SELECT Households_Inventories.id_household_inventory AS ID, Households.name AS Household, Households_Items.name
    AS Item, Households_Inventories.amount_left AS 'Amount Left', IF(restock_status=1, 'Restock', '') AS 'Restock Status'
FROM Households_Inventories
INNER JOIN Households ON Households.id_household = Households_Inventories.id_household
INNER JOIN Households_Items ON Households_Items.id_item = Households_Inventories.id_item
WHERE id_household_inventory = %s
ORDER BY Households_Inventories.id_household_inventory ASC;

-- CREATE/INSERT
INSERT INTO Households_Inventories (id_household, id_item, amount_left, restock_status)
VALUES (%s, %s, %s, %s);

-- UPDATE
UPDATE Households_Inventories
SET Households_Inventories.amount_left = %s, Households_Inventories.restock_status = %s
WHERE id_household_inventory = %s;

-- DELETE
DELETE FROM Households_Inventories
WHERE id_household_inventory = %s;


--
-- Household Items Queries
--

-- READ/SELECT
SELECT Households_Items.id_item AS ID, Items_Types.name AS 'Item Type', Households_Items.name
    AS Name, Households_Items.best_if_used_by AS 'Best If Used By'
FROM Households_Items
INNER JOIN Items_Types ON Items_Types.id_item_type = Households_Items.id_item_type;

-- CREATE/INSERT
INSERT INTO Households_Items (id_item_type, name, best_if_used_by)
VALUES (%s, %s, %s);


--
-- Item Types Queries
--

-- READ/SELECT
SELECT Items_Types.id_item_type AS ID, name AS "Item Type"
FROM Items_Types;

-- CREATE/INSERT
INSERT INTO Items_Types (name)
VALUES (%s);


--
-- Store Inventories Queries
--

-- READ/SELECT
SELECT Items_Types.name AS 'Item Type', Stores.name AS Store
FROM Stores_Inventories
INNER JOIN Items_Types ON Items_Types.id_item_type = Stores_Inventories.id_item_type
INNER JOIN Stores ON Stores.id_store = Stores_Inventories.id_store;

-- CREATE/INSERT
INSERT INTO Stores_Inventories (id_item_type, id_store)
VALUES (%s, %s);


--
-- Stores Queries
--

-- READ/SELECT
SELECT Stores.id_store AS ID, Stores.name AS Name, Stores.address
    AS Address, Stores.hours_open AS "Hours Open"
FROM Stores;

-- READ/SELECT for update household form
SELECT Stores.id_store AS ID, Stores.name AS Name, Stores.address
    AS Address, Stores.hours_open AS 'Hours Open'
FROM Stores
WHERE id_store = %s;

-- CREATE/INSERT (no nullable attribute)
INSERT INTO Stores (name, address, hours_open)
VALUES (%s, %s, %s);

-- CREATE/INSERT (nullable hours_open)
INSERT INTO Stores (name, address)
VALUES (%s, %s);

-- UPDATE (no nullable attribute)
UPDATE Stores
SET name = %s, address = %s, hours_open = %s
WHERE id_store = %s;

-- UPDATE (nullable hours_open)
UPDATE Stores
SET name = %s, address = %s, hours_open = NULL
WHERE id_store = %s;

-- DELETE
DELETE FROM Stores
WHERE id_store = %s;
